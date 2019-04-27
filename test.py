import decimal, math
l = math.log
e = math.e

print(0x00ffff * 2**(8*(0x1d - 3)) / float(0x0404cb * 2**(8*(0x1b - 3))))
print(l(0x00ffff * 2**(8*(0x1d - 3)) / float(0x0404cb * 2**(8*(0x1b - 3)))))
print(l(0x00ffff * 2**(8*(0x1d - 3))) - l(0x0404cb * 2**(8*(0x1b - 3))))
print(l(0x00ffff) + l(2**(8*(0x1d - 3))) - l(0x0404cb) - l(2**(8*(0x1b - 3))))
print(l(0x00ffff) + (8*(0x1d - 3))*l(2) - l(0x0404cb) - (8*(0x1b - 3))*l(2))
print(l(0x00ffff / float(0x0404cb)) + (8*(0x1d - 3))*l(2) - (8*(0x1b - 3))*l(2))
print(l(0x00ffff / float(0x0404cb)) + (0x1d - 0x1b)*l(2**8))
