# Yayın kapsamı ve kaynak izi

Bu depo `/home/berkayhsrt/ASIS-CFT` içindeki geçmiş yarışma çalışma klasöründen seçilerek hazırlandı. Orijinal klasör Git deposu değildi ve bu yayın için değiştirilmedi. Aşağıdaki tablo, hangi kanıtın sonuç iddiasını desteklediğini gösterir.

| Writeup | İlk kaynak / kayıt | Sonuç ölçütü |
|:--|:--|:--|
| [Portalis](../web/portalis/README.md) | `web/portalis/WRITEUP.md`, `ssrf.py` | `/api/preview` iç `/flag` gövdesini döndürdü |
| [ProxyDough](../web/proxydough/README.md) | `web/ProxyDough_…/ProxyDough/api/`, canlı istek kaydı | İki `HTTP 200` yanıtı aynı flag'i verdi; verilen `recipe.php` içindeki fake flag ayrı tutuldu |
| [Profile](../web/profile/README.md) | `web/profile/NOTES`, `FLAG`, `solve.py` | Altı EF_ADN parçası ve kaydedilen flag eşleşiyor |
| [QFilter](../pwn/qfilter/README.md) | `pwn/QFilter/NOTES`, `FLAG`, `exploit.js` | Canlı servis flag yanıtı |
| [Revenant Buddy](../pwn/revenant-buddy/README.md) | `pwn/Revenant-Buddy_…/NOTES`, `FLAG`, `solve.py` | Uzak worker `OK ASIS{…}` döndürdü |
| [Signal Race](../pwn/signal-race/README.md) | `pwn/signal-race/NOTES`, `STATUS`, `FLAG`, `solve.py` | Uzak `RESTORE` yanıtı ve çevrimdışı mühür kontrolü |
| [Dead Letter Queue](../pwn/dead-letter-queue/README.md) | `pwn/dead-letter-queue_…/` ikilileri, oturum arşivindeki `dlq_exp.py` | Yerel uçtan uca test ve uzak flag yanıtı |
| [Mario](../crypto/mario/README.md) | `crypto/Mario_…/Mario/solve.py`, `output.txt` | AES-GCM etiketi doğrulanarak plaintext açıldı |
| [Atarude](../rev/atarude/README.md) | `rev/Atarude_…/Atarude/`, debugger çıktı kaydı | İki çalışmada aynı flag; normal girdi çözümü yok |
| [2048 / Citadel Grid](../misc/2048/README.md) | `misc/2048/NOTES`, `FLAG`, `solve.py` | İki parçanın canlı okunmasıyla flag oluştu |

Yayıma yalnızca bu on çözüm/kurtarma kaydı alındı. `Mousa`, `Collector`, `Dark Pixels`, `OutOfPhase`, `Lottery Race` gibi tamamlanmamış çalışmalar ve ham çalışma notları eklenmedi. Kaybolmuş çözüm dosyaları için sayı veya başarı iddiası türetilmedi.

## Dış kaynakların statüsü

[Bağımsız okuma rehberindeki](EXTERNAL-READING.md) bağlantılar üçüncü taraf yazarların kendi depolarına gider. Arşivde çözülmemiş sorular için dış writeup bulmak, yukarıdaki yerel çözüm tablosuna yeni bir başarı eklemez. Üçüncü taraf metinleri, kodları ve flag'leri bu depoya kopyalanmadı; challenge sayfalarındaki kısa karşılaştırmalar yazarı belirtilmiş okuma önerileridir. Dış yazarın belirttiği çalıştırma sonucu, ayrıca yerel olarak denenmedikçe burada doğrulanmış sonuç diye sunulmaz.

## Artefakt kimliği

| Dosya | SHA-256 |
|:--|:--|
| `rev/atarude/Atarude/Atarude` | `a9ae09a1056b2350b863f9668d462b330a3a087a0dd4aa4322cb791244a9c829` |
| `rev/atarude/Atarude/flag.enc` | `2468045a254092a7edbad0bd30376dacaf963ffdaa5e83af8dea6a819d0d719e` |

Diğer yayımlanan kod dosyaları, çalışma klasöründeki ilgili çözümlü challenge altından aynen kopyalandı. `pwn/dead-letter-queue/solve.py`, aynı klasörde kalıcı kopyası bulunmadığı için geçmiş oturumun doğrulanmış `dlq_exp.py` içeriğinden geri alındı. Bu ayrım, kaynakların nereden geldiğini açık tutar.

## Yeniden üretim

Canlı servis gerektirmeyen kontroller: `crypto/mario/solve.py` için sağlanan `output.txt` ve GCM etiketi; `pwn/signal-race/solve.py --selftest` için mühür dönüşümü. Ağ tabanlı betiklerin varsayılan hedefleri tarihi yarışma örneğini gösterir ve servislerin bugün erişilebilir olduğu varsayılmaz. Bazı betikler ek yarışma dosyalarına veya o oturumda kurulan harici araca bağımlıdır; her writeup bunu belirtir.
