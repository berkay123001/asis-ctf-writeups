# ProxyDough · Web

**Öz:** PHP URL doğrulaması ile yönlendirme zincirindeki URL yorumlaması ayrışınca, görünürde izinli görsel sunucusundan başlayan istek localhost'a ulaştı.

**Doğrulama:** Canlı `api/proxy.php` yanıtı iki kez aynı gerçek flag'i döndürdü. Dağıtılan `recipe.php` içindeki `ASIS{fake_flag}` yalnızca örnek/decoy değerdir.

## Problem

`api/proxy.php`, `parse_url($url)` ile `scheme=https` ve `host=img.proxydough.net` şartlarını kontrol ediyor. Ardından aynı URL'yi `file_get_contents` ile çağırıp gövdeyi dönüyor. `api/recipe.php` ise yalnızca `REMOTE_ADDR` loopback olduğunda gerçek flag'i veriyor.

## Zincirin kurulması

Görsel alanında Cloudflare Image Resizing'in `onerror=redirect` seçeneği vardı. Görsel işleme başarısız olduğunda hedef URL'ye yönlendirme üretiyordu. PHP HTTP wrapper yönlendirmeyi takip edince, ilk URL için yapılmış host kontrolü ikinci hedefe uygulanmadı.

Sıradan `https://proxydough.net/api/recipe.php` yönlendirmesi uygulamaya ulaşıyor, fakat uzak IP nedeniyle `Access not allowed.` dönüyordu. Bu hata önemliydi: ilk iki adımın çalıştığını, eksik parçanın loopback bağlantısı olduğunu gösterdi.

Başarılı örnekte yönlendirme URL'sinde **ham ters eğik çizgi** vardı:

```text
https://img.proxydough.net/cdn-cgi/image/onerror=redirect/http://proxydough.net\@127.0.0.1/api/recipe.php
```

Cloudflare bu değeri yönlendirmeye taşıdı. PHP'nin sonraki URL ayrıştırması son `@` işaretinden sonraki `127.0.0.1` adresine bağlandı; böylece `recipe.php` isteği loopback kaynağından geldi. `%5C` yazımı aynı bayt dizisi olmadığından bu denemede işe yaramadı. Son istek, proxy'nin `url` parametresi bu görsel URL'si olacak şekilde yapıldı.

Canlı sonuç: `ASIS{802ab2a8f0f435759ad6d1dfe8999de0}`.

## Öğrenilen ders

Bir URL'nin yalnızca ilk hop'unu denetlemek, yönlendirmeleri de denetlemek anlamına gelmez. Ham isteğin baytları bu çözümde belirleyiciydi; istemci tarafından normalleştirilen veya yüzde kodlanmış sürüm farklı davranıyor. [Verilen PHP kaynakları](source/proxy.php), kontrolün nerede uygulandığını ve loopback şartını incelemek için eklendi. Kaynakta görünen fake flag'in canlı flag kanıtı olarak kullanılmaması gerekiyor.
