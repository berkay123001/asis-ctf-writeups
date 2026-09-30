# Atarude · Reverse engineering

**Öz:** Stripped Rust ikilisindeki tablo tabanlı özet ve MAC işlemi incelendi. Şifreli `flag.enc`, başarısız birleşik MAC sonucunun debugger içinde beklenen özetle değiştirilmesi sonrası açıldı.

**Doğrulama türü:** Orijinal [Atarude](Atarude/Atarude) ikilisi ve [flag.enc](Atarude/flag.enc) ile iki ayrı debugger çalışmasında aynı flag yazıldı; süreç normal çıktı koduyla sonlandı. Normal protokolde kabul edilen bir girdi üretilmedi.

## Yapı

İkili, girdi şeritleri üzerinde MAC kontrolleri yapıyor. `work/atarude.py`, verilen ikilinin tablosundan 16 baytlık anahtarı türetiyor ve gözlenen AES/MAC işlemlerinin Python karşılığını içeriyor. Anahtar sabit bir string olarak varsayılmıyor; dosyadaki tablo üzerinden hesaplanıyor.

Önceki analizde altı şerit için `e,e,s` oturumları oluşturulmuştu. Bunların bir kısmı bireysel kontrollerden geçti. Birleşik MAC ise son kabul adımında başarısız kaldı. Bu nedenle tek bir `ok` satırı programın çözülmüş olduğu anlamına gelmiyor.

## Flag'in çıkarılması

Debugger, reddedilme yolunu geçip birleşik MAC'in hesaplanan 16 baytlık özetini ikilideki beklenen değerle değiştirdi. İkili ardından kendi `flag.enc` doğrulama/açma yolunu çalıştırdı ve şu metni verdi:

```text
ASIS{_iZ_c0p1eD_m4sk5_m4Ke_3Ven_Spl!c3s_vAn1sh!!?}
```

Bu bir **debugger ile flag kurtarma** kaydıdır. Birleşik MAC için dışarıdan gönderilebilecek geçerli preimage bulunmadı; mevcut `work/` kodu da tek komutluk tam bir çözücü değildir. `work/gf.py` ilgili `GF(2^128)` aritmetiğini gösterir. Önceki AES izleri ve bunları işleyen geçici yardımcı betikler bu arşive alınmadı.

## Öğrenilen ders

Bir challenge'ın şifreli artefaktından flag çıkarmak ve challenge doğrulayıcısını normal akışta geçmek ayrı sonuçlardır. İki ayrı debugger çalışması flag'in bu ikili ve bu `flag.enc` ile ilişkisini doğruladı; burada daha ileri bir başarı iddia edilmiyor. Orijinal artefaktların SHA-256 değerleri [yayın kaydında](../../docs/PROVENANCE.md) bulunur.
