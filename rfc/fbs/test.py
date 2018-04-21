import os
import json
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
    'meta': {},
    'tables': [],
    'enums': [],
    'services': [],
}

schema_by_uri = {
    'meta': {},
    'uri': {},
}


# idl_parser.cpp: line 2404:
# while (token_ != kTokenEof) { ... }
#
# "namespace"       => ParseNamespace()
# "enum"            => ParseEnum(false, nullptr)
# "union"           => ParseEnum(true, nullptr)
# "root_type"       => SetRootType(name)
# "file_identifier" => file_identifier_
# "file_extension"  => file_extension_
# "attribute"       => known_attributes_[name] = false;
# "rpc_service"     => ParseService()
#                   => ParseDecl()
#

filename = './_build/schema/example.bfbs'
filepath = os.path.abspath(filename)

with open(filepath, 'rb') as f:
    buf = f.read()
    _schema = Schema.GetRootAsSchema(buf, 0)

    schema_meta = {
        'filename': filename,
        'filepath': filepath,
        'file_ident': _schema.FileIdent().decode('utf8'),
        'file_ext': _schema.FileExt().decode('utf8'),
        'root': _schema.RootTable(),
    }

    schema['meta'] = schema_meta
    schema_by_uri['meta'] = schema_meta

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

            num_enum_value_docs = _enum_value.DocumentationLength()
            enum_value_docs = [_enum_value.Documentation(i).decode('utf8').strip() for i in range(num_enum_value_docs)]
            enum_value['docs'] = enum_value_docs

            enum_values.append(enum_value)

        enum['values'] = sorted(enum_values, key=lambda enum_value: enum_value['name'])

        num_enum_docs = _enum.DocumentationLength()
        enum_docs = [_enum.Documentation(i).decode('utf8').strip() for i in range(num_enum_docs)]
        enum['docs'] = enum_docs

        enums.append(enum)

        if enum['name'] in schema_by_uri['uri']:
            raise Exception('unexpected duplicate definition for qualified name "{}"'.format(enum['name']))
        else:
            schema_by_uri['uri'][enum['name']] = enum


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
                'def': 'field',
                'name': _field_name,
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

        num_obj_docs = _obj.DocumentationLength()
        obj_docs = [_obj.Documentation(i).decode('utf8').strip() for i in range(num_obj_docs)]
        obj['docs'] = obj_docs

        objects.append(obj)

        if obj['name'] in schema_by_uri['uri']:
            raise Exception('unexpected duplicate definition for qualified name "{}"'.format(field['name']))
        else:
            schema_by_uri['uri'][obj['name']] = obj


    # iterate over services
    #
    num_services = _schema.ServicesLength()
    services = []
    for i in range(num_services):
        _service = _schema.Services(i)

        service = {
            'def': 'service',
            'name': _service.Name().decode('utf8'),
        }

        num_calls = _service.CallsLength()
        calls = []
        calls_by_name = {}
        for j in range(num_calls):
            _call = _service.Calls(j)

            _call_name = _call.Name().decode('utf8')
            call = {
                'def': 'call',
                'name': _call_name,
                'request': _call.Request().Name().decode('utf8'),
                'response': _call.Response().Name().decode('utf8'),
                #'id': int(_call.Id()),
                #'offset': int(_call.Offset()),
            }

            num_call_docs = _call.DocumentationLength()
            call_docs = [_call.Documentation(i).decode('utf8').strip() for i in range(num_call_docs)]
            call['docs'] = call_docs

            calls.append(call)
            calls_by_name[_call_name] = call

        # service['calls'] = sorted(calls, key=lambda field: field['id'])
        service['calls'] = calls_by_name

        num_service_docs = _service.DocumentationLength()
        service_docs = [_service.Documentation(i).decode('utf8').strip() for i in range(num_service_docs)]
        service['docs'] = service_docs

        services.append(service)

        if service['name'] in schema_by_uri['uri']:
            raise Exception('unexpected duplicate definition for qualified name "{}"'.format(service['name']))
        else:
            schema_by_uri['uri'][service['name']] = service



schema['enums'] = sorted(enums, key=lambda enum: enum['name'])
schema['tables'] = sorted(objects, key=lambda obj: obj['name'])
schema['services'] = sorted(services, key=lambda service: service['name'])


if False:
    if True:
        #pprint(schema)
        pprint(schema_by_uri)
    else:
        pprint(schema_by_uri['meta'])

if False:
    pprint(schema_by_uri['uri']['wamp.proto.Serializer'])
    pprint(schema_by_uri['uri']['com.example.accelstorage.TimeRange'])
    pprint(schema_by_uri['uri']['com.example.accelstorage.AccelSamples'])

if False:
    pprint(schema['services'])


output_filename = './_build/schema/example.json'
output_filepath = os.path.abspath(output_filename)
with open(output_filepath, 'wb') as f:
    data = json.dumps(schema_by_uri, ensure_ascii=False, sort_keys=False, separators=(',',':')).encode('utf8')
    f.write(data)

print('output file written: {}'.format(output_filepath))
