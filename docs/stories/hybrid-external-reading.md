# Story: Çözüm arşivine bağımsız okuma katmanı ekle

## Amaç

Kendi doğrulanmış ASIS çözümleri ile başka yazarların writeup'larını birlikte okunabilir hâle getirmek. Kaynak ve başarı sahipliğini açık tutmak; çözümsüz yerel çalışmaları yayımlamamak.

## Kabul kontrolü

- [x] Aynı yarışmadan yazarın kendi yayımladığı writeup bağlantıları challenge bazında incelendi.
- [x] Kendi çözümler ile dışarıdaki farklı yöntemler kaynak gösterilerek karşılaştırıldı.
- [x] Kendi arşivimde çözülmemiş sorular yalnızca ayrı dış okuma listesine alındı; yerel dosyalar ve üçüncü taraf kodu eklenmedi.
- [x] Atarude'daki debugger kurtarma ile dış yazarın normal akış çözümü farklı doğrulama iddiaları olarak bırakıldı.
- [x] ProxyDough örneğindeki ham ters eğik çizgi sayısı, kayıtlı başarılı istekle karşılaştırılarak düzeltildi.
- [x] Yerel bağlantı, Markdown ve npm kalite kapıları çalıştırılıp sonuçları kaydedildi.
- [x] Değişiklikler public depoya gönderildi.

## File list

- `README.md` — hibrit dizine giriş ve başarı sahipliği ayrımı.
- `docs/EXTERNAL-READING.md` — kaynaklı dış okuma ve dışarıda çözülmüş ayrı sorular.
- `docs/PROVENANCE.md` — dış kaynakların doğrulama statüsü.
- `rev/atarude/README.md`, `pwn/dead-letter-queue/README.md`, `pwn/qfilter/README.md`, `crypto/mario/README.md`, `web/proxydough/README.md` — challenge içinde yöntem karşılaştırması ve bir tarihsel örnek düzeltmesi.
- `docs/stories/hybrid-external-reading.md` — bu işin kapsamı ve denetimi.

## Doğrulama

Yerel Markdown dosyalarında 56 göreli bağlantı tarandı, eksik hedef bulunmadı. `git diff --check` temiz. `npm run lint`, `npm run typecheck` ve `npm test` komutları çalıştırıldı; bu dokümantasyon deposunda `package.json`/ilgili betikler olmadığı için her biri `Missing script` ile bitti. Haricî GitHub yolları kaynak depoların ağaçlarında doğrulandı; dış betikler bu çalışma kapsamında çalıştırılmadı.
