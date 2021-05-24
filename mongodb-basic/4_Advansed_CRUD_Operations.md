# MQL operators:
> **Update Operators** - enable us to modify database. -> *Previous chapter*  
> Example: `$inc`, `$set`, `$unset`, `$push`  
> 
> **Query Operators** - provide additional ways to locate data within the database. -> *This chapter*
## Query Operators: Comparison
> **Comparison Operators** specifically allow us to find data within a certain range.  
> `{ <field>: { <operator>: <value> } }`  
> `$eq` = **EQ**ual to  
> `$ne` = **N**ot **E**qual to  
> `$gt` > **G**reater **T**han  
> `$lt` < **L**ess **T**han  
> `$gte` >= **G**reater **T**han or **E**qual to  
> `$lte` <= **L**ess **T**han or **E**qual to  
> If no comparison operator specified, `$eq` is used by default.
### Example from the lesson
```
$ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"
$ use sample_training
```
Find all documents where the **tripduration** was less than or equal to **70** seconds, and the **usertype** was not **Subscriber**:  
```
$ db.trips.find({ "tripduration": { "$lte" : 70 }, "usertype": { "$ne": "Subscriber" } }).pretty()
```
Find all documents where the **tripduration** was less than or equal to **70** seconds, and the **usertype** was **Customer** using a redundant equality operator:
```
db.trips.find({ "tripduration": { "$lte" : 70 }, "usertype": { "$eq": "Customer" }}).pretty()
```
Find all documents where the **tripduration** was less than or equal to **70** seconds, and the **usertype** was **Customer** using the implicit equality operator:
```
db.trips.find({ "tripduration": { "$lte" : 70 }, "usertype": "Customer" }).pretty()
```
### Practice Question
How many documents in the **sample_training.zips** collection have fewer than **1000** people listed in the **pop** field?
```
$ use sample_training
'switched to db sample_training'
$ db.zips.find({ "pop": { "$lt": 1000 } }).count()
8065
```
What is the difference between the number of people born in **1998** and the number of people born after **1998** in the **sample_training.trips** collection?
```
$ db.trips.find({ "birth year": { "$gt": 1998 } }).count() - db.trips.find({ "birth year": 1998 }).count()
```
Using the **sample_training.routes** collection find out which of the following statements will return all routes that have at least one stop in them?
```
$ db.routes.find({ "stops": { "$gt": 0 } }).pretty()
$ db.routes.find({ "stops": { "$ne": 0 } }).pretty()
```
## Query Operators: Logic
