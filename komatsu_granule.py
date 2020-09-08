#GRANULE
plaintext=0000000000000000000000000000000000000000000000000000000000000000 #64bit

###pt1 pt0 32bitsに分割
pt1=(plaintext>>32)&0xffffffff
pt0=plaintext&0xffffffff

# Permutation sbox
def ps(p):
    
     pt=[]　#4bit単位でリストに格納（最上位がindex0になるよう）
     for i in range(8):
        y=(p>>(i*4))&0xf
        pt.insert(0,y)
        
     pt[4],pt[0],pt[3],pt[1],pt[6],pt[2],pt[7],pt[5] =  pt[0],pt[1],pt[2],pt[3],pt[4],pt[5],pt[6],pt[7]
     
     s=[0xe,0x7,0x8,0x4,0x1,0x9,0x2,0xf,0xc5,0xa,0xb,0x0,0x6,0xc,0xd,0x3]
     for j in range(8):
        pt[j]=s[pt[j]]
    ###リストからビット列になおす###
     a=pt[7]
     b=pt[6]<<4
     c=pt[5]<<8
     d=pt[4]<<12
     e=pt[3]<<16
     f=pt[2]<<20
     g=pt[1]<<24
     h=pt[0]<<28
     ps=a^b^c^d^e^f^g^h
     return ps

#shift
def shift(p):
    ps2=((p<<2)&0xffffffff)^(p>>30) #巡回シフトを実現　  <<<2
    ps7=(p>>7)^((p<<25)&0xffffffff)                  # >>>7
    #plaintext after shift
    psh=ps2^ps7
    return psh



######key_schedule######
key=0x00000000000000000000000000000000 #128bits
s=[0xe,0x7,0x8,0x4,0x1,0x9,0x2,0xf,0x5,0xa,0xb,0x0,0x6,0xc,0xd,0x3]
rk=[]
for i in range(32):
    rkey=key&0xffffffff #32bits取り出し
    rk.append(rkey)　　#リストに格納
    ##鍵の更新
    key=((key<<31)&0xffffffffffffffffffffffffffffffff)^(key>>97)  ###31shift
    a=key&0xf　#0123bitをsboxに
    b=s[a]
    c=(key>>4)&0xf　#4567bitをsboxに
    d=s[c]
    e=key^(i<<66)　#66~70とカウンターxor
    f=(e>>8)<<8    #0~7bitを0にする
    key=(f^b)^(d<<4)


def main (p1,p0):
    for i in range(32):
        pps=ps(p1)
        print("pps=",hex(pps))
        pf=shift(pps)
        print("pf=",bin(pf))
        pxo=pf^p0^rk[i]
        p0=p1
        p1=pxo
        print(i,"p1=",hex(p1),"p0=",hex(p0))
    return p1,p0

p0_out,p1_out = main(pt1,pt0)
print(hex(p1_out),hex(p0_out))
