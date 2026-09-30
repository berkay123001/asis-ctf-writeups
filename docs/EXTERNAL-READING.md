# Bağımsız çözümlerle birlikte okuma

Bu sayfa, [kendi doğrulanmış arşivimdeki](../README.md) yöntemleri başka yazarların yayımladığı çözümlerle yan yana okumak içindir. Araştırma tarihi: **30 Eylül 2026**. Dış yazılardaki kod veya flag'ler bu depoya taşınmadı; bağlantılar yazarların özgün sayfalarına gider. Dışarıdaki bir başarıyı kendi çözüm sayımına eklemiyorum.

## Aynı soruya farklı bakış

| Soru | Bu arşiv | Bağımsız kaynak | Okumaya değer fark |
|:--|:--|:--|:--|
| Atarude | [Debugger ile kurtarma](../rev/atarude/README.md) | [trefor: normal akış çözümü](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/rev/atarude/README.md) | 11 blokluk ciphertext splice ve birleşik MAC; bizim kurtarma kaydımızla aynı iddia değil. |
| Dead Letter Queue | [Dolu kuyruk sınırı](../pwn/dead-letter-queue/README.md) | [trefor: sarmış kuyruk](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/pwn/dead-letter/README.md) | Aynı eksik aralık taramasının iki farklı sınır durumu. |
| QFilter | [Getter tabanlı okuma](../pwn/qfilter/README.md) | [trefor: farklı tahsis zinciri](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/pwn/qfilter/README.md) | 15/31 baytlık leak ayrımı ve `Reflect.apply` ile çağrı. |
| Mario | [Ortak görüntü](../crypto/mario/README.md) | [Abdelkad3r: polar çekirdekler](https://github.com/Abdelkad3r/ASIS-CTF-Quals-2026/blob/master/Crypto/Mario/README.md) | Aynı oil uzayı, ortak çarpan ve rank-2 çekirdekler üzerinden türetiliyor. |
| ProxyDough | [İki URL ayrıştırıcısı](../web/proxydough/README.md) | [trefor: bağımsız istek zinciri](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/web/proxy-dough/README.md) | İç URL'de ham `\` ile dış sorgu parametresindeki `%5C` farkı. |
| Profile | [Altı EF_ADN parçası](../web/profile/README.md) | [trefor: eSIM akışı](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/web/profile/README.md) | Yazar, test PKI kimliğini istekten hemen önce yenileme ihtiyacını anlatıyor; bizim tarihsel betiğimiz tek başına yeniden çalışmaz. |
| Revenant Buddy | [Tür aklama](../pwn/revenant-buddy/README.md) | [trefor: VM programı](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/pwn/revenant-buddy/README.md) | Aynı capability kökeni hatasına farklı opcode seçimiyle yaklaşım. |
| Signal Race | [Bookmark ve checkpoint](../pwn/signal-race/README.md) | [trefor: iki mühür ve zamanlama](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/pwn/signal-race/README.md) | Dış anlatım ikinci mührü ve `TIMER`/`RUN` zamanlamasını ayrıca açıyor; bu kodun doğrulaması bizim selftest'in kapsamı değil. |
| 2048 / Citadel Grid | [Tribes deserialization](../misc/2048/README.md) | [trefor: Web/2048](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/web/2048/README.md) | Başlangıç ipuçları, cluster frame'i ve iki parçalı flag yolu daha ayrıntılı. |

Portalis için bu taramada aynı soruya ait, yazarının kendi yöntemi olarak yayımladığı eşleşen bir writeup doğrulamadım. Bu, internette hiç çözüm olmadığı anlamına gelmez.

## Bu arşivde çözülmemiş, dışarıda çözümü yayımlanmış

Aşağıdakiler **benim çözüm listeme dahil değil**. Kendi yarım kalmış notlarım veya betiklerim public depoya alınmadı; yalnızca başkasının yazısına bağlantı veriliyor.

| Soru | Dış yazarın writeup'ı | Konu |
|:--|:--|:--|
| Mousa | [trefor](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/rev/mousa/README.md) | Şifreleme/MAC yapısının terslenmesi. |
| Collector | [trefor](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/rev/collector/README.md) | Tersine mühendislik ve challenge sonucunun yorumlanması. |
| OutOfPhase | [trefor](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/hardware/out-of-phase/README.md) | Faz kaymalı sinyal çözümlemesi. |
| The Lottery Race | [trefor](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/web/the-lottery-race/README.md) | Bilet/kimlik doğrulama zinciri. |

Okuma sırası önerisi: önce kendi sayfamdaki **kanıt ve sınır** bölümünü, sonra dış yazıdaki yöntem farkını inceleyin. Farklı yolların aynı flag'e varması öğreticidir, ancak dışarıda yayımlanmış bir betik bizim arşivimizde yeniden üretildiği anlamına gelmez.
