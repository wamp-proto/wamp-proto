SERMAP = {
   1: 'json',
   2: 'msgpack'
}

## map serializer / max. msg length to RawSocket handshake request or success reply (2nd octet)
##
for ser in SERMAP:
   for l in range(16):
      octet_2 = (l << 4) | ser
      print("serializer: {}, maxlen: {} => 0x{:02x}".format(SERMAP[ser], 2 ** (l + 9), octet_2))


print("-" * 80)

## map RawSocket handshake request (2nd octet) to serializer / max. msg length
##
for i in range(256):
   ser_id = i & 0x0f
   if ser_id:
      ser = SERMAP.get(ser_id, 'currently undefined')
      maxlen = 2 ** ((i >> 4) + 9)
      print("{:02x} => serializer: {}, maxlen: {}".format(i, ser, maxlen))
   else:
      print("fail the connection: illegal serializer value")

print("-" * 80)

ERRMAP = {
   0: "serializer unsupported",
   1: "maximum message length unacceptable",
   2: "use of reserved bits (unsupported feature)",
   3: "maximum connection count reached"
}

## map error to RawSocket handshake error reply (2nd octet)
##
for err in ERRMAP:
   octet_2 = err << 4
   print("error: {} => 0x{:02x}").format(ERRMAP[err], err)

print("-" * 80)

## map RawSocket handshake reply (2nd octet)
##
for i in range(256):
   ser_id = i & 0x0f
   if ser_id:
      ## verify the serializer is the one we requested! if not, fail the connection!
      ser = SERMAP.get(ser_id, 'currently undefined')
      maxlen = 2 ** ((i >> 4) + 9)
      print("{:02x} => serializer: {}, maxlen: {}".format(i, ser, maxlen))
   else:
      err = i >> 4
      print("error: {}".format(ERRMAP.get(err, 'currently undefined')))
