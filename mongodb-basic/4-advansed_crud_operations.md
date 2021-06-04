# MQL operators:
> **Update Operators** - enable us to modify database. -> *Previous chapter*  

Name | Description
---|---
`$currentDate` | Sets the value of a field to current date, either as a Date or a Timestamp.
`$inc` | Increments the value of the field by the specified amount.
`$min` | Only updates the field if the specified value is less than the existing field value.
`$max` | Only updates the field if the specified value is greater than the existing field value.
`$mul` | Multiplies the value of the field by the specified amount.
`$rename` | Renames a field.
`$set` | Sets the value of a field in a document.
`$setOnInsert` | Sets the value of a field if an update results in an insert of a document. Has no effect on update operations that modify existing documents.
`$unset` | Removes the specified field from a document.

> **Query Operators** - provide additional ways to locate data within the database. -> *This chapter*
## Query Operators: Comparison
**Comparison Operators** specifically allow us to find data within a certain range.  
`{ <field>: { <operator>: <value> } }`
> Operator | in Python | Description
> --- | --- | --- 
> `$eq` | `==` | **EQ**ual to   
> `$ne` | `!=` | **N**ot **E**qual to  
> `$gt` | `>` | **G**reater **T**han  
> `$lt` |  `<` | **L**ess **T**han  
> `$gte` | `>=` | **G**reater **T**han or **E**qual to  
> `$lte` | `<=` | **L**ess **T**han or **E**qual to  
If no comparison operator specified, `$eq` is used by default.
### Find query examples
1. Find all documents where the **tripduration** was less than or equal to **70** seconds, and the **usertype** was  
   a) not Subscriber, b-c: Customer using b) redundant equality operator and c) implicit equality operator
```
$ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"
$ use sample_training
$ db.trips.find({ "tripduration": { "$lte" : 70 }, "usertype": { "$ne": "Subscriber" } }).pretty()
$ db.trips.find({ "tripduration": { "$lte" : 70 }, "usertype": { "$eq": "Customer" } }).pretty()
$ db.trips.find({ "tripduration": { "$lte" : 70 }, "usertype": "Customer" }).pretty()
```
2. How many documents in the **sample_training.zips** collection have fewer than **1000** people listed in the **pop** field?
```
$ db.zips.find({ "pop": { "$lt": 1000 } }).count()
```
3. What is the difference between the number of people born in **1998** and the number of people born after **1998** in the **sample_training.trips** collection?
```
$ db.trips.find({ "birth year": { "$gt": 1998 } }).count() - db.trips.find({ "birth year": 1998 }).count()
```
---
## Query Operators: Logic
Operator | Description  
---|---  
`$and`| Joins query clauses with a logical AND returns all documents that match the conditions of both clauses.  
`$or`| Joins query clauses with a logical OR returns all documents that match the conditions of either clause.  
`$nor`| Joins query clauses with a logical NOR returns all documents that fail to match both clauses.  
`$not`| Inverts the effect of a query expression and returns documents that do not match the query expression.  

If no logical operator specified, `$and` is used by default as:   
```{ <operator>: [ <statement1>, <statement1>,...] }```  
Explicitly use `$and` when you need to include the same operator more than once in a query

Operator | Syntax 
---|---
`$and` `$or` `$nor` | ```{ <operator>: [ {<statement1>}, {<statement1>},...]}```   
`$not` | ```{ $not: {statement} }```

### Find query examples
1. Find all documents where airplanes **CR2** or **A81** left or landed in the **KZN** airport:
``` 
$ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"
$ use sample_training
$ db.routes.find({ "$and": [{ "$or" :[{ "dst_airport": "KZN" },
                                      { "src_airport": "KZN" }]},
                            { "$or" :[{ "airplane": "CR2" },
                                       { "airplane": "A81" } ] } ] }).pretty()
```
2. How many businesses in the **sample_training.inspections** dataset have the inspection **result** **"Out of Business"** and belong to the **"Home Improvement Contractor - 100"** **sector**?  
```
$ db.inspections.find({ "result": "Out of Business", "sector": "Home Improvement Contractor - 100"}).count()
```
3. Which is the most succinct query to return all documents from the **sample_training.inspections** collection where the inspection **date** is either **"Feb 20 2015"**, or **"Feb 21 2015"** and the company is not part of the **"Cigarette Retail Dealer - 127"** **sector**?
```
$ db.inspections.find({ "$or": [{ "date": "Feb 20 2015" }, { "date": "Feb 21 2015" }],
                        "sector": { "$ne": "Cigarette Retail Dealer - 127" } }).pretty()
```
4. Before solving this exercise, make sure to undo the changes that we made to the **zips** collection earlier in the course by running the following command:  
```db.zips.updateMany({ "city": "HUDSON" }, { "$inc": { "pop": -10 }})```
   How many zips in the **sample_training.zips** dataset are neither over-populated nor under-populated?
   In this case, we consider population of more than **1,000,000** to be over-populated and less than **5,000** to be under-populated.
```
$ db.zips.find({ "$nor":[{ "pop": { "$gt": 1000000 } }, 
                         { "pop": { "$lt": 5000 } }]}).count()
```
5. How many companies in the **sample_training.companies** dataset 
   - were either founded in **2004** [and] either have the *social* **category_code** [or] *web* **category_code**,  
   - [or] were founded in the month of **October** [and] also either have the *social* **category_code** [or] *web* **category_code**?
```
$ db.companies.find({ "$and": [{ "$or": [{ "category_code": "social" },
                                         { "category_code": "web" }] },
                               { "$or": [{ "founded_year": 2004 },
                                         {"founded_month": 10 }] }] }).count()           
```   
---
## Expressive Query Operator
> `$<expr>` allows the use of **aggregation expressions** within the query language, and it uses this syntax:  
> ```
> { <operator>: { <field>: <value> } }
> ```  
> `$expr` compares one field directly with other in one document, without specifying values of the fields.  
> 
> `$` denote an operator  
> `$` signify that you're looking at the value of that field, rather than just the field name itself
### Find query examples
1. Find all documents where the **trip** 
   - started and ended at the same **station**
   - lasted longer than **1200 seconds**, and started and ended at the same **station**
```
$ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"
$ use sample_training
$ db.trips.find({ "$expr": { 
                         "$eq": [ 
                              "$end station id", "$start station id"
                              ] 
                         }
               }).count()
$ db.trips.find({ "$expr": { 
                         "$and": [ 
                                   { "$gt": [ "$tripduration", 1200 ]},
                                   { "$eq": [ "$end station id", "$start station id" ]}
                               ]
                         }
               }).count()
```
2. How many companies in the **sample_training.companies** collection have the same **permalink** as their **twitter_username**?
```
$ db.companies.find({ "$expr": { "$eq": [ "$permalink", "$twitter_username" ] } }).count()
```
---
## Array operator
To specify conditions on the elements in the array field, use query operators in the query filter document:  
`{ <array field> : { <field>: <value> } }`  

`<field>` | Description
--- | ---
`$all` | Matches arrays that contain all elements specified in the query.
`$elemMatch` | Selects documents if element in the array field matches all the specified $elemMatch conditions.
`$size` | Selects documents if the array field is a specified size.
  
To query if the array field contains at least one element with the specified value,   
use the filter `{ <field>: <value> }` where `<value>` is the **element value**.

When specifying compound conditions on array elements, 
you can specify the query such that either a single array element meets these condition 
or any combination of array elements meets the conditions.

To learn more about all available update operators in MQL, visit our excellent [documentation page](https://docs.mongodb.com/manual/reference/operator/update/#id1).  

Name | Description  
---|---  
`$` | Acts as a placeholder to **update the first element** that matches the query condition.  
`$[]` | Acts as a placeholder to **update all elements in an array** for the documents that match the query condition.
`$[<identifier>]` | Acts as a placeholder to **update all elements** that match the **arrayFilters** condition for the documents that match the query condition.
`$addToSet` | **Adds** elements to an array only if they **do not already exist** in the set.
`$pop` | **Removes the first or last** item of an array.
`$pull` | **Removes all specified elements** of the array that match a query.
`$push` | **Adds an item** to an array.
`$pullAll` | **Removes all matching values** from an array.
> `$push` allows us to **add an element** to an array  
> `$push` will *fail*, if the field is **not an array**   
> `$push` *adds* the array field *with the value*, if the field is **absent**  
### Find query examples
1. Using the **sample_airbnb.listingsAndReviews** collection find out:
- all documents with exactly **20** amenities which include all the **amenities** listed in the query array
- the **name** of the listing that **accommodates** more than **6** people and has exactly **50 reviews**
- how many documents have the **"property_type" "House"**, and include **"Changing table"** as one of the **"amenities"**
- Which of the following queries will return all listings that have "Free parking on premises", "Air conditioning", and "Wifi" as part of their amenities, and have at least 2 bedrooms
```
$ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"
$ use sample_airbnb
$ db.listingsAndReviews.find({ "amenities": {
                                          "$size": 20,
                                          "$all": [ 
                                                "Internet", "Wifi",  "Kitchen",
                                                "Heating", "Family/kid friendly",
                                                "Washer", "Dryer", "Essentials",
                                                "Shampoo", "Hangers", "Hair dryer", 
                                                "Iron", "Laptop friendly workspace" 
                                                ]
                                          }
                            }).pretty()
$ db.listingsAndReviews.find({ "accommodates": { "$gt":  6 }, "number_of_reviews": 50 }).pretty()
$ db.listingsAndReviews.find({ "property_type": "House", "amenities": "Changing table"}).count()
$ db.listingsAndReviews.find({ "amenities": { 
                                          "$all": [ 
                                                "Free parking on premises", 
                                                "Wifi", 
                                                "Air conditioning" 
                                                ] 
                                          },
                               "bedrooms": { "$gte":  2 }}).pretty()
```
## Array Operators and Projection
> If documents have a lot of fields and don't fit on the screen, you can add a **projection** to our Find queries with *syntax*:   
>
> ```db.<collection>.find( { <query> }, { <projection> })```  
> 
> - `<query>` describes the **content we're looking for**, though we didn't write out the whole list on this slide    
> - `<projection>` describes specifically **which fields we're looking for**  

> `{ <projection> }` == `{ <field1>: <i>, <field2>: <i>, ... }`  
> - `i = 1` -> include the field
> - `i = 0` -> exclude the field
> - do not combine `i == 0` and `i == 1` in a projection 
> - exception: `{ "_id": 0, <field>: 1, }`  
  
> ```{ <field>: { "$elemMatch": { <field>: <value> } } }```
> - **match documents** that contain an array field with **at least one element** that matches the specified query criteria
> - **project** only the array elements with the **at least one element** that matches the specified criteria
### Find query examples
1. Find all documents 
   - with exactly **20 amenities** which include **all** the amenities listed in the query array, and display their **price** and **address**
   - that have **Wifi** as one of the amenities only include **price** and **address** in the resulting cursor 
   - try to exclude **maximum_nights** from the last -> *This will be an error*
```
$ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"
$ use sample_airbnb
$ db.listingsAndReviews.find({ "amenities": { 
                                          "$size": 20, 
                                          "$all": [ 
                                                "Internet", "Wifi",  "Kitchen", "Heating",
                                                "Family/kid friendly", "Washer", "Dryer",
                                                "Essentials", "Shampoo", "Hangers",
                                                "Hair dryer", "Iron",
                                                "Laptop friendly workspace" 
                                                ] 
                                          } 
                             }, { "price": 1, "address": 1 }).pretty()
$ db.listingsAndReviews.find({ "amenities": "Wifi" },
                             { "price": 1, "address": 1, "_id": 0 }).pretty()
$ db.listingsAndReviews.find({ "amenities": "Wifi" },
                             { "price": 1, "address": 1, "_id": 0, "maximum_nights":0 }).pretty() -> *This will be an error*
```
4. Switch to the **sample_training** database and **get one document** from the collection. Find all documents where the **student**:
- in **class 431** received a **grade** higher than **85** for any **type** of assignment
- had an **extra credit score**
```
$ use sample_training
$ db.grades.findOne()
$ db.grades.find({ "class_id": 431 },
               { "scores": { "$elemMatch": { "score": { "$gt": 85 } } }
             }).pretty()
$ db.grades.find({ "scores": { "$elemMatch": { "type": "extra credit" } }
               }).pretty()
```
5. In the **sample_training.companies** collection:
   - how many companies have offices in the **city** of **Seattle**
   - **names** of companies that had exactly **8 funding rounds**

```
$ db.companies.find({ "offices": { "$elemMatch": { "city": "Seattle" } } }).count()
$ db.companies.find({ "funding_rounds": { "$size": 8 } },
                    { "name": 1, "_id": 0 })
```
## Array Operators and Sub-Documents
MQL uses **dot-notation** to specify the adress of **nested** elements of document.  
To use dot-notation in arrays specify the **position** of the element in array **starting from 0**.
```
$ db.<collection>.find({ "<field0>.<field1>.<field2>": "value>" })
```
The following example queries for all documents where the second element in the array dim_cm is greater than 25:

`cursor = db.inventory.find({"dim_cm.1": {"$gt": 25}})`

To learn more about [querying arrays using MQL visit our excellent documentation page](https://docs.mongodb.com/manual/tutorial/query-arrays/).  
To learn more about the `$regex` operator [check out this documentation page](https://docs.mongodb.com/manual/reference/operator/query/regex/).

```
$ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"
$ use sample_training

db.trips.findOne({ "start station location.type": "Point" })

db.companies.find({ "relationships.0.person.last_name": "Zuckerberg" },
                  { "name": 1 }).pretty()

db.companies.find({ "relationships.0.person.first_name": "Mark",
                    "relationships.0.title": { "$regex": "CEO" } },
                  { "name": 1 }).count()


db.companies.find({ "relationships.0.person.first_name": "Mark",
                    "relationships.0.title": {"$regex": "CEO" } },
                  { "name": 1 }).pretty()

db.companies.find({ "relationships":
                      { "$elemMatch": { "is_past": true,
                                        "person.first_name": "Mark" } } },
                  { "name": 1 }).pretty()

db.companies.find({ "relationships":
                      { "$elemMatch": { "is_past": true,
                                        "person.first_name": "Mark" } } },
                  { "name": 1 }).count()

```
How many <collection>s in the sample_training.trips collection:
- started at stations that are to the west of the -74 longitude coordinate? Longitude decreases in value as you move west.
- were conducted in the city of NEW YORK?
```
$ db.trips.find({ "start station location.coordinates": { "$lt": -74 }}).count()
$ db.inspections.find({ "address.city": "NEW YORK"}).count()
```
The "start station location" has a sub-document that contains the coordinates array. To get to this coordinates array we must use use dot-notation. We can issue a range query to find all documents in this longitude. The caveat is to remember that all trips take place in NYC so the latitude value in the coordinates array will always be positive, and we don't have to worry about it when issuing a range query like this.


Which of the following queries will return the names and addresses of all listings from the sample_airbnb.listingsAndReviews collection where the first amenity in the list is "Internet"?
```
db.listingsAndReviews.find({ "amenities.0": "Internet" },
                           { "name": 1, "address": 1 }).pretty()
```

