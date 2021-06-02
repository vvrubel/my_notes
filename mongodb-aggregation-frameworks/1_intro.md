# Introduction and Aggregation Concepts
- Tutorial to install [MongoDB Enterprise](https://docs.mongodb.com/manual/tutorial/install-mongodb-enterprise-on-os-x/)

- to connect
```
mongo "mongodb://cluster0-shard-00-00-jxeqq.mongodb.net:27017,cluster0-shard-00-01-jxeqq.mongodb.net:27017,cluster0-shard-00-02-jxeqq.mongodb.net:27017/aggregations?replicaSet=Cluster0-shard-0" --authenticationDatabase admin --ssl -u m121 -p aggregations --norc
```
## The Concept of Pipelines
```
db.collection.aggregate( [ { <stage> }, ... ] )
```
- Pipelines are a composition of stages.

- Stages are configurable to produce desired transformations.

- Pipelines must consist of at least one stage, and can have many stages.

- Documents flow through the pipeline, passing one stage to the next

- The Aggregation Framework provides us many stages to filter and transform our data.


## Aggregation Structure and Syntax
```
db.orders.aggregate([
   { $match: { status: "A" } },
   { $group: { _id: "$cust_id", total: { $sum: "$amount" } } }
])
db.collection.aggregate( [ { <stage> }, ... ], { <option> } )
```

[Each stage is composed of either operators or expressions.](https://docs.mongodb.com/manual/meta/aggregation-quick-reference/)

### So what's an operator?

For this course, when we say operators, we mean either query operators or aggregation stages.

In this example, `$match` and `$project` are **aggregation operators**, and `$in`, `$gte`, and `$lte`, are **query operators**.

As a general rule, operators always appear in the *key position* of a document.

### What's an expression?

Expressions act a lot like functions.

We provide arguments and they provide a computed output.

And just like functions, expressions can be composed to form powerful new data transformations.

MongoDB provides expressions for working with and producing values for many types of values.

In the project stage, $gt is an expression.

And its arguments are supplied in ths array.

This $number of moons, surrounded by the quotes, is also an expression that you'll learn about in a moment.

An easy way to remember how to use expressions is that it will always appear in a value position.


Field Path: `$fieldName`
System Variable: `$$UPPERCASE`
User Variable: `$$foo`