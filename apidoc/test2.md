# Store API

## Products API

### Deleting Products

To delete an existing product from the store, call the **procedure**

	com.example.store.delete_product(product_id, cascade) -> total_deleted

 * The procedure takes a mandatory positional argument `product_id` to provide the ID of the product to be deleted.
 * An optional `cascade` positional argument allows you to extend the deletion to any dependend objects.
 * The procedure will return the total number of deleted items (including those deleted due to cascading the deletion).

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

```javascript
{
	"uri": "com.example.store.delete_product",
   	"type": "procedure",
	"help": "Delete an existing product. When successful, a notification is sent.",
	"args": [
		{
			"label": "product_id",
			"types": ["int"],
			"help" = "The product to be deleted."
		},
		{
			"label": "cascade",
			"types": ["bool"],
			"optional": true,
			"help" = "Flag to activate cascaded delete, which deletes any dependent objects also."}
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
