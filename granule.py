#granule 勝田による書き直し
#途中まで作成済み 
#鍵は128ビットを想定

def main():
    ##s_layer test
    #import random
    ##xを32ビットのランダム値に設定
    #x=random.randint(0,0xffffffff)
    #print( "0x"+format(x, '08x'))
    #y=s_layer(x)
    #print( "0x"+format(y, '08x'))

    
    #p_layer test
    #import random
    ##xを32ビットのランダム値に設定
    #x=random.randint(0,0xffffffff)
    #print( "0x"+format(x, '08x'))
    #y=p_layer(x)
    #print( "0x"+format(y, '08x'))
    

    #left_shift test
    #import random
    ##xを32ビットのランダム値に設定
    #x=random.randint(0,0xffffffff)
    #print( "0b"+format(x, '032b'))
    #y=left_shift(x,2)
    #print( "0b"+format(y, '032b'))
    

    ##rp_layer test
    #x=0x10000000
    #print( "0b"+format(x, '032b'))
    #y=rp_layer(x)
    #print( "0b"+format(y, '032b'))
    
    plain_text=0x0000000000000000
    mas_key=0x00000000000000000000000000000000 
    rk=key_sch(mas_key)

    cipher_text=granule(plain_text,rk)
    print( "0x"+format(cipher_text, '016x'))



def granule(plain_text,rk):
    #plain_textは64ビット値
    #leftが左側の値、rightが右側の値を示す
    left=(plain_text>>32)&0xffffffff
    right=(plain_text)&0xffffffff

    for r in range(32):
        temp=left
        left=f_func(temp)^rk[r]^right
        right=temp
        print("%dround output" % (r))
        print( "left : 0x"+format(left, '08x'))
        print( "right : 0x"+format(left, '08x'))
        print("")

    
    #right と left を結合する
    cipher_text=(left<<32) ^ right

    return cipher_text

def f_func(x):
    #F関数を表す
    #xが入力(32ビット値)
    a=p_layer(x)
    b=s_layer(a)
    y=rp_layer(b)
    #yが出力(32ビット値)
    return y

def p_layer(x):
    #int型変数xが引数 → 入力を表す
    #int型変数yが戻り値 → 出力を表す
    
    #yを=0で初期化
    y=0

    #ニブルごとの変換表
    #(例 0ニブル目 → p_table[0] = 4ニブル目に移動)
    p_table=[4,0,3,1,6,2,7,5]
    for i in range(8):
        #変数tempにxのiニブル目を代入
        temp=(x>>(4*i))&0xf

        #tempをp_tableによって転置させ、つなげていく
        #y^=～  →  y=y^～
        y^=temp<<(4*p_table[i])

    return y

def s_layer(x):
    #int型変数xが引数 → 入力を表す
    #int型変数yが戻り値 → 出力を表す
    
    #yを=0で初期化
    y=0

    #s-boxの変換表
    #      0x0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
    s_box=[0xe,0x7,0x8,0x4,0x1,0x9,0x2,0xf,0x5,0xa,0xb,0x0,0x6,0xc,0xd,0x3]

    for i in range(8):
        #変数tempにxのiニブル目を代入
        temp=(x>>(4*i))&0xf

        #tempをs-boxに通して、つなげていく
        #y^=～  →  y=y^～
        y^=s_box[temp]<<(4*i)

    return y

def left_shift(x,num):
    #32ビット値における左ビット巡回シフト
    #int型変数xが引数 → 入力を表す
    #int型変数numが引数 → 何ビット左に動かすかを表す
    #int型変数yが戻り値 → 出力を表す
    
    #yを=0で初期化
    y=0

    #詳細図はgithubに載せておきます
    #https://github.com/igarashiken/granule_edit/blob/master/pic/bit_lotate.png
    temp=x<<num
    a=temp&0xffffffff
    b=(temp>>32)&0xffffffff

    #aとbを結合する
    y=a^b
    return y

def left_shift_128(x,num):
    y=0

    #詳細図はgithubに載せておきます
    #https://github.com/igarashiken/granule_edit/blob/master/pic/bit_lotate.png
    temp=x<<num
    a=temp&0xffffffffffffffffffffffffffffffff
    b=(temp>>128)&0xffffffffffffffffffffffffffffffff

    #aとbを結合する
    y=a^b
    return y

def rp_layer(x):
    #int型変数xが引数 → 入力を表す
    #int型変数yが戻り値 → 出力を表す

    #yを=0で初期化
    y=0

    #右7ビット巡回シフトは、32ビット値なら左25ビット巡回シフト
    y=left_shift(x,2)^left_shift(x,25)
    return y

def key_sch(mas_key):
    #mas_keyはマスターキー　秘密鍵を示す
    #res_keyはレジスタとしてのキーを示す
    res_key=mas_key
    #rkは段鍵が入ったリストを示す
    rk=[]

    #s-boxの変換表
    #      0x0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
    s_box=[0xe,0x7,0x8,0x4,0x1,0x9,0x2,0xf,0x5,0xa,0xb,0x0,0x6,0xc,0xd,0x3]

    for r in range(32):
        #下位32ビットの抽出,リストへの追加
        rk.append(res_key&0xffffffff)
        #左31ビットローテート
        res_key=left_shift_128(res_key,31)
        #下位8ビット(2ニブル)のS-Box変換
        res_key=(res_key&0xffffffffffffffffffffffffffffff00) ^ s_box[(res_key>>4)&0xf]<<4 ^ s_box[(res_key)&0xf]
        #iのxor
        res_key^=r<<66
    
    return rk


if __name__=="__main__":
    main()