import hashlib

'ychda@qq.com'
print(hashlib.sha256(b"abc").hexdigest())
import struct

def rotr(n, x):
    """循环右移 n bit，32位无符号整数"""
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def Σ0(x):
    return rotr(2, x) ^ rotr(13, x) ^ rotr(22, x)

def Σ1(x):
    return rotr(6, x) ^ rotr(11, x) ^ rotr(25, x)

def σ0(x):
    return rotr(7, x) ^ rotr(18, x) ^ (x >> 3)

def σ1(x):
    return rotr(17, x) ^ rotr(19, x) ^ (x >> 10)

def ch(e, f, g):
    return (e & f) ^ (~e & g)

def maj(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)

# 初始哈希值 H0~H7
H = [
    0x6a09e667,
    0xbb67ae85,
    0x3c6ef372,
    0xa54ff53a,
    0x510e527f,
    0x9b05688c,
    0x1f83d9ab,
    0x5be0cd19,
]

# SHA256 固定64个常量K
K = [
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
    0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
    0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391e8391,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
    0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2,
]

def sha256(data: bytes) -> str:
    msg = bytearray(data)
    orig_len_bits = len(msg) * 8

    # 1. 填充 padding
    msg.append(0x80)
    while (len(msg) * 8) % 512 != 448:
        msg.append(0x00)
    # 末尾附加原始长度(64bit大端)
    msg.extend(struct.pack('>Q', orig_len_bits))

    # 2. 按512bit(64字节)分块处理
    h = H.copy()
    for chunk_start in range(0, len(msg), 64):
        chunk = msg[chunk_start:chunk_start+64]
        # 前16个W
        W = list(struct.unpack('>16L', chunk))
        # 扩展到64个W
        for t in range(16, 64):
            wt = (σ1(W[t-2]) + W[t-7] + σ0(W[t-15]) + W[t-16]) & 0xFFFFFFFF
            W.append(wt)

        a,b,c,d,e,f,g,hh = h

        # 64轮压缩运算
        for t in range(64):
            t1 = (hh + Σ1(e) + ch(e,f,g) + K[t] + W[t]) & 0xFFFFFFFF
            t2 = (Σ0(a) + maj(a,b,c)) & 0xFFFFFFFF

            hh = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFF

        # 叠加到哈希
        h[0] = (h[0] + a) & 0xFFFFFFFF
        h[1] = (h[1] + b) & 0xFFFFFFFF
        h[2] = (h[2] + c) & 0xFFFFFFFF
        h[3] = (h[3] + d) & 0xFFFFFFFF
        h[4] = (h[4] + e) & 0xFFFFFFFF
        h[5] = (h[5] + f) & 0xFFFFFFFF
        h[6] = (h[6] + g) & 0xFFFFFFFF
        h[7] = (h[7] + hh) & 0xFFFFFFFF

    # 转为十六进制字符串
    return ''.join(f"{val:08x}" for val in h)


# 测试
if __name__ == "__main__":
    test_str = b"abc"
    res = sha256(test_str)
    print(res)
    # 预期输出: ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad

