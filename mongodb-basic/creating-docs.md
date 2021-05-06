# ObjectId(<hexadecimal>)
 
 `_id` unique identifier for a document in a collection.  
 
 `_id` required in every MongoDB document.  
 
 `ObjectId()` is the default value for the `_id` field which is automatically generated unless otherwise specified.  
 
  The value of `_id` get assigned to a document, if you select a non `ObjectId` type value when inserting a new document, as long as that value is unique to this document. 
  
  
> `ObjectId()` - returns a new ObjectId value. The 12-byte ObjectId value consists of:
>
> - a 4-byte timestamp value, representing the ObjectId's creation, measured in seconds since the Unix epoch
> - a 5-byte random value
> - a 3-byte incrementing counter, initialized to a random value
>
> While the BSON format itself is little-endian, the timestamp and counter values are big-endian, with the most significant bytes appearing first in the byte sequence.

---

# Inserting New Documents - insert() and errors:

> If a document is inserted without a provided `_id` value, then the `_id` field and value will be automatically generated for the inserted document before insertion.
>
> MongoDB can store duplicate documents in the same collection, as long as their `_id` values are different.
>
> To learn more about [Schema Validation, check out our excellent documentation page on that subject](https://docs.mongodb.com/manual/core/schema-validation/index.html#schema-validation).

`mongoimport --uri="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/sample_supplies" --drop sales.json`  # to upload document to the collection without *key error*

1. Get a random document from a collection

`mongo "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/admin"`
`use <collection>`
`db.inspections.findOne();`

2. Copy this random document, and insert it back to the collection. Do you get
   a "Duplicate Key" error?

```
db.inspections.insert({
      "_id" : ObjectId("56d61033a378eccde8a8354f"),
      "id" : "10021-2015-ENFO",
      "certificate_number" : 9278806,
      "business_name" : "ATLIXCO DELI GROCERY INC.",
      "date" : "Feb 20 2015",
      "result" : "No Violation Issued",
      "sector" : "Cigarette Retail Dealer - 127",
      "address" : {
              "city" : "RIDGEWOOD",
              "zip" : 11385,
              "street" : "MENAHAN ST",
              "number" : 1712
         }
  })
```

3. Insert that document into the collection without the _id field to get a
   successfull insert. Did it work?
   
```
db.inspections.insert({
      "id" : "10021-2015-ENFO",
      "certificate_number" : 9278806,
      "business_name" : "ATLIXCO DELI GROCERY INC.",
      "date" : "Feb 20 2015",
      "result" : "No Violation Issued",
      "sector" : "Cigarette Retail Dealer - 127",
      "address" : {
              "city" : "RIDGEWOOD",
              "zip" : 11385,
              "street" : "MENAHAN ST",
              "number" : 1712
         }
  })
```
`db.inspections.find({"id" : "10021-2015-ENFO", "certificate_number" : 9278806}).pretty()`  # check results

---

# Inserting New Documents - insert() order:

> Insert multiple documents using an arrray: `db.collection.insert([{<doc1>}, {<doc2>}])`
>
> Use `{"ordered": false}` to disable the default ordered insert.  


1. Insert three test documents into the inspections collection

`db.inspections.insert([{"test":1},{"test":2},{"test":3}])`

2. Insert the same three documents into the inspections collection. Did it
   work? Why?
   - It works because new `_id` is generated for everyone.
   
3. Insert these three test documents into the inspections collection. Did it
   work? Why?
   
`db.inspections.insert([{"_id": 1, "test": 1},{"_id": 1, "test": 2},{"_id": 3,"test": 3}])`

4. Try the same insert as above but make it unordered.

`db.inspections.insert([{ "_id": 1, "test": 1 },{ "_id": 1, "test": 2 }, { "_id": 3, "test": 3 }], { "ordered": false })`

5. Try this command. Did it work? Why?

`db.inspection.insert([{ "_id":1, "test": 1 },{ "_id": 3,"test": 3 }])`  # it works because there is a typo! the new collection was created: to see it `show collections`. It works the same way with databases.


# Updating Documents  - mongo shell

Update operators:
`{"$inc": {"pop": 10, "<field2>": <increment value>, ...}}`  # increments field value by a specified amount. 

`{"$set": {"pop": 17630, "<field2>": <new value>, ...}}`  # sets field value to a new spesified value. 

`{ $push: { <field1>: <value1>, ...}}`  # adds an element to an array field. 

> To learn more about all available [update operators in MQL, visit our excellent documentation page](https://docs.mongodb.com/manual/reference/operator/update/#id1).

1. Find all documents in the zips collection where the zip field is equal to
   12434.
2. Find all documents in the zips collection where the city field is equal to
   "HUDSON".
3. Find how many documents in the zips collection have the zip field is equal
   to "HUDSON".
4. Update all documents in the zips collection where the city field is equal
   to "HUDSON" by adding 10 to the current value of the "pop" field.
5. Update a single document in the zips collection where the zip field is
   equal to 12534 by setting the value of the "pop" field to 17630.
6. Update a single document in the zips collection where the zip field is
   equal to 12534 by setting the value of the "population" field to 17630.
7. Find all documents in the grades collection where the student_id is 151,
   and the class_id field is 339.
8. Find all documents in the grades collection where the student_id is 250,
   and the class_id field is 339.
9. Update one document in the grades collection where the student_id is 250,
   and the class_id field is 339, by adding a document element to the "scores"
   array.

Practice Question:

People often confuse New York City as the capital of New York state, when in
reality the capital of New York state is Albany.

Add a boolean field "capital?" to all documents pertaining to Albany NY, and
New York, NY. The value of the field should be true for all Albany documents
and false for all New York documents.


Deleting Documents and Collections

1. Look at all the documents in the inspections collection that have test field
   equal to 1.
2. Look at all the documents in the inspections collection that have test field
   equal to 3.
3. Delete all the documents from the inspections collection that have test
   field equal to 1
4. Delete one document from the inspections collection that has test field
   equal to 3
5. Inspect what is left of the inspection collection.
6. View what collections are present in the sample_training collection.
7. Drop the inspection collection

---

Practice Question:

People often confuse New York City as the capital of New York state, when in
reality the capital of New York state is Albany.

In the sample_training.zips collection add a boolean field "capital?" to all
documents pertaining to Albany NY, and New York, NY. The value of the field
should be true for all Albany documents and false for all New York documents.
