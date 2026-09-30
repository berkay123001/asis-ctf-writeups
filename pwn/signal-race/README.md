# Signal Race · Pwn

**Öz:** Bookmark nesnesi frame neslini tek baytta saklıyor. Slot yeniden kullanıldığında nesil sarması, eski bookmark'a yeni frame üzerinde okuma ve yazma yetkisi veriyor.

**Doğrulama:** Uzak servis `ASIS{8d88aebc6d193672f1e3a2ddced7bc58b2769d1f}` döndürdü. Betikteki çevrimdışı seal kontrolü ayrıca tekrar üretilebilir.

## İlk kırılma: generation wrap

VM'de `NOTE`, `NEW`, `DROP`, `BOOKMARK`, `READ` ve `WRITE` komutları var. Bookmark, slotun generation değerini 8 bit saklıyor. 128 adet `DROP` + `NEW` çevrimi generation'ı 256 artırınca kayıtlı bayt eski değerine dönüyor. Eski bookmark, artık NOTE olmayan canlı FRAME slotunu kabul ediyor. Böylece 192 baytlık frame okunuyor.

## İkinci kırılma: mühürleri yeniden kurma

Frame üzerinde FNV-1a ve oturum anahtarından türetilen `seal1` kontrolü var. FNV anahtarsız. `seal1` için kullanılan `splitmix64` çarpanları tek sayı olduğundan mod `2^64` altında terslenebilir; okunan frame'in bilinen alanlarından oturum anahtarı geri hesaplanıyor. [solve.py](solve.py) anahtarı doğruluyor, frame seçicisini flag yoluna çeviriyor ve iki mührü yeniden yazıyor.

## Üçüncü kırılma: checkpoint

`RUN` içindeki `0x92` opcode'u zaman alan bir döngü çalıştırıyor. Kısa aralıkla kurulan `TIMER`, bu pencerede `SIGALRM` tetikleyerek checkpoint oluşturuyor. `RESTORE`, geçerli checkpoint ve özel seçicili frame ile `/flag` dosyasını okuyor.

```text
8-bit bookmark sarması → frame okuma → seal1 anahtarı → frame değişikliği
→ SIGALRM checkpoint → RESTORE → flag
```

Yalnızca aritmetik ve frame yamalama kısmını ağ olmadan kontrol etmek için `python3 solve.py --selftest` kullanılabilir. Tam exploit servis zamanlamasına bağlıdır ve [signal-race-vm](signal-race-vm) özgün ikilisiyle ilişkilidir.
