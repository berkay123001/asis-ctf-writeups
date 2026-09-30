# Revenant Buddy · Pwn

**Öz:** Sekiz register'lı VM, gizli oturum değerini kullanmaya izin vermeyen türler tanımlıyor; fakat kopyalama opcode'u gizli değeri ve hash'ini dışa aktarılabilir türe dönüştürüyor.

**Doğrulama:** Uzak worker `OK ASIS{8bf2fd2a3f7eecec5f5fab1861e51c579975ba45}` döndürdü.

## Programın beklediği koşul

Worker `RUN <hex>` ile en fazla 64 adet little-endian 32 bit sözcük alıyor. Girdi önce sürüme özgü S-box ve tabloyla çözülüyor. Programın başında magic, sonunda `halt` gerekiyor. `r7` rastgele üretilen sekiz baytlık oturum sırrıyla ve tür 2 ile başlıyor. `export` için ise sır ve `mixhash(sır)` değerlerinin ikisinin de tür 1 register'larda olması gerekiyor.

```text
r7: secret, type 2
hash(r7): value, type 4
export(secret, hash): both inputs must be type 1
```

`0xd9` komutu `((imm+1)&0x7fff) * src2 ^ src1` hesaplıyor ve hedefe tür 1 veriyor. `src2` sıfır değerli `r0`, `imm=0x7fff` seçilince çarpan sıfır oluyor: sonuç doğrudan `src1`. Böylece tür 2'deki sır ve tür 4'teki hash, değerleri bozulmadan tür 1 register'lara taşınabiliyor.

## Minimal VM programı

```text
magic
r1 = mixhash(r7)           # 0x8d
r2 = copy(r7, r0)          # 0xd9, type 1
r3 = copy(r1, r0)          # 0xd9, type 1
export(r2, r3)             # 0x9e
halt                       # 0xdc
```

[solve.py](solve.py) sözcükleri oluşturuyor, worker'ın obfuscation adımının tersini hesaplıyor ve `RUN` protokolüne gönderiyor. Ofsetleri okumak için aynı sürüm [revenant-worker](Revenant-Buddy/revenant-worker) dosyası gerekir. Bu çözümde asıl hata, `0xd9` sonrası atanan türün değerin kökenini korumamasıdır.
