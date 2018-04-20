import flatbuffers

from reflection.Schema import Schema


with open('./_build/schema/example.bfbs', 'rb') as f:
    buf = f.read()
    schema = Schema.GetRootAsSchema(buf, 0)
    num_objs = schema.ObjectsLength()
    print('objects: {}'.format(num_objs))
    for i in range(num_objs):
        obj = schema.Objects(i)
        name = obj.Name().decode('utf8')
        print('object: {}'.format(name))
