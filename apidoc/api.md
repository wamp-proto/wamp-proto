# Store API

## Products API

### Creating a Product

The store API includes a procedure to create a new product in the catalog

```javascript
{
	"$schema": "http://wamp.ws/schema#",
	"uri": "com.example.store.create_product",
	"type": "procedure",
	"title": "Create Product",
	"description": "Create a new product in the store catalog."
}
```

To create a new product, you need to provide an ID, a name and a price


```javascript
{
	"$schema": "http://wamp.ws/schema#",
    "uri": "com.example.store.create_product",
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
	}
}
```

When the product was successfully created, the procedure returns with


```javascript
{
	"$schema": "http://wamp.ws/schema#",
	"uri": "com.example.store.create_product",
	"result": {
		"args": {
		   	"type": "array",
		   	"items": [
				{
					"type": "number",
					"title": "Current Inventory",
					"description": "Total number of product items in inventory."
				}
			]
		}
	}
}
```

Also, whenever a product is successfully created in the store catalog, an event will be published


```javascript
{
	"$schema": "http://wamp.ws/schema#",
	"uri": "com.example.store.on_create_product",
   	"type": "topic",
	"title": "Product created",
	"description": "Fired when a product was created.",
	"result": {
		"args": {
		   	"type": "array",
		   	"items": [
				{
					"type": "number",
					"title": "Product ID",
					"description": "The ID of the product that was created."
				}
			]
		}
	}
}
```

Failure conditions where the procedure will raise an error include non-existant product


```javascript
{
	"$schema": "http://wamp.ws/schema#",
	"uri": "com.example.store.create_product",
	"errors": [
		"com.example.store.error.no_such_product",
		"com.example.store.error.invalid_price"
    ]
}
```

where

```javascript
{
	"$schema": "http://wamp.ws/schema#",
	"uri": "com.example.store.error.no_such_product",
	"title": "No such Product",
	"description": "This error is raised when an operation is performed on a product that does not exist in the catalog.",
	"type": "error",
	"args": {
	   	"type": "array",
	   	"items": [
			{
				"type": "string",
				"title": "Reason",
				"description": "A human readable message, intended for development and logging purposes."
			}
		]
	}
}
```
