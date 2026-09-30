# Profile · Web / eSIM

**Öz:** Sayfa yorumlarında sızmış test eUICC kimliği ile altı profil paketi indirildi. Flag, her paketteki EF_ADN kişi adı parçasının birleştirilmesiyle çıktı.

**Doğrulama:** Altı parçanın sırası matching ID'lerle eşleşti ve birleşim `ASIS{as!S_1n_T3lC0_fr0MN_oW}` oldu.

## Problem ve gözlem

Başlangıç sayfasındaki QR verisi bir SM-DP+ adresine işaret ediyordu: `LPA:1$dpp.asisctf.com$`. HTML yorumlarında yazılım test eUICC'sine ait EID, sertifika zinciri ve özel anahtar bulunuyordu. Başka yorumlarda alternatif kimlikler ve eski host adları da vardı; çözümde eşleşen test zinciri kullanıldı.

SM-DP+ akışında `initiateAuthentication`, `authenticateClient` ve `getBoundProfilePackage` çağrıları vardı. Matching ID'leri `RPROFILE0001`–`RPROFILE0006` olan paketler indirildi. `RPROFILE0000` stok test profiliydi; flag parçası vermedi.

## Çözüm

Her UPP içindeki EF_ADN kayıtlarında `test contact` yerine kısa bir ASCII parçası bulunuyordu. Parçalar matching ID sırasıyla:

| Profil | EF_ADN parçası |
|:--|:--|
| 0001 | `ASIS{` |
| 0002 | `as!S_` |
| 0003 | `1n_T3` |
| 0004 | `lC0_f` |
| 0005 | `r0MN_` |
| 0006 | `oW}` |

Bu sıralama birleştirildiğinde flag oluştu. [solve.py](solve.py) indirilen UPP'lerde ADN alpha-ID alanını ayıklar ve aynı birleştirmeyi yapar.

## Tekrar üretme sınırı

Tarihsel betik, o oturumdaki `/tmp/pysim` istemcisine, test eUICC sertifikalarına ve yarışma servisine bağımlı. Sertifikalar ile özel anahtarlar public arşive alınmadı; dolayısıyla bu repodaki betik tek başına canlı indirme yapmaz. Yukarıdaki parça tablosu, kaydedilmiş çözümün denetlenebilir kısmını verir. Esas yöntem, QR ile profili bulup doğru test kimliğini seçmek ve indirilen paketlerin uygulama verisini incelemektir.
