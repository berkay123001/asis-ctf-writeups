# Portalis · Web

**Öz:** Sadece izinli alanları kabul eden bir profil API'si, iç içe JSON birleşiminde `constructor.prototype` yolunu korumuyor. Miras alınan `ogImage` alanı önizleme tarafından okununca sunucuya URL isteği yaptırılabiliyor.

**Doğrulama:** Yarışma sunucusunun `/api/preview` yanıtı iç servisin `/flag` gövdesini gösterdi.

## Problem

`PUT /api/theme` profil verisini birleştiriyor; `GET /api/preview` ise profilin görsel önizlemesini üretiyor. `/api/schema` çıktısında `ogImage` gösterilen alanlarda var, ancak yazılabilir alanlarda yoktu. Bu, doğrudan `ogImage` gönderiminin neden etkisiz kaldığını ve önizlemenin yine de bu alanı kullandığını açıklayan ilk ipucuydu.

## Kilit gözlem

Normal bir `links` dizisi API cevabında sayısal anahtarlı nesneye dönüştü. Bu, birleşim işleminin dizilerle nesneleri aynı tür gibi ele aldığına dair gözlemdi. Kaynak kod elimizde olmadığı için birleşimin tam uygulamasını iddia etmiyoruz; sonraki istekler prototip yolunun gerçekten çalıştığını gösterdi.

Doğrudan `{"ogImage":"http://127.0.0.1/"}` gönderildiğinde önizleme değişmedi. Şu gövde gönderildiğinde önizleme seçilen URL'yi fetch etmeye çalıştı:

```json
{"constructor":{"prototype":{"ogImage":"http://127.0.0.1:3000/x"}}}
```

İstek engellense de önizleme `host not allowed` döndürdü. Böylece `ogImage` değerinin profilin kendi alanı olmadan okunabildiği ve URL'nin sunucu tarafındaki fetch yoluna geçtiği gözlendi.

## SSRF'den flag'e

URL denemeleri, `127.0.0.1` gibi açık yazımları engelleyen kontrolün `[::ffff:127.0.0.1]` biçimini kabul ettiğini gösterdi. Bu IPv4 adresinin IPv6 içinde gösterimidir. `GET /api/preview` isteğin sonucunu veya hatasını döndürdüğü için iç servislerden gelen yanıt görülebildi.

İçeride `9001` portundaki servis bulundu. Hedef:

```text
http://[::ffff:127.0.0.1]:9001/flag
```

Önizleme gövdesi `ASIS{Y0U_WeR3nT_SuPp0$eD_To_S3E_Th1S_P0rT@L}` değerini verdi. `3000` portundaki `/api/flag` endpoint'i `403` döndürdüğü için gerçek hedefin o endpoint olmadığı da ayrıştırılmış oldu.

## Öğrenilen ders

Yazılabilir alan listesi, sonradan okunacak nesnenin prototipini korumaz. URL denetimi metinsel gösterim üzerinden yapılıyorsa aynı adrese giden başka gösterimler kaçabilir. Buradaki sömürü için hem veri birleşimi hem de önizleme isteğinin cevabı dışarı aktarması gerekiyordu.

Arşiv dosyaları: [ssrf.py](ssrf.py) ve [scan.py](scan.py). Bu betikler eski yarışma hedefini içerir; writeup'taki istek ve yanıtlar tarihsel kayıttır.
