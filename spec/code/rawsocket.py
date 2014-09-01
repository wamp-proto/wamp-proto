SERMAP = {
   0: 'json',
   1: 'msgpack'
}

## map RawSocket handshake 2nd octet to serializer / max. msg length
##
for i in range(256):
   ser = SERMAP.get(i & 0x0f, 'currently undefined')
   maxlen = 2 ** ((i >> 4) + 9)
   print("{:02x} => serializer: {}, maxlen: {}".format(i, ser, maxlen))

## map serializer / max. msg length to RawSocket handshake 2nd octet
##
for ser in SERMAP:
   for l in range(16):
      b = (l << 4) | ser
      maxlen = 2** (l + 9)
      print("serializer: {}, maxlen: {} => {:02x}".format(SERMAP[ser], maxlen, b))
