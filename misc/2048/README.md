# 2048 / Citadel Grid · Misc

**Öz:** Tomcat Tribes kanalı, çözülemeyen şifreli veri sonrasında yine Java deserialization yoluna düşüyordu. Geçerli bir Tribes frame'ine yerleştirilen CommonsCollections6 nesnesi, flag'in iki parçasını okunabilen paylaşımlı alana taşıdı.

**Doğrulama:** İki ayrı dosyadan gelen parçalar birleştirildi ve `ASIS{t0McAT_was_Th3_KEY}` elde edildi.

## İpuçlarından yola çıkış

`robots.txt`, `/citadel/lab-notes.html` yoluna yönlendirdi. `/diagnostics.jsp` belirli bir localhost başlığıyla Tomcat 9.0.116, Commons Collections 3.2.1, şifreleme modu ve `:4000` Tribes kanalına dair bilgi verdi. Bunlar saldırı yüzeyini belirledi; sayfadaki ilk `ASIS{...}` değerleri ise gerçek sonuca ulaşmadan görülebilen decoy'lardı.

## Zincir

`solve.py`, CommonsCollections6 yükünü Java serialized nesne biçiminde üretiyor. Bunu `FLT2002` başlangıcı, `ChannelData` ve `TLF2003` bitişinden oluşan Tribes frame'ine koyup `:4000` kanalına gönderiyor. Bu örnekte şifre çözme hatası yükün deserialization yoluna gitmesini engellemedi.

Yük, iki dosyayı `/opt/citadel/shared` altında etiketli parçalara kopyaladı. Sonra `/mirror.jsp?parcel=half1` ve `half2` yoluyla parçalar okundu:

```text
ASIS{t0McAT_was
_Th3_KEY}
```

Bu birleşim hem formatı hem de challenge'ın iki ayrı kaynaktan okuma fikrini doğruluyor. Doğrudan görülen `vault/flag.txt` benzeri alanlar sonucun yerine geçmedi.

## Tekrar üretme sınırı

[solve.py](solve.py) tarihsel hedef adresini içerir ve `gadgets/ysoserial.jar` dosyasını bekler. 57 MB'lık üçüncü taraf JAR arşive kopyalanmadı. Frame kurma ve parça birleştirme mantığı betikte incelenebilir; çalışan servis olmadan canlı sömürü yeniden üretilemez.
