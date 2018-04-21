from pprint import pprint
import flatbuffers

from reflection.Schema import Schema

_BASETYPE_ID2NAME = {
    None: 'Unknown',
    0: 'None',
    1: 'UType',
    2: 'Bool',
    3: 'Byte',
    4: 'UByte',
    5: 'Short',
    6: 'UShort',
    7: 'Int',
    8: 'UInt',
    9: 'Long',
    10: 'ULong',
    11: 'Float',
    12: 'Double',
    13: 'String',
    14: 'Vector',
    15: 'Obj',
    16: 'Union',
}


schema = {
    'tables': None,
    'enums': None,
    'interfaces': None,
}

schema_by_uri = {
}


with open('./_build/schema/example.bfbs', 'rb') as f:
    buf = f.read()
    _schema = Schema.GetRootAsSchema(buf, 0)

    # iterate over enums
    #
    num_enums = _schema.EnumsLength()
    enums = []
    for i in range(num_enums):
        _enum = _schema.Enums(i)
        enum = {
            'def': 'enum',
            'name': _enum.Name().decode('utf8'),
        }
        num_enum_values = _enum.ValuesLength()
        enum_values = []
        for j in range(num_enum_values):
            _enum_value = _enum.Values(j)
            enum_value = {
                'name': _enum_value.Name().decode('utf8'),
            }
            enum_values.append(enum_value)
        
        enum['values'] = sorted(enum_values, key=lambda enum_value: enum_value['name'])
        enums.append(enum)

        if enum['name'] in schema_by_uri:
            raise Exception('unexpected duplicate definition for qualified name "{}"'.format(field['name']))
        else:
            schema_by_uri[enum['name']] = enum


    # iterate over objects (framebuffer structs)
    #
    num_objs = _schema.ObjectsLength()
    objects = []
    for i in range(num_objs):
        _obj = _schema.Objects(i)
        obj = {
            'def': 'table',
            'name': _obj.Name().decode('utf8'),
        }
        num_fields = _obj.FieldsLength()
        fields = []
        fields_by_name = {}
        for j in range(num_fields):
            _field = _obj.Fields(j)
            _field_type = _field.Type()
            _field_index = int(_field_type.Index())
            _field_name = _field.Name().decode('utf8')
            field = {
                # 'name': _field_name,
                'type': {
                    'base_type': _BASETYPE_ID2NAME.get(_field_type.BaseType(), None),
                    'element': _BASETYPE_ID2NAME.get(_field_type.Element(), None),
                    'index': _field_index,
                },
                'id': int(_field.Id()),
                'offset': int(_field.Offset()),
            }
            fields.append(field)
            fields_by_name[_field_name] = field
        
        # obj['fields'] = sorted(fields, key=lambda field: field['id'])
        obj['fields'] = fields_by_name

        objects.append(obj)

        if obj['name'] in schema_by_uri:
            raise Exception('unexpected duplicate definition for qualified name "{}"'.format(field['name']))
        else:
            schema_by_uri[obj['name']] = obj

    # iterate over interfaces
    #
    # FIXME


schema['enums'] = sorted(enums, key=lambda enum: enum['name'])
schema['tables'] = sorted(objects, key=lambda obj: obj['name'])

pprint(schema)
pprint(schema_by_uri)
