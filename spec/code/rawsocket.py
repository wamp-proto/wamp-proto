SERMAP = {
   1: 'json',
   2: 'msgpack'
}

## map serializer / max. msg length to RawSocket handshake 2nd octet
##
for ser in SERMAP:
   for l in range(16):
      octet_2 = (l << 4) | ser
      print("serializer: {}, maxlen: {} => 0x{:02x}".format(SERMAP[ser], 2 ** (l + 9), octet_2))


## map RawSocket handshake 2nd octet to serializer / max. msg length
##
for i in range(256):
   octet_2 = i & 0x0f
   if octet_2:
      ser = SERMAP.get(octet_2, 'currently undefined')
      maxlen = 2 ** ((i >> 4) + 9)
      print("{:02x} => serializer: {}, maxlen: {}".format(i, ser, maxlen))
   else:
      pass

