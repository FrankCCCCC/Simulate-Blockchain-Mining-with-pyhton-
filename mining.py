# Modified from GitHub: https://gist.github.com/turunut/7857bd34bac37a04a91a91ee9ea33520

import hashlib, struct, codecs, time, random

def mine(version, prev_block, merkle_root, timestamp, bits, debug_mode, hint = 0x0):

    time_int = int(time.mktime(time.strptime(timestamp,"%Y-%m-%d %H:%M:%S")))

    # Difficulty: https://en.bitcoin.it/wiki/Difficulty
    exp = bits >> 24
    mant = bits & 0xffffff
    target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
    target_str = codecs.decode(target_hexstr, "hex")
    
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


    while nonce < 0x100000000:
        
        encoded_nonce = struct.pack("<L", nonce)
        header = encoded_version+encoded_prev_block+encoded_merkle_root+encoded_time_int+encoded_bits+encoded_nonce

        # Double-SHA-256
        hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()
        
        #print( 'nonce =', hex(nonce), '    hash =', codecs.encode(hash[::-1], "hex"))

        if hash[::-1] < target_str:
            print( 'nonce =', hex(nonce), '    hash =', codecs.encode(hash[::-1], "hex"))
            break
        
        nonce += 1
        

        if('slow' in debug_mode):
            time.sleep(0.5)


    print('Find the valid nonce... End mining...')
    tEnd = time.time()

    if('time' in debug_mode):
        print('\nMining time:', tEnd - tStart, 'sec')

