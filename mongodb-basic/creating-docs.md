# ObjectId(<hexadecimal>)
- `_id` unique identifier for a document in a collection.
- `_id` required in every MongoDB document.
- `ObjectId()` is the default value for the `_id` field which is automatically generated unless otherwise specified.   
- The value of `_id` get assigned to a document, if you select a non `ObjectId` type value when inserting a new document, as long as that value is unique to this document.
> `ObjectId()` - returns a new ObjectId value. The 12-byte ObjectId value consists of:
> - a 4-byte **timestamp value**, representing the ObjectId's creation, measured in seconds since the Unix epoch
> - a 5-byte **random value**
> - a 3-byte **incrementing counter**, initialized to a random value  
> 
> While the *BSON format* itself is **little-endian**, the *timestamp* and *counter values* are **big-endian**, with the most significant bytes appearing first in the byte sequence.
---
# Inserting New Documents - insert() and errors:
To learn more about [Schema Validation, check out our excellent documentation page on that subject](https://docs.mongodb.com/manual/core/schema-validation/index.html#schema-validation).
> Upload document to the collection *without* **"E11000 duplicate key error"**
> ```
> $ mongoimport --uri="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<collection>" --drop <name>.json
> ```
1. Get a random document from the *inspections* collection
   ```
   $ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"
   $ use inspections  
   $ db.inspections.findOne();
   ```
2. Copy this random document, and insert it back to the *inspections* collection. Do you get
   a *__"Duplicate Key"__ error*?
   ```
   $ db.inspections.insert({
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
3. Insert that document into the *inspections* collection **without the `_id` field** to get a
   successful insert. Did it work?
   ```
   $ db.inspections.insert({
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
4. Check the results are correct  
   ```
   db.inspections.find({"id" : "10021-2015-ENFO", "certificate_number" : 9278806}).pretty()
   ```
---
# Inserting New Documents - insert() order:
> To insert multiple documents, use an array:  
> `db.<collection>.insert([{<doc1>}, {<doc2>}])`  
> 
> To disable the default ordered insert, add the field: `{"ordered": false}`
1. Insert three test documents into the **inspections** collection
   ```
   $ db.inspections.insert([{"test":1},{"test":2},{"test":3}])
   ```
2. Insert the same three documents into the **inspections** collection. Did it
   work? Why?  
   > If `_id` value is *undefined* in inserted document, it will be **automatically generated** before insertion.
3. Insert these three test documents into the **inspections** collection. Did it
   work? Why?
   ```
   $ db.inspections.insert([{"_id": 1, "test": 1},{"_id": 1, "test": 2},{"_id": 3,"test": 3}])
   ```  
   > *Duplicate* documents can be stored in the same collection, as long as their `_id` values are **different**.
4. Try the same insert as above but make it unordered.     
   ```
   $ db.inspections.insert([{ "_id": 1, "test": 1 },{ "_id": 1, "test": 2 }, { "_id": 3, "test": 3 }], { "ordered":false })
   ```
5. Try this command. Did it work? Why?
   ```
   $ db.inspection.insert([{ "_id":1, "test": 1 },{ "_id": 3,"test": 3 }])
   ```    
   > It works because there is a typo! the *new* collection **inspection** was created:   
   > to see it, type command `show collections` or use it, else the new one won't be created.     
   > It works the same way with *databases*.  
---
# Updating Documents  - *mongo shell*
> **Update operators:**
> 
> `{"$inc": {"pop": 10, "<field2>": <increment value>, ...}}`  
> -> **increments** field value by a specified amount.   
>
>`{"$set": {"pop": 17630, "<field2>": <new value>, ...}}`  
> -> **sets** field value to a *new* specified value.   
>
>`{ $push: { <field1>: <value1>, ...}}`  
> -> **adds** an element *to an array field*.  
>
> To learn more about all available [update operators in MQL, visit our excellent documentation page](https://docs.mongodb.com/manual/reference/operator/update/#id1).
1. Find all documents in the **zips** collection where the *zip* field is equal to
   *12434*.  
   ```
   $ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"  
   $ use sample_training  
   $ db.zips.find({ "zip": "12534" }).pretty()
   ```
2. Find all documents in the **zips** collection where the *city* field is equal to
   *"HUDSON"*.  
   ```
   $ db.zips.find({ "city": "HUDSON" }).pretty()
   ```
3. Find how many documents in the **zips** collection have the *city* field is equal
   to *"HUDSON"*.  
   ```
   $ db.zips.find({ "city": "HUDSON" }).count()   
   ```
4. Update all documents in the **zips** collection where the *city* field is equal
   to *"HUDSON"* by adding *10* to the current value of the *"pop"* field.  
   ```
   $ db.zips.updateMany({ "city": "HUDSON" }, 
                        { "$inc": { "pop": 10 } })
   ```
5. Update a single document in the **zips** collection where the *zip* field is
   equal to *12534* by setting the value of the *"pop"* field to *17630*.  
   ```
   $ db.zips.updateOne({ "zip": "12534" }, 
                       { "$set": { "pop": 17630 } })
   ```
6. Update a single document in the **zips** collection where the *zip* field is
   equal to *12534* by setting the value of the *"population"* field to *17630*.  
   ```
   $ db.zips.updateOne({ "zip": "12534" }, 
                       { "$set": { "population": 17630 } })
   ```
7. Find all documents in the **grades** collection where the *student_id* is *151*,
   and the *class_id* field is *339*.  
   ```
   $ db.grades.find({ "student_id": 151, "class_id": 339 }).pretty()
   ```
8. Find all documents in the **grades** collection where the *student_id* is *250*,
   and the *class_id* field is *339*.  
   ```
   $ db.grades.find({ "student_id": 250, "class_id": 339 }).pretty()
   ```
9. Update one document in the **grades** collection where the *student_id* is *250*,
   and the *class_id* field is *339*, by adding a document element to the *"scores"*
   array.  
   ```
   $ db.grades.updateOne({ "student_id": 250, "class_id": 339 }, 
                         { "$push": { "scores": { "type": "extra credit", "score": 100 } } })
   ```
# Deleting Documents and Collections
1. Look at all the documents in the **inspections** collection that have *test* field
   equal to *1*.
   ```
   $ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"  
   $ use sample_training
   $ db.inspections.find({ "test": 1 }).pretty()
   ```
2. Look at all the documents in the **inspections** collection that have *test* field
   equal to *3*.
   ```
   $ db.inspections.find({ "test": 3 }).pretty()
   ```
3. Delete all the documents from the **inspections** collection that have *test*
   field equal to *1*.
   ```
   $ db.inspections.deleteMany({ "test": 1 })
   ```
4. Delete one document from the **inspections** collection that has *test* field
   equal to *3*.
   ```
   $ db.inspections.deleteOne({ "test": 3 })
   ```
5. Inspect what is left of the **inspection** collection.  
   ```
   $ db.inspection.find().pretty()
   ```
   > We've made a typo and got the additional empty collection.
6. View what collections are present in the **sample_training** database and see **inspection** collection along with **inspections** collection.
   ```
   show collections
   ```
7. Drop (delete) the **inspection** collection and check the result.
   ```
   db.inspection.drop()
   ```
---
# Summary
| One | Many |
|---|---|
| `deleteOne("_id": 11)` | `deleteMany()` | 
| `updateOne("_id": 11)` | `updateMany()` |
| `findOne("_id": 11)` | `find()` |
> You can manipulate with a single document without `_id` field value if only a duplicates are not included in the collection.
> Remember: after deleting the data is GONE! 
---
## Practice Question:
People often confuse New York City as the capital of New York state, when in
reality the capital of New York state is Albany.  
In the **sample_training.zips** collection add a boolean field *"capital?"* to all
documents pertaining to *ALBANY* and *NEW YORK* in *state NY*. The value of the field
should be *true* for all *Albany* documents and *false* for all *New York* documents.

```
$ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"  
$ use sample_training
$ db.zips.findOne()  # to see the schema
$ db.zips.find({ "state": "NY" }).count()  # 1596
$ db.zips.find({ "state": "NY", "city": "ALBANY" }).count()  # 7
$ db.zips.find({ "state": "NY", "city": "NEW YORK" }).count()  # 40
$ db.zips.updateMany({ "state": "NY", "city": "ALBANY"}, { "$set": { "capital?": true } })  # modifiedCount: 7
$ db.zips.updateMany({ "state": "NY", "city": "NEW YORK"}, { "$set": { "capital?": false } })  # modifiedCount: 40
```