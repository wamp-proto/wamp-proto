# Procedures

List of procedures the store application provides.

## Procedure `com.example.store.create_product`

Delete a product from the store catalog.

### Arguments

1. `id` (integer) The unique identifier for a product
2. `name` (string) The product name.
3. `price` (number) The price per unit in Euro.
4. `details` (object) Product details.
    * `rating` (integer) Product rating on a scale [0, 10].
    * `color` (string) Product color as a CSS color literal.
    * ... 

### Results

1. `total` (integer) Total number of product items in inventory.

### Errors

* `com.example.store.error.no_such_product` Unable to perform since the product does not exist.
* `com.example.store.error.invalid_price` The product price was invalid (e.g. negative).

### Events

* `com.example.store.on_create_product` Fired whenever a product was successfully created in the store catalog.

---


# Topics

List of topics used in the store application.

## Topic `com.example.store.on_create_product`

Fired when a product was created.

### Arguments

1. `id` (integer) The unique identifier of the product created.

---

# Errors

List of application specific errors used in the store application.

## Error `com.example.store.error.no_such_product`

This error is raised when an operation is performed on a product that does not exist in the catalog.

### Values

1. `reason` (string) A human readable message, intended for development and logging purposes.

---