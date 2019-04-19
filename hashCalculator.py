#!/usr/bin/python

from binascii import unhexlify
from hashlib import sha256
import json
#import urllib2
import sys

#convert into little endian format
def littleEndian(string):
	splited = [str(string)[i:i + 2] for i in range(0, len(str(string)), 2)]
	splited.reverse()
	return "".join(splited)

def littleEndianNonce(string):
	splited = [str(string)[i:i + 2] for i in range(0, len(str(string)), 2)]
	splited.reverse()
	splited = "".join(splited)

	#print("Splited", splited)

	while len(splited) < 8:
		splited = "0" + splited
		#print("Splited", splited)
	#print("Splited Ouput", splited)
	return "".join(splited)

helpMessage = 'Please give arguments to read the block data\nTo read the block as a json file\n-f <fileName>\nTo read the block from a url as a json body\n-i <url>\n'
"""
if (len(sys.argv) < 3):
	print(helpMessage)
	sys.exit()
elif sys.argv[1] == '-f':
	response = json.load(open(sys.argv[2]))
#elif sys.argv[1] == '-i':
	#response = json.loads(urllib2.urlopen(sys.argv[2]).read())
"""
version = '01000000'
little_endian_previousHash = littleEndian("0000000000000000000000000000000000000000000000000000000000000000")
little_endian_merkleRoot = littleEndian("4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b")
little_endian_time = littleEndian(hex(1231006505)[2:])
little_endian_difficultyBits = littleEndian(hex(486604799)[2:])
little_endian_nonce = littleEndianNonce(hex(2083236893)[2:])

#append
header = version + little_endian_previousHash + little_endian_merkleRoot + little_endian_time + little_endian_difficultyBits + little_endian_nonce

header = unhexlify(header)
#sent hash by the miner
Responsehash = littleEndian("000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")
Responsehash = Responsehash[::-1]
#calculated hash
CalculatedHash = sha256(sha256(header).digest()).hexdigest()
CalculatedHash = CalculatedHash[::-1]

#print(type(CalculatedHash))
nonce = 2083236893
bits = str(0x1d00ffff)
prefix = str("0000000000");

while(prefix not in CalculatedHash and nonce < 2083236899):
	print("NONCE ", nonce)
	print("HASH ", CalculatedHash)
	little_endian_nonce1 = littleEndian(hex(nonce)[2:])

	header = version + little_endian_previousHash + little_endian_merkleRoot + little_endian_time + little_endian_difficultyBits + little_endian_nonce1
	header = unhexlify(header)
	CalculatedHash = sha256(sha256(header).digest()).hexdigest()
	CalculatedHash = CalculatedHash[::-1]
	print("CALCULATEHASH", CalculatedHash)
	nonce = nonce + 1


print("BITS ", bits)
print("CALCULATEHASH", CalculatedHash)
print("RESPONSEHASH", Responsehash)

#verify the hash is smaller than the target
solved = 'Hash is smaller than the target' if Responsehash <= little_endian_difficultyBits else 'Hash is larger than the target'
print(solved)
#Equality of the calculated and received hashes
state = 'Hash of the block is acceptable.' if Responsehash == CalculatedHash else 'Hash of the block is not acceptable.'
print(state)
