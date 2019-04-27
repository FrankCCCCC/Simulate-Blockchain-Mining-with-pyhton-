# Modified from GitHub: https://gist.github.com/turunut/7857bd34bac37a04a91a91ee9ea33520
#Implement mining program of Bitcoin
#Reference:
# Bitcoin Minig: http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html
# Target and Difficulty: https://bitcoin.stackexchange.com/questions/49068/how-to-generate-bitcoin-target-from-difficulty
# Calculate difficulty: https://bitcoin.stackexchange.com/questions/5838/how-is-difficulty-calculated

import hashlib, struct, codecs, time, random

def mine(version, prev_block, merkle_root, timestamp, bits, debug_mode, hint = 0x0):

    time_int = int(time.mktime(time.strptime(timestamp,"%Y-%m-%d %H:%M:%S")))

    # Difficulty: https://en.bitcoin.it/wiki/Difficulty
    # Hexademal prefix: https://zh.wikipedia.org/wiki/%E5%8D%81%E5%85%AD%E8%BF%9B%E5%88%B6
    #Bits has 8 digits in hexademal representation which is 32 binary bits long
    #For eamample: in genesis block, the bits is "1d00ffff". But in C++, JAVA, Python it would add '0x' or '0X' to represent a hexademal number, so '1d00ffff' will be represented as '0x1d00ffff'
    #For '0x1d00ffff', '0x' is prefix for Python interpreter to read. '1d' represnts exponent. '00ffff' represents significant(mantissa). Actually, '1d00ffff' is a base-256 scientific notation.
    print('bits: ', bits)
    print('Hex bits: ', hex(bits))
    print('Binary bits: ', bin(bits))

    # Bitcoin official Doc: https://bitcoin.org/en/developer-reference#target-nbits
    #bits is an integer number, hex() will transfer number to hexademal notation, bin() will transfer number to binary notation
    #As the same as bits * 2^24 which drops 6 hexademal digits.
    #For example: '1d00ffff' would become '1d'
    exp = bits >> 24
    print('exp: ', exp)
    print('Hex exp: ', hex(exp))
    print('Binary exp: ', bin(exp))
    #Remain the last 6 hexademal digits of bits.
    #For example: '1d00ffff' would become 'ffff'
    mant = bits & 0xffffff
    print('mant: ', mant)
    print('Hex mant: ', hex(mant))
    print('Binary mant: ', bin(mant))
    #mant * (1<<(8*(exp - 3))) is the same as: mant * 256^(exp - 3), it will add 2*(exp - 3) hexademal 0
    #'%064x' % will fill leading 0 until the number achieve 64 hexademal digits
    target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
    print('Target before padding leading 0: ')
    print('Target of mant * (1<<(8*(exp - 3))): ', hex(mant * (1<<(8*(exp - 3)))))
    print('Target of mant * 256**(0x1d - 3):    ', hex(mant * 256**(0x1d - 3)))
    print('Correct Target:                      ', '0xFFFF0000000000000000000000000000000000000000000000000000')
    print('Target after padding leading 0: ')
    print(target_hexstr)

    print()

    #We get the target the hash value of block must be smaller than the target which is the variable 'target_str'
    target_str = codecs.decode(target_hexstr, "hex")
    print('Target after decode: ', target_str)

    #nonce = random.randint(0,0x100000000)    # start from a random number
    nonce = 0x0

    # Use "hint" to make mining faster
    if(hint != 0x0):
        count = 100000
        nonce = hint-count

    print('Start mining...')
    tStart = time.time()

    # Totally 80 bytes (4B+32B+32B+4B+4B+4B) (in little indian)
    encoded_version = struct.pack("<L", version)
    encoded_prev_block = codecs.decode(prev_block, "hex")[::-1]
    encoded_merkle_root = codecs.decode(merkle_root, "hex")[::-1]
    encoded_time_int = struct.pack("<L", time_int)
    encoded_bits = struct.pack("<L", bits)
    encoded_nonce = struct.pack("<L", nonce)
    h = encoded_version+encoded_prev_block+encoded_merkle_root+encoded_time_int+encoded_bits+encoded_nonce

    print()
    originalNonce = nonce;
    print('original Nonce: ', originalNonce)
    print('Hint: ', hint)

    while nonce < 0x100000000:

        encoded_nonce = struct.pack("<L", nonce)
        header = encoded_version+encoded_prev_block+encoded_merkle_root+encoded_time_int+encoded_bits+encoded_nonce

        # Double-SHA-256
        hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()

        #print( 'nonce =', hex(nonce), '    hash =', codecs.encode(hash[::-1], "hex"))

        if hash[::-1] < target_str:
            print('original Nonce: ', originalNonce)
            print('nonce: ', nonce)
            print('target_str', target_str)
            print( 'nonce =', hex(nonce), '    hash =', codecs.encode(hash[::-1], "hex"))
            break

        nonce += 1


        if('slow' in debug_mode):
            time.sleep(0.5)


    print('Find the valid nonce... End mining...')
    tEnd = time.time()

    if('time' in debug_mode):
        print('\nMining time:', tEnd - tStart, 'sec')
