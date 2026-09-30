R=(1<<128)|0x87
def mul(x,y):
    r=0
    for i in range(127,-1,-1):
        if (x>>i)&1: r^=y
        y<<=1
        if y>>128: y^=R
    return r
def inv(a):
    e=(1<<128)-2; base=a; acc=1
    while e:
        if e&1: acc=mul(acc,base)
        base=mul(base,base); e>>=1
    return acc
i2=lambda x:int.from_bytes(x,'big')
b2=lambda x:x.to_bytes(16,'big')
