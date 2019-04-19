from mining import mine


hyperlink = 'https://btc.com/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'
height = '#0'

version = 1
prev_block = "0000000000000000000000000000000000000000000000000000000000000000"
merkle_root = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
timestamp = "2009-01-04 2:15:05"
bits = 0x1d00ffff


mine(version, prev_block, merkle_root, timestamp, bits, debug_mode = ('fast'), hint = 0x7c2bac1d)
