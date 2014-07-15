FORMAT: 1A

# Gist Fox API
Gist Fox API is a **pastes service** similar to [GitHub's Gist](http://gist.github.com).

# Gist Fox API Root [/]
Gist Fox API entry point.

This resource does not have any attributes. Instead it offers the initial API affordances in the form of the HTTP Link header and HAL links.

## Retrieve Entry Point [GET]

+ Response 200 (application/hal+json)
    + Headers

            Link: <http:/api.gistfox.com/>;rel="self",<http:/api.gistfox.com/gists>;rel="gists"

    + Body

            {
                "_links": {
                    "self": { "href": "/" },
                    "gists": { "href": "/gists?{since}", "templated": true }
                }
            }


## Delete a Product

To delete an existing product:

+ Procedure [com.example.store.delete_product]
	+ Request
		+ Args
	
				[<product_id|int>, <cascade|bool>]
	
	+ Result
		+ KwArgs
	
				{"cascaded": 5, "lifetime": 714172}
	+ Errors
		+ Could not find Product [com.example.error.no_such_product]
	+ Events
		+ Product was created [com.example.store.product.on_create]
			+ Args
				
					[100]
	
			+ KwArgs
			
					{"label": "red apple", "size": 120, "price", 99.99} 

## Product was Deleted

When the product creation succeeds, an event is triggered:

+ Topic [com.example.store.product.on_create]
	+ Args
				
			[100]

	+ KwArgs
	
			{"label": "red apple", "size": 120, "price", 99.99} 
		


## Delete a Product [com.example.store.delete_product]

+ Args: `<product_id:int>[, <cascade:bool> := False]`
+ KwArgs: -
+ Errors:
	+ `com.example.error.no_such_product`: 
	+ 

```wamp
{
	"type": "topic",
    "short": "",
    "args": [
       {"label": "product_id", "types": [int]},
       {"label": "cascade", "types": [bool], "default": false}
    ]
}
```

# Examples

Call **procedure** `com.example.store.delete_product` with **args** = `[123, true]`.

**Result**:

```javascript
{
   "lifetime": 33451
   "cascaded": 23
}
```



```javascript
{
   	"type": "procedure",
	"uri": "com.example.store.delete_product",
	"help": "Delete an existing product. When successful, a notification is sent.",
	"args": [
		{
			"label": "product_id",
			"types": ["int"],
			help = "The product to be deleted."
		},
		{
			"label": "cascade",
			"types": ["bool"],
			"optional": true,
			help = "Flag to activate cascaded delete, which deletes any dependent objects also."}
	],
	"result": {
		"args": [{"label": "cascaded_count", "types": ["int"]}]
	},
	"errors": {
		"com.example.error.no_such_product": {
			"help": "The product that was requested to be deleted does not exist.",
			"args": [{"label": "error_message", "types": ["string"]}]
		}
	}
}
```

Example call `args`:


```javascript
[100, true]
```

and example result `args`:

```javascript
[3]
```

or error `args` for an error `com.example.error.no_such_product`:

```javascript
["no product with ID 100"]
```
