# Store API

## Products API

### Deleting Products

To delete an existing product from the store, call the **procedure**

	com.example.store.delete_product(product_id, cascade) -> total_deleted

 * The procedure takes a mandatory positional argument `product_id` to provide the ID of the product to be deleted.
 * An optional `cascade` positional argument allows you to extend the deletion to any dependend objects.
 * When successful, the procedure will return the total number of deleted items (including those deleted due to cascading the deletion).
 * When successful, the procedure will also publish a notification to the **topic** `com.example.store.on_delete_product`

#### Example

A call of `com.example.store.delete_product` with `args`


```javascript
[100, true]
```

will either return successfully with a result having `args`:

```javascript
[3]
```

indicating there were 3 items deleted in total.

Or the call returns with an error `com.example.error.no_such_product` having `args`:

```javascript
["no product with ID 100"]
```

When the call succeeds, an event `com.example.store.on_delete_product` with `args`

```javascript
[100]
```

would have been published.


#### Procedure [**com.example.store.delete_product**]

Here is the complete signature of above procedure:

```javascript
{
	"uri": "com.example.store.delete_product",
   	"type": "procedure",
	"help": "Delete an existing product. When successful, a notification is sent.",
	"args": [
		{
			"label": "product_id",
			"types": ["int"],
			"help": "The product to be deleted."
		},
		{
			"label": "cascade",
			"types": ["bool"],
			"optional": true,
			"help": "Flag to activate cascaded delete, which deletes any dependent objects also."
		}
	],
	"result": {
		"args": [{"label": "total_deleted", "types": ["int"]}]
	},
	"errors": {
		"com.example.error.no_such_product": {
			"help": "The product that was requested to be deleted does not exist.",
			"args": [{"label": "error_message", "types": ["string"]}]
		}
	},
    "events": {
		"com.example.store.on_delete_product": {
        }
    }
}
```

#### Topic [**com.example.store.on_delete_product**]

Whenever a previously existing product was successfully deleted, the following event will be published:

```javascript
{
	"uri": "com.example.store.on_delete_product",
   	"type": "topic",
	"help": "Fired when a product was deleted.",
	"args": [
		{
			"label": "product_id",
			"types": ["int"],
			"help": "The product with given ID was deleted."
		}
	]
}
```

#### Procedure [**com.example.store.delete_product**]

Here is the complete signature of above procedure:

+ Procedure [com.example.store.delete_product]
	+ Help: Delete an existing product. When successful, a notification is sent.
	+ Arg: Product ID (int) - The product to be deleted.
	+ Arg: Cascade? (bool, optional) - Flag to activate cascaded delete, which deletes any dependent objects also.
	+ Result
		+ Arg: Total Deleted (int) - The total number of deleted items - including cascaded deletes.
	+ Error [com.example.error.no_such_product]
		+ Arg: Error Message (string) - An error messages for logging purposes. 
	+ Event [com.example.store.on_delete_product]
+ Topic [com.example.store.on_delete_product]
	+ Help: Fired when a product was deleted.
	+ Arg: Product ID (int) - The product with given ID was deleted


#### Procedure

```javascript
{
	"uri": "com.example.myproc1",
	"type": "procedure",
	"kwargs": {
		"number": {"type": "number"},
		"street_name": {"type": "string"},
		"street_type": {"type": "string",
			"enum": ["Street", "Avenue", "Boulevard"]}
	},
	"result_args": {
		"type": "number"
	}
}
```


```javascript
{
	"title": "com.example.myproc1",
    "description": "This procedure adds two numbers and returns the sum.",
	"type": "object",
	"properties": {
		"type": "procedure",
		"args": [
	    	{"type": "number", "title": "x"},
	    	{"type": "number", "title": "y"}
		],
		"rargs": [
	    	{"type": "number", "title": "sum"},
	    ]
	}
}
```


```javascript
{
	"$schema": "http://wamp.ws/schema#",
    "uri": "com.example.store.create_product",
	"type": "procedure",
    "title": "Create a Product",
    "description": "Create a new product entry in the Acme's catalog. Upon success, publish a notification.",
	"kwargs": {
	    "type": "object",
	    "properties": {
	        "id": {
	            "description": "The unique identifier for a product",
	            "type": "integer"
	        },
	        "name": {
	            "description": "Name of the product",
	            "type": "string"
	        },
	        "price": {
	            "type": "number",
	            "minimum": 0,
	            "exclusiveMinimum": true
	        }
	    },
	    "required": ["id", "name", "price"]
	},
	"result": {
		"args": {
			"type": "array",
			"items": [
				{
					"type": "number"
				}
			]
		}
	}
}
```


```javascript
{
	"$schema": "http://wamp.ws/schema#",
	"uri": "com.example.store.create_product:result:args",
	"value": {
	   "type": "array",
	   "items": [
	      {
	         "type": "number"
	      }
	   ]
	}
}
```
