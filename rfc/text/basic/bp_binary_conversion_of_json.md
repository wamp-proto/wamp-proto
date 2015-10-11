# Binary conversion of JSON Strings

Binary data follows a convention for conversion to JSON strings.

A **byte array** is converted to a **JSON string** as follows:

1. convert the byte array to a Base64 encoded (host language) string
2. prepend the string with a `\0` character
3. serialize the string to a JSON string

*Example*

Consider the byte array (hex representation):

{align="left"}
        10e3ff9053075c526f5fc06d4fe37cdb

This will get converted to Base64

{align="left"}
        EOP/kFMHXFJvX8BtT+N82w==

prepended with `\0`

{align="left"}
        \x00EOP/kFMHXFJvX8BtT+N82w==

and serialized to a JSON string

{align="left"}
        "\\u0000EOP/kFMHXFJvX8BtT+N82w=="

A **JSON string** is unserialized to either a **string** or a **byte array** using the following procedure:

1. Unserialize a JSON string to a host language (Unicode) string
2. If the string starts with a `\0` character, interpret the rest (after the first character) as Base64 and decode to a byte array
3. Otherwise, return the Unicode string

Below are complete Python and JavaScript code examples for conversion between byte arrays and JSON strings.

## Python

Here is a complete example in Python showing how byte arrays are converted to and from JSON:

{align="left"}
        ```python
        <CODE BEGINS>

        import os, base64, json, sys, binascii
        PY3 = sys.version_info >= (3,)
        if PY3:
           unicode = str

        data_in = os.urandom(16)
        print("In:   {}".format(binascii.hexlify(data_in)))

        ## encoding
        encoded = json.dumps('\0' + base64.b64encode(data_in).
                                              decode('ascii'))

        print("JSON: {}".format(encoded))

        ## decoding
        decoded = json.loads(encoded)
        if type(decoded) == unicode:
           if decoded[0] == '\0':
              data_out = base64.b64decode(decoded[1:])
           else:
              data_out = decoded

        print("Out:  {}".format(binascii.hexlify(data_out)))

        assert(data_out == data_in)

        <CODE ENDS>
        ```

## JavaScript

Here is a complete example in JavaScript showing how byte arrays are converted to and from JSON:

{align="left"}
        ```javascript
        <CODE BEGINS>

        var data_in = new Uint8Array(new ArrayBuffer(16));

        // initialize test data
        for (var i = 0; i < data_in.length; ++i) {
           data_in[i] = i;
        }
        console.log(data_in);

        // convert byte array to raw string
        var raw_out = '';
        for (var i = 0; i < data_in.length; ++i) {
           raw_out += String.fromCharCode(data_in[i]);
        }

        // base64 encode raw string, prepend with \0
        // and serialize to JSON
        var encoded = JSON.stringify("\0" + window.btoa(raw_out));
        console.log(encoded); // "\u0000AAECAwQFBgcICQoLDA0ODw=="

        // unserialize from JSON
        var decoded = JSON.parse(encoded);

        var data_out;
        if (decoded.charCodeAt(0) === 0) {
           // strip first character and decode base64 to raw string
           var raw = window.atob(decoded.substring(1));

           // convert raw string to byte array
           var data_out = new Uint8Array(new ArrayBuffer(raw.length));
           for (var i = 0; i < raw.length; ++i) {
              data_out[i] = raw.charCodeAt(i);
           }
        } else {
           data_out = decoded;
        }

        console.log(data_out);

        <CODE ENDS>
        ```