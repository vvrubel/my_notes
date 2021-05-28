# Query on Embedded/Nested Documents

This page provides examples of query operations on embedded/nested documents 
using the [`db.collection.find()`](https://docs.mongodb.com/manual/reference/method/db.collection.find/#mongodb-method-db.collection.find)
method in the [mongo](https://docs.mongodb.com/manual/reference/program/mongo/#mongodb-binary-bin.mongo) shell. 
The examples on this page use the `inventory` collection. To populate the `inventory` collection, run the following:
```
db.inventory.insertMany( [
   { item: "journal", qty: 25, size: { h: 14, w: 21, uom: "cm" }, status: "A" },
   { item: "notebook", qty: 50, size: { h: 8.5, w: 11, uom: "in" }, status: "A" },
   { item: "paper", qty: 100, size: { h: 8.5, w: 11, uom: "in" }, status: "D" },
   { item: "planner", qty: 75, size: { h: 22.85, w: 30, uom: "cm" }, status: "D" },
   { item: "postcard", qty: 45, size: { h: 10, w: 15.25, uom: "cm" }, status: "A" }
]);
```
---
## Match an Embedded/Nested Document
To specify an equality condition on a field that is an embedded/nested document, 
use the [query filter document](https://docs.mongodb.com/manual/core/document/#std-label-document-query-filter) 
`{ <field>: <value> }` where `<value>` is the document to match.

For example, the following query selects all documents where 
the field `size` equals the document `{ h: 14, w: 21, uom: "cm" }`:
```
db.inventory.find( { size: { h: 14, w: 21, uom: "cm" } } )
```
Equality matches on the whole embedded document require an exact match of the specified `<value>` document, 
including the field order. For example, the following query does not match any documents in the `inventory` collection:
```
db.inventory.find(  { size: { w: 21, h: 14, uom: "cm" } }  )
```
## Query on Nested Field
To specify a query condition on fields in an embedded/nested document, u
se [dot notation](https://docs.mongodb.com/manual/reference/glossary/#std-term-dot-notation) 
`<"field.nestedField">`

- When querying using dot notation, the field and nested field must be inside quotation marks.

### Specify Equality Match on a Nested Field
The following example selects all documents where the field `uom` nested in the `size` field equals `"in"`:
```
db.inventory.find( { "size.uom": "in" } )
```
### Specify Match using Query Operator
A [query filter document](https://docs.mongodb.com/manual/core/document/#std-label-document-query-filter) 
can use the [query operators](https://docs.mongodb.com/manual/reference/operator/query/#std-label-query-selectors) 
to specify conditions in the following form:

`{ <field1>: { <operator1>: <value1> }, ... }`

The following query uses the less than operator `($lt)` on the field `h` embedded in the `size` field:
```
db.inventory.find( { "size.h": { $lt: 15 } } )
```
### Specify AND Condition
The following query selects all documents where the nested field `h` is less than `15`, the nested field `uom `equals `"in"`, and the `status` field equals `"D"`:
```
db.inventory.find( { "size.h": { $lt: 15 }, "size.uom": "in", status: "D" } )
```
---
# Query an Array
This page provides examples of query operations on array fields using the `db.collection.find()` method in the mongo shell. 
The examples on this page use the `inventory` collection. To populate the `inventory` collection, run the following:
```
db.inventory.insertMany([
   { item: "journal", qty: 25, tags: ["blank", "red"], dim_cm: [ 14, 21 ] },
   { item: "notebook", qty: 50, tags: ["red", "blank"], dim_cm: [ 14, 21 ] },
   { item: "paper", qty: 100, tags: ["red", "blank", "plain"], dim_cm: [ 14, 21 ] },
   { item: "planner", qty: 75, tags: ["blank", "red"], dim_cm: [ 22.85, 30 ] },
   { item: "postcard", qty: 45, tags: ["blue"], dim_cm: [ 10, 15.25 ] }
]);
```
## Match an Array
To specify equality condition on an array, use the query document `{ <field>: <value> }`   
where `<value>` is the exact array to match, including the order of the elements.

The following example queries for all documents where the field `tags` value is an array  
with exactly two elements, `"red"` and `"blank"`, in the **specified order**:
```
cursor = db.inventory.find({"tags": ["red", "blank"]})
```
If, instead, you wish to find an array that contains both the elements `"red"` and `"blank"`,  
**without regard to order or other elements** in the array, 
use the [`$all`](https://docs.mongodb.com/manual/reference/operator/query/all/#mongodb-query-op.-all) operator:
```
cursor = db.inventory.find({"tags": {"$all": ["red", "blank"]}})
```
## Query an Array for an Element
To query if the array field contains at least one element with the specified value, 
use the filter `{ <field>: <value> }`, where `<value>` is the element value.

The following example queries for all documents where `tags` is an array  
that contains the string `"red"` as **one of its elements**:
```
cursor = db.inventory.find({"tags": "red"})
```
To specify conditions on the elements in the array field, 
use [query operators](https://docs.mongodb.com/manual/reference/operator/query/#std-label-query-selectors) 
in the [query filter document](https://docs.mongodb.com/manual/core/document/#std-label-document-query-filter):
`{ <array field>: { <operator1>: <value1>, ... } }`

For example, the following operation queries for all documents where the array `dim_cm` contains 
at least one element whose value is greater than `25`.
```
cursor = db.inventory.find({"dim_cm": {"$gt": 25}})
```
# Specify Multiple Conditions for Array Elements
When specifying compound conditions on array elements, you can specify the query such that either a single array element meets these condition or any combination of array elements meets the conditions.

### Query an Array with Compound Filter Conditions on the Array Elements
The following example queries for documents where the `dim_cm` array contains elements 
that in some combination satisfy the query conditions; 
e.g., one element can satisfy the greater than `15` condition 
and another element can satisfy the less than `20` condition, or a single element can satisfy both:
```
db.inventory.find( { dim_cm: { $gt: 15, $lt: 20 } } )`
```
### Query for an Array Element that Meets Multiple Criteria
Use [`$elemMatch`](https://docs.mongodb.com/manual/reference/operator/query/elemMatch/#mongodb-query-op.-elemMatch) operator 
to specify multiple criteria on the elements of an array such that at least one array element satisfies all the specified criteria.

The following example queries for documents where the `dim_cm` array contains at least one element 
that is both greater than [`$gt`](https://docs.mongodb.com/manual/reference/operator/query/gt/#mongodb-query-op.-gt) `22` 
and less than [`$lt`](https://docs.mongodb.com/manual/reference/operator/query/lt/#mongodb-query-op.-lt) `30`:
```
db.inventory.find( { dim_cm: { $elemMatch: { $gt: 22, $lt: 30 } } } )
```
### Query for an Element by the Array Index Position
Using [dot notation](https://docs.mongodb.com/manual/reference/glossary/#std-term-dot-notation), 
you can specify query conditions for an element at a particular index or position of the array. 
The array uses zero-based indexing.
- When querying using dot notation, the field and nested field must be inside quotation marks.

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:
```
db.inventory.find( { "dim_cm.1": { $gt: 25 } } )
```
### Query an Array by Array Length
Use the [`$size`](https://docs.mongodb.com/manual/reference/operator/query/size/#mongodb-query-op.-size) operator 
to query for arrays by number of elements. For example, the following selects documents where the array `tags` has 3 elements.
```
db.inventory.find( { "tags": { $size: 3 } } )
```
---
# Query an Array of Embedded Documents
This page provides examples of query operations on an array of nested documents 
using the `db.collection.find()` method in the mongo shell. 
The examples on this page use the `inventory` collection. To populate the `inventory` collection, run the following:
```
db.inventory.insertMany( [
   { item: "journal", instock: [ { warehouse: "A", qty: 5 }, { warehouse: "C", qty: 15 } ] },
   { item: "notebook", instock: [ { warehouse: "C", qty: 5 } ] },
   { item: "paper", instock: [ { warehouse: "A", qty: 60 }, { warehouse: "B", qty: 15 } ] },
   { item: "planner", instock: [ { warehouse: "A", qty: 40 }, { warehouse: "B", qty: 5 } ] },
   { item: "postcard", instock: [ { warehouse: "B", qty: 15 }, { warehouse: "C", qty: 35 } ] }
]);
```
## Query for a Document Nested in an Array
The following example selects all documents where an element in the `instock` array matches the specified document:
```
db.inventory.find( { "instock": { warehouse: "A", qty: 5 } } )
```
Equality matches on the whole embedded/nested document require an *exact* match of the specified document, 
including the field order. For example, the following query does not match any documents in the `inventory` collection:
```
db.inventory.find( { "instock": { qty: 5, warehouse: "A" } } )
```
## Specify a Query Condition on a Field in an Array of Documents
### Specify a Query Condition on a Field Embedded in an Array of Documents
If you do not know the index position of the document nested in the array, 
concatenate the name of the array field, with a dot `.` and the name of the field in the nested document.

The following example selects all documents where the `instock` array has at least one embedded document 
that contains the field `qty` whose value is less than or equal to `20`:
```
db.inventory.find( { 'instock.qty': { $lte: 20 } } )
```
### Use the Array Index to Query for a Field in the Embedded Document
Using [dot notation](https://docs.mongodb.com/manual/reference/glossary/#std-term-dot-notation),
you can specify query conditions for field in a document at a particular index or position of the array. 
The array uses zero-based indexing
- When querying using dot notation, the field and index must be inside quotation marks.

The following example selects all documents where the `instock` array has as its first element a document 
that contains the field `qty` whose value is less than or equal to `20`:
```
db.inventory.find( { 'instock.0.qty': { $lte: 20 } } )
```
## Specify Multiple Conditions for Array of Documents
When specifying conditions on more than one field nested in an array of documents, 
you can specify the query such that either a single document meets these condition 
or any combination of documents (including a single document) in the array meets the conditions.

### A Single Nested Document Meets Multiple Query Conditions on Nested Fields
Use [`$elemMatch`](https://docs.mongodb.com/manual/reference/operator/query/elemMatch/#mongodb-query-op.-elemMatch) operator 
to specify multiple criteria on an array of embedded documents such 
that at least one embedded document satisfies all the specified criteria.

The following example queries for documents where the `instock` array has at least one embedded document 
that contains both the field `qty` equal to `5` and the field `warehouse` equal to `A`:
```
db.inventory.find( { "instock": { $elemMatch: { qty: 5, warehouse: "A" } } } )
```
The following example queries for documents where the `instock` array has at least one embedded document 
that contains the field `qty` that is greater than `10` and less than or equal to `20`:
```
db.inventory.find( { "instock": { $elemMatch: { qty: { $gt: 10, $lte: 20 } } } } )
```
### Combination of Elements Satisfies the Criteria
If the compound query conditions on an array field do not use the 
[`$elemMatch`](https://docs.mongodb.com/manual/reference/operator/query/elemMatch/#mongodb-query-op.-elemMatch) operator, 
the query selects those documents whose array contains any combination of elements that satisfies the conditions.

For example, the following query matches documents where any document nested in the `instock` array 
has the `qty` field greater than `10` and any document (but not necessarily the same embedded document) in the array 
has the `qty` field less than or equal to `20`:
```
db.inventory.find( { "instock.qty": { $gt: 10,  $lte: 20 } } )
```
The following example queries for documents where the `instock` array has at least one embedded document 
that contains the field `qty` equal to `5` and at least one embedded document (but not necessarily the same embedded document) 
that contains the field `warehouse` equal to `A`:
```
db.inventory.find( { "instock.qty": 5, "instock.warehouse": "A" } )
```
