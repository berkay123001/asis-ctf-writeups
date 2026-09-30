<div align="center">

# ASIS CTF · Çözüm Arşivi

**Bir flag'den çok, oraya giden düşünce zinciri.**

ASIS CTF arşivimden doğrulanmış çözümler ve yerel olarak yeniden üretilebilen analizler.

[Web](#web) · [Pwn](#pwn) · [Crypto](#crypto) · [Reverse](#reverse) · [Misc](#misc)

</div>

---

Bu koleksiyon, elimde çözüm kanıtı ve yeterli teknik notu bulunan çalışmalardan oluşur. Yarışmadaki bütün soruları veya geçmişte çözdüğüm bütün soruları temsil etmez; bazı eski çözümlerin dosyaları günümüze ulaşmadı. Her sayfada sonuç, temel fikir, çözüm adımları ve doğrulama sınırı açıkça yazılıdır.

| Kategori | Çalışma | Temel konu | Kayıt |
|:--|:--|:--|:--|
| Web | [Portalis](web/portalis/README.md) | Prototype pollution → SSRF | Canlı flag |
| Web | [ProxyDough](web/proxydough/README.md) | Farklı URL ayrıştırıcıları, ham `\` | Canlı flag |
| Web | [Profile](web/profile/README.md) | eSIM profil indirme, EF_ADN | Canlı flag |
| Pwn | [QFilter](pwn/qfilter/README.md) | QuickJS use-after-free | Canlı flag |
| Pwn | [Revenant Buddy](pwn/revenant-buddy/README.md) | VM tür denetimi, capability aktarımı | Canlı flag |
| Pwn | [Signal Race](pwn/signal-race/README.md) | Generation wrap, checkpoint | Canlı flag |
| Pwn | [Dead Letter Queue](pwn/dead-letter-queue/README.md) | Kuyrukta dangling entry | Canlı flag |
| Crypto | [Mario](crypto/mario/README.md) | Sonlu cisimde altuzay kurtarma | GCM etiketi doğrulandı |
| Reverse | [Atarude](rev/atarude/README.md) | MAC analizi ve debugger ile flag kurtarma | Debugger ile flag |
| Misc | [2048 / Citadel Grid](misc/2048/README.md) | Tomcat Tribes deserialization | Canlı flag |

## Nasıl okunur?

Önce ilgili sayfanın **Problem** ve **Kilit gözlem** kısımlarına bakın; spoiler istemiyorsanız flag bölümünü sona bırakın. `solve.py` dosyaları çözüm anında kullanılan betiklerin arşiv kopyalarıdır. Bir kısmı artık erişilemeyebilen yarışma sunucularına varsayılan olarak bağlanır. Yerel inceleme için writeup'taki çevrimdışı doğrulama adımlarını kullanın.

İkili dosyalar yalnızca çözümlü challenge'lara ait, ilgili betiğin analizini yeniden üretmeye yarayan seçilmiş yarışma artefaktlarıdır. `output.txt` Mario'nun herkese verilen şifreli örneğidir. Sır, özel hesap anahtarı, çözümsüz challenge veya tüm eski çalışma klasörü bu repoda yer almaz. Challenge dağıtımına ait üçüncü taraf büyük araçlar da kopyalanmadı.

Bu notlar geçmiş yarışma örneklerine özeldir. Her çözümün doğrulama türünü tabloda ayrı gösterdim; özellikle Atarude'daki debugger ile flag kurtarma, normal program akışında geçerli bir girdi üretildiği anlamına gelmez.

## Dizinin yapısı

```text
web/      Portalis · ProxyDough · Profile
pwn/      QFilter · Revenant Buddy · Signal Race · Dead Letter Queue
crypto/   Mario
rev/      Atarude
misc/     2048 / Citadel Grid
docs/     Yayın kapsamı ve kontrol kaydı
```

Sorular ve düzeltmeler için GitHub Issues kullanılabilir. Yeni challenge'lar yalnızca doğrulanmış bir çözüm ve anlaşılır bir anlatımla eklenir.
