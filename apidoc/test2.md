# Store API

## Products API

### Deleting Products

To delete an existing product from the store, call the **procedure**

	com.example.store.delete_product

The procedure takes a mandatory positional argument `product_id` to provide the ID of the product to be deleted.

An optional `cascade` positional argument allows you to extend the deletion to any dependend objects.

The procedure will return the total number of deleted items (including those deleted due to cascading the deletion).

Here is the procedure signature:

```wamp
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

#### Deleting Products - Example 1

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
