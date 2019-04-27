#Implement mining program of Bitcoin
#Reference:
# Bitcoin Minig: http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html
# Target and Difficulty: https://bitcoin.stackexchange.com/questions/49068/how-to-generate-bitcoin-target-from-difficulty
# Calculate difficulty: https://bitcoin.stackexchange.com/questions/5838/how-is-difficulty-calculated

import hashlib, time, struct, codecs

def mine(ver, prevHash, merkleRoot, timeI, bits):
    nonce = 0x7c1bac1d
    #nonce = 0x0
    encodeVer = struct.pack("<L", ver)
    encodePrevHash = codecs.decode(prevHash, "hex")[::-1]
    encodeMerkleRoot = codecs.decode(merkleRoot, "hex")[::-1]
    encodeTime = struct.pack("<L", int(time.mktime(time.strptime(timeI, "%H:%M:%S_%m-%d-%Y"))))
    print(time.strptime(timeI, "%H:%M:%S_%m-%d-%Y"))
    encodeBits = struct.pack("<L", bits)
    print(bits)
    encodeNonce = struct.pack("<L", nonce)
    print(nonce)
    hashInput = encodeVer + encodePrevHash + encodeMerkleRoot + encodeTime + encodeBits + encodeNonce
    print('hashInput', hashInput)

    # Difficulty: https://en.bitcoin.it/wiki/Difficulty
    # Hexademal prefix: https://zh.wikipedia.org/wiki/%E5%8D%81%E5%85%AD%E8%BF%9B%E5%88%B6
    #Bits has 8 digits in hexademal representation which is 32 binary bits long
    #For eamample: in genesis block, the bits is "1d00ffff". But in C++, JAVA, Python it would add '0x' or '0X' to represent a hexademal number, so '1d00ffff' will be represented as '0x1d00ffff'
    #For '0x1d00ffff', '0x' is prefix for Python interpreter to read. '1d' represnts exponent. '00ffff' represents significant(mantissa). Actually, '1d00ffff' is a base-256 scientific notation.

    # Bitcoin official Doc: https://bitcoin.org/en/developer-reference#target-nbits
    #bits is an integer number, hex() will transfer number to hexademal notation, bin() will transfer number to binary notation
    #As the same as bits * 2^24 which drops 6 hexademal digits.
    #For example: '1d00ffff' would become '1d'
    exp = bits >> 24

    #Remain the last 6 hexademal digits of bits.
    #For example: '1d00ffff' would become 'ffff'
    sig = bits & 0xffffff

    #sig * (1<<(8*(exp - 3))) is the same as: sig * 256^(exp - 3), it will add 2*(exp - 3) hexademal 0
    #'%064x' % will fill leading 0 until the number achieve 64 hexademal digits
    threshold = '%064x' % (sig * (1 << 8*(exp - 3)))

    #We get the target the hash value of block must be smaller than the target which is the variable 'target_str'
    encodeThreshold = codecs.decode(threshold, "hex")

    print(threshold)
    print("00000000ffff0000000000000000000000000000000000000000000000000000")
    print(encodeThreshold)


    """Mining"""
    while nonce < 0x100000000:
        hash = (hashlib.sha256(hashlib.sha256(hashInput).digest()).digest())[::-1]

        if hash < encodeThreshold:
            out = codecs.encode(hash, "hex")
            print('Nonce: ', hex(nonce), '  Hash: ', out)
            return out

        nonce+=1
        encodeNonce = struct.pack("<L", nonce)
        hashInput = encodeVer + encodePrevHash + encodeMerkleRoot + encodeTime + encodeBits + encodeNonce




version = 1
prev_block = "0000000000000000000000000000000000000000000000000000000000000000"
merkle_root = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
timestamp = "2:15:05_01-04-2009"
bits = 0x1d00ffff

mine(version, prev_block, merkle_root, timestamp, bits)
#Nonce:  0x7c2bac1d   Hash:  b'000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'
#nonce = 0x7c2bac1d   hash = b'000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'
