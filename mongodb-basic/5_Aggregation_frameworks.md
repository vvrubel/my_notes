What are the differences between using aggregate() and find()?
- aggregate() can do what find() can and more.
- aggregate() allows us to compute and reshape data in the cursor.
```
db.<colection>.aggregate([{ "$match": { <field>: <value> } },
                          { "$project": { <field>: 1 } },
                          { "$group": { _id: <$expression>, //Group by Expression
                                        <field1>: { <accumulator1>: <expression1> }, //"count": { "$sum": 1 }
                                        ... }}
                          ])

db.listingsAndReviews.aggregate([{ "$project": { "room_type": 1, "_id": 0 }},
                                 { "$group": { "_id": "$room_type" }} ])
```

Connect to the Atlas cluster:
``` 
mongo "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/admin"
$ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"
``` 
Switch to this database:
``` 
use sample_airbnb
``` 
Find all documents that have `Wifi` as one of the `amenities`. Only include `price` and `address` in the resulting cursor.
``` 
db.listingsAndReviews.find({ "amenities": "Wifi" },
                           { "price": 1, "address": 1, "_id": 0 }).pretty()
``` 
Using the aggregation framework find all documents that have `Wifi` as one of the `amenities`. 
Only include `price` and `address` in the resulting cursor.
``` 
db.listingsAndReviews.aggregate([
                                  { "$match": { "amenities": "Wifi" } },
                                  { "$project": { "price": 1,
                                                  "address": 1,
                                                  "_id": 0 }}]).pretty()
``` 
Find one document in the collection and only include the `address` field in the resulting cursor.
``` 
db.listingsAndReviews.findOne({ },{ "address": 1, "_id": 0 })
``` 
Project only the `address` field value for each document, then group all documents into one document per `address.country` value.
``` 
db.listingsAndReviews.aggregate([ { "$project": { "address": 1, "_id": 0 }},
                                  { "$group": { "_id": "$address.country" }}])
``` 
Project only the `address` field value for each document, then group all documents into one document per `address.country` value, and count one for each document in each group.
``` 
db.listingsAndReviews.aggregate([
                                  { "$project": { "address": 1, "_id": 0 }},
                                  { "$group": { "_id": "$address.country",
                                                "count": { "$sum": 1 } } }
                                ])
```
---
## Cursor method: `sort()` and `limit()` 
(use with `find()` command):
- `sort()`
- `limit()`
- `pretty()`
- `count()`
There is another fun method called `skip()` that might come in handy with `sort()` and `limit()`
[Read more about it on the documentation page](https://docs.mongodb.com/manual/reference/method/cursor.skip/index.html)
```
db.<collection>.find().sort({ "pop": 1, "city": -1 }).limit(1).pretty()
```
"pop": 1 => 0 -> +Z (increasing - the least first)
"city": -1 => +Z -> 0 (decreasing - the highest first)

only `db.zips.find(...).sort(...).limit(n)`
not `db.zips.find(...).limit(n).sort(...)`

```
$ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"

$ use sample_training
$ db.zips.find().sort({ "pop": 1 }).limit(1)
$ db.zips.find({ "pop": 0 }).count()
$ db.zips.find().sort({ "pop": -1 }).limit(1)
$ db.zips.find().sort({ "pop": -1 }).limit(10)
$ db.zips.find().sort({ "pop": 1, "city": -1 })
```
Which of the following commands will return the `name` and `founding year` for the `5 `oldest companies 
in the `sample_training.companies` collection?
correct answers:
```
db.companies.find({ "founded_year": { "$ne": null }},
                  { "name": 1, "founded_year": 1 }
                 ).sort({ "founded_year": 1 }).limit(5)
         
db.companies.find({ "founded_year": { "$ne": null }},
                  { "name": 1, "founded_year": 1 }
                 ).limit(5).sort({ "founded_year": 1 })
```
not correct: 
```
$ db.companies.find({ },{ "name": 1, "founded_year": 1 }
                 ).sort({ "founded_year": 1 }).limit(5)

$ db.companies.find({ "name": 1, "founded_year": 1 }
                  ).sort({ "founded_year": 1 }).limit(5)
```

In what year was the youngest bike rider from the `sample_training.trips` collection born?
```
db.trips.find({ "birth year": { "$ne": "" }}, { "birth year": 1, "_id": 0 }).sort({ "birth year": -1 }).limit(1)
```
---
## Introduction to Indexes
- make queries even more efficient
- are one of the most impactful ways to improve query performance

**Index** -in a database - special data structure that stores a small portion of the collection's data set in an easy to traverse form.
When to index
Given
```
db.trips.find({ "birth year": 1989 }) // #filter by `birth year`
db.trips.find({ "start station id": 476 }).sort( { "birth year": 1 } ) // #sort by `birth year`
```
Index
```
db.trips.createIndex({ "birth year": 1 }) // #single field index
db.trips.createIndex({ "start station id": 1, "birth year": 1 }) // #compound index 
```
Jameela often queries the sample_training.routes collection by the src_airport field like this:
```
db.routes.find({ "src_airport": "MUC" }).pretty()
>>
db.routes.createIndex({ "src_airport": -1 })
```
## Introduction to Data Modeling

Data modeling - a way to organize fields in a document to support your application performance and querying capabilities.
Rule: data is stored in the way that it is used. 
Check out our [documentation](https://docs.mongodb.com/manual/core/data-modeling-introduction/) 

## Upsert - Update or Insert?
Everything in MQL that is used to *locate* a document in a collection can also be used to *modify* this document.   
```
db.<collection>.updateOne( {<query to locate>}, {<update>} )
```
`Upsert` is a hybrid of update and insert, it should only be used hen it is needed  
```
db.<collection>.updateOne( {<query>}, {<update>}, { "upsert": true } )
``` 
### The `upsert` option: 
  
- only needs its value specified if you want **to change the default* **false** *setting* to **true**
- `false` by default
- `upsert: true` and the query predicate returns an *empty cursor*, 
  the `update` operation creates a *new document* using the directive from the query predicate, and the *update* predicate. 
  (performs an insert if the query predicate doesn't return a matching document)
- When `upser: false` and the query predicate returns an empty cursor then there will be no updated documents as a result of this operation.  
  (an update will happen only when the query predicate is matched with a document from the collection)


`upsert: true`
- conditional updates:  
  Is there a match?
  - yes - update the matched document
  - no - insert a new document

`upsert: false`
- update an existing document
- insert a brand new document

query | `upsert:true` |	`upsert:false`
---|---|---
match | update | update
no match | insert |	nothing

```
db.iot.updateOne({ "sensor": r.sensor, "date": r.date,
                   "valcount": { "$lt": 48 } },
                         { "$push": { "readings": { "v": r.value, "t": r.time } },
                        "$inc": { "valcount": 1, "total": r.value } },
                 { "upsert": true })
```

## What actions are available to you via the Aggregation Builder in the Atlas Data Explorer?

- Syntax for each selected aggregation stage.
- Export pipeline to a programming language.
- A preview of the data in the pipeline at each selected stage.

To learn more about Realm check out our [Realm documentation](https://docs.mongodb.com/realm/)

To learn about application development with MongoDB take a [course from our Developer series](https://university.mongodb.com/learning_paths/developer)

Check out this [Charts tutorial](https://docs.mongodb.com/charts/saas/tutorial/order-data/order-data-tutorial-overview/)

## What is MongoDB Charts?
- A product that helps you build visualizations of the data stored in your Atlas Cluster.

Follow this link to [download MongoDB Compass](https://www.mongodb.com/try/download/compass)

To learn more about performance and indexing with MongoDB, take our [MongoDB Performance Course](https://university.mongodb.com/courses/M201/about)
