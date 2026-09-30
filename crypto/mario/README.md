# Mario · Crypto

**Öz:** Gizli 24 boyutlu altuzay, yayımlanan 64 raporun oluşturduğu 25 boyutlu uzaydan geri çıkarılıyor. Kurtarılan baz, GCM anahtarını türetiyor.

**Doğrulama:** Sağlanan [output.txt](output.txt) üzerinden hesaplanan anahtar AES-GCM etiketini doğruladı ve flag'i açtı.

## Yapı

Problem `GF(16)` üzerinde çalışıyor; indirgenemez polinom `x⁴+x+1`. Gizli *oil* altuzayı 24 boyutlu. Raporların her biri, bu altuzaydan seçilen bir vektöre aynı gizli yönün farklı katlarını ekliyor. Bu yüzden raporların doğrusal zarfı 25 boyuta yükseliyor: `W = O' + <g>`.

Yayımlanan iki kuadratik formu `W` üzerinde kutuplaştırıp iki bilineer matris `M₀` ve `M₁` elde ediyoruz. Çözüm örneğinde bu matrislerin görüntülerinin kesişimi tek boyutlu: `ℓ`. Bu doğrusal fonksiyonun çekirdeği 24 boyutlu `O'` oluyor. Çekirdeğin baz vektörleri tekrar 96 boyutlu kamusal koordinatlara kaldırılıyor.

```text
64 rapor → rank 25'lik W
W üzerindeki iki bilineer form → ortak 1-boyutlu görüntü ℓ
ker(ℓ) → rank 24'lük oil altuzayı
kanonik baz → HKDF("MARIO") → AES-GCM doğrulaması
```

[solve.py](solve.py) bu adımları ve boyut kontrollerini içeriyor. Baz satır indirgemeyle sabit sıraya sokuluyor; bu önemli, çünkü anahtar türetimi bazın bayt dizisine bağlı. Son aşamada `decrypt_and_verify` etiketi doğrulamadan flag kabul edilmiyor.

Sonuç: `ASIS{MARY0___grOe8n3r___8aSi5_chA1L3n9e_Mas7eR3d_r3A1Ly?!!!}`. Bu flag'in doğrulaması yerel kriptografik etiketten geliyor; canlı scoreboard gönderimi kaydı değil.

Çalıştırma için `pycryptodome` gerekir: `python3 solve.py`. [Kaynak üretici](source/mario.py), raporların nasıl hazırlandığını görmek isteyenler içindir.

## Bağımsız matematiksel bakış

[Abdelkad3r'in Mario writeup'ı](https://github.com/Abdelkad3r/ASIS-CTF-Quals-2026/blob/master/Crypto/Mario/README.md) aynı 25 boyutlu sızıntıyı, her kuadratik formun bu uzayda ortak bir doğrusal çarpan taşıması üzerinden türetiyor. Rank-2 polar formların 23 boyutlu çekirdekleri iki farklı form için birleştirilince 24 boyutlu oil uzayı elde ediliyor. Bu, yukarıda kullanılan ortak görüntü/tek boyutlu fonksiyon bakışının eşdeğer ama farklı öğretici bir açıklaması; yazarın kodu bu arşive kopyalanmadı.
