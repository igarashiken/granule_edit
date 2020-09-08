#granule 勝田による書き直し
#途中まで作成済み 

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



def granule():
    return 

def f_func():
    return

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
    temp=x<<num
    a=temp&0xffffffff
    b=(temp>>32)&0xffffffff

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


if __name__=="__main__":
    main()