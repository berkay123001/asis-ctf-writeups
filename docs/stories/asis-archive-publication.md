# Story: ASIS çözüm arşivi yayımla

## Amaç

Mevcut ASIS çalışma klasöründen doğrulanmış çözümleri ayrı, okunabilir bir public GitHub deposuna taşımak. Çözümsüz araştırmalar yayımlanmaz. Her writeup yöntem, kanıt ve yeniden üretim sınırını açıklar.

## Kabul kontrolü

- [x] Kaynak klasördeki çözüm kayıtları ve yanıltıcı `fake_flag`/yerel test örnekleri ayrıldı.
- [x] Dokuz tam çözüm ve bir debugger ile flag kurtarma kaydı kategoriye göre listelendi.
- [x] Her kayıtta temel fikir, kritik adımlar, kanıt türü ve sınırlama belirtildi.
- [x] Çözümsüz klasörler, kişisel test anahtarları ve geniş çalışma notları yayın dizinine alınmadı.
- [x] Yalnızca seçili çözümlere ait kod ve gerekli örnek artefaktlar kopyalandı.
- [x] Yayın öncesi yerel dosya ve bağlantı denetimi tamamlandı (42 Markdown bağlantısı, kaynak derleme kontrolü, Mario GCM doğrulaması ve Signal Race selftest).
- [x] Yeni Git deposu oluşturuldu ve public GitHub deposuna gönderildi.

`npm run lint`, `npm run typecheck` ve `npm test` denendi. Bu dokümantasyon arşivinde `package.json` ve ilgili npm betikleri bulunmadığından üç komut da `Missing script` ile bitti. Kod için uygun çevrimdışı kontroller yukarıda kaydedildi.

## File list

- `README.md` — arşivin amacı, kategori dizini ve kapsamı.
- `web/{portalis,proxydough,profile}/README.md` — web writeup'ları.
- `pwn/{qfilter,revenant-buddy,signal-race,dead-letter-queue}/README.md` — pwn writeup'ları.
- `crypto/mario/README.md`, `rev/atarude/README.md`, `misc/2048/README.md` — diğer kategori writeup'ları.
- `docs/PROVENANCE.md` — kaynak ve kanıt türü tablosu.
- İlgili klasörlerde `solve.py`, `exploit.js`, `source/`, `work/` — seçili çözüm kodu ve işe yarayan analiz yardımcıları.
- İlgili klasörlerde `output.txt`, `qjs`, `revenant-worker`, `signal-race-vm`, `relay`, `warden`, `worker`, `Atarude`, `flag.enc` — çözümü anlamak veya doğrulamak için gereken seçili artefaktlar.
