# QFilter · Pwn

**Öz:** QuickJS'nin `Array.prototype.customFilter` uygulaması, belirli bir dizide öğelerin referans sayısını fazla azaltıyor. Serbest bırakılan nesneler yeni tahsislerle yeniden kullanıldığında bellek okuma ve çağrı yönlendirme mümkün oluyor.

**Doğrulama:** Arşivdeki payload canlı servisten `ASIS{m337_7h3_br4nd_n3w_QJS_4ll0c470r_334811b53075}` yanıtını aldı.

## Kusur nerede?

Fast-array yolunda öğelerin `JS_DupValue` ile tutulması ilk slotun JS nesnesi olmasına bağlı. Callback sonrası temizleme ise bütün slotlara `JS_FreeValue` uyguluyor. İlk eleman nesne olmadığında, sonraki nesne ve stringler beklenenden erken serbest kalıyor. `exploit.js` diziyi bu yüzden `0` ile başlatıyor.

## Zincir

1. 31 karakterlik string ve üç nesne erken serbest bırakılıyor.
2. Aynı boyut sınıfındaki `ArrayBuffer`, veri bloğu ve `Uint8Array` tahsisleri boşalan alanı tekrar kullanıyor.
3. Eski string görünümü üzerinden `JSTypedArray` işaretçisi sızıyor.
4. `ArrayBuffer.prototype.byteLength` getter'ı sahte nesnede kullanılarak 32 bitlik okuma elde ediliyor.
5. Okumalarla PIE tabanı ve fonksiyon nesnesi bulunuyor. Sahte JS fonksiyon nesnesi `js_os_exec`'e yönlendirilip `/readflag` çağrılıyor.

Bu son adımın offsetleri yayımlanan [qjs](qjs) sürümüne özeldir; farklı QuickJS derlemesinde aynı sayıları kullanmak işe yaramaz. Sürümün ve tahsis boyutlarının çözümün bir parçası olmasının nedeni bu.

## Arşiv

[exploit.js](exploit.js) bellek zincirini, [solve.py](solve.py) ise yarışma servisinin `-- EOF --` protokolünü ve yanıt ayrıştırmasını gösterir. `solve.py` eski canlı hedefi varsayılan olarak içerir. `qjs` orijinal çözümlü challenge dağıtımından alınan analiz artefaktıdır; burada servis veya SUID `/readflag` çalıştırılmıyor.
