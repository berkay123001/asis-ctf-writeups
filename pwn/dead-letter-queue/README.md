# Dead Letter Queue · Pwn

**Öz:** Dolu dairesel kuyruğun `head == tail` durumu boş kuyruk gibi taranıyor. Serbest bırakılan slotun kuyruk kaydı kalıyor; yeniden ayrılan slot, warden denetiminden geçmeden worker'a gönderilebiliyor.

**Doğrulama:** Arşivdeki exploit önce yerel test flag'ini, ardından canlı hedeften `ASIS{5bde7fad6ec7676208a5d225f4230997ef81f0af}` değerini aldı.

## Üç süreçli yapı

`relay` istemci protokolü ve slotları, `warden` izin verilen mesaj türlerini, `worker` ise VM ve dosya işlemlerini yönetiyor. Kuyruk altı kayıt tutuyor. Altı meşru mesajla dolunca `head=tail=0` olur; ancak `count=6` olduğu için kuyruk boş değildir.

Slot serbest bırakma yolu, `tail >= head` iken `[head, tail)` aralığını tarıyor. Bu aralık dolu kuyrukta sıfır uzunlukta kalınca hiçbir kuyruk kaydı silinmiyor. Böylece serbest slot tekrar ayrılabiliyor, eski kuyruk kaydı ise hâlâ o slotu işaret ediyor.

## Çözüm zinciri

1. Altı adet izinli `0x69` mesajı warden'dan geçirip kuyruğu doldur.
2. İlk üç slotu serbest bırak; kuyruktaki referansları koru.
3. İlk slotu `0x92` VM mesajıyla yeniden doldur. `0xb9` opcode'u worker'ın süreç sırrını sızdırır.
4. Bu sırla `/flag` mesajı için MAC ve kontrol değerini hesapla.
5. İkinci slotta VM'nin `0x96` yoluyla beklenen token'ı kur.
6. Üçüncü slotu `0xad` dosya mesajıyla yeniden doldur; `drain` worker çıktısını getirir.

Asıl yetki atlaması 2. adımda oluşur: `drain`, kuyruktaki kaydın bugün hâlâ warden'ın onayladığı aynı içerik olup olmadığını yeniden kontrol etmiyor. Sonraki adımlar bu yetki atlamasını flag okumasına çeviriyor.

[solve.py](solve.py), çözüm oturumunda `/tmp/dlq_exp.py` olarak tutulan betiğin arşivlenmiş kopyasıdır. Gerekli bağımlılık `pwntools`; betik iki argüman olarak host ve port bekler. İkili artefaktlar: [relay](relay), [warden](warden), [worker](worker).

## Bağımsız yaklaşım

[trefor'un Dead Letter writeup'ı](https://github.com/hax1ng/ASIS-CTF-Quals-2026/blob/main/pwn/dead-letter/README.md) aynı kuyrukta farklı bir sınır durumunu kullanıyor: bizim tam dolu `head == tail, count == 6` durumumuz yerine sarmış kuyrukta iptal edilen kaydın eksik aralık taramasından kaçmasını gösteriyor. İki anlatımın ortak kökü, kuyruğun tuttuğu slot numarasının serbest bırakma/yeniden kullanma sonrasında da yetkili kabul edilmesi. Dış betik burada kendi exploit'imizin parçası olarak sayılmıyor.
