# Basic Aggregation - $match and $project 
## Filtering documents with `$match`

[Documentation page](https://docs.mongodb.com/manual/reference/operator/aggregation/match/?jmp=university)
```
{ $match: { <query> } }
```

- The `$match` query syntax is identical to the [read operation query](https://docs.mongodb.com/manual/tutorial/query-documents/#std-label-read-operations-query-argument) syntax; i.e. `$match` does not accept [raw aggregation expressions](https://docs.mongodb.com/manual/meta/aggregation-quick-reference/#std-label-aggregation-expressions). To include aggregation expression in `$match`, use a `$expr` query expression:
```
$match: { $expr: { <aggregation expression> } } }
var pipeline = [
  {"$match": {
    "$expr": {"$gt": [{"$multiply": ["$width", "$height"]}, 12]},
  }},      
];
```
Inside an `$expr` operator, you can include any composite expression fashioned from `$` operator functions, `$` field paths and `$$` variables.

A few situations demand having to use `$expr` from inside a `$match` stage. Examples include:

A requirement to compare two fields from the same record to determine whether to keep the record based on the comparison's outcome
A requirement to perform a calculation based on values from multiple existing fields in each record and then comparing the calculation to a constant

- You cannot use `$where` in `$match` queries as part of the aggregation pipeline.
- You cannot use `$near` or `$nearSphere` in `$match` queries as part of the aggregation pipeline. As an alternative, you can either:
  - Use `$geoNear` stage instead of the `$match` stage.
  - Use `$geoWithin` query operator with `$center` or `$centerSphere` in the `$match` stage.
- To use `$text` in the `$match` stage, the `$match` stage has to be the first stage of the pipeline.

> - It uses the familiar MongoDB query language.  
> 
> $match uses the MongoDB query language query operators to express queries.
> - It should come very early in an aggregation pipeline.
> 
> The earlier in the pipeline, the more efficient our pipelines will become. Not only because we will expression filters that reduce the number of documents to process, but also the fact that we might be using indexes withing the pipeline execution.


### Lab - $match
Documentation
Help MongoDB pick a movie our next movie night! Based on employee polling, we've decided that potential movies must meet the following criteria.
- `imdb.rating` is at least 7 
- `genres` does not contain "Crime" or "Horror"
- `rated` is either "PG" or "G"
- `languages` contains "English" and "Japanese"
```
var pipeline = [{ $match: { "imdb.rating": { $gte: 7 }}}, 
                { $match: { "genres": { $nin: ["Crime", "Horror"] }}}, 
                { $match: { "rated": { $in: ["PG", "G"]}}}, 
                { $match: { "languages": { $all: ["English", "Japanese"]}}
                }]
db.movies.aggregate(pipeline).itcount()
load("/Users/vasilevaaa/Documents/MongoDB/m121/validateLab1.js")
<<< true
validateLab1(pipeline)
<<< Answer is 15
```
## Shaping documents with `$project`

[Documentation](https://docs.mongodb.com/manual/reference/operator/aggregation/project/?jmp=university)  
- Once we specify a field to retain or perform some computation in a $project stage, we must specify all fields we wish to retain. The only exception to this is the _id field.

- Beyond simply removing and retaining fields, $project lets us add new fields.

### Lab - Changing Document Shape with `$project`
Using the same `$match` stage from the previous lab, add a `$project` stage to only display `title` and `rated` fields.
```
var pipeline = [{$match: {
              "imdb.rating": { $gte: 7 }
            }}, {$match: {
              "genres": { $nin: ["Crime", "Horror"] }
            }}, {$match: {
              "rated": { $in: ["PG", "G"]}
            }}, {$match: {
              "languages": { $all: ["English", "Japanese"]}
            }}, {$project: {
              "_id": 0, "title": 1, "rated": 1
            }}]
```
## Computing Fields
[$split (aggregation)](https://docs.mongodb.com/manual/reference/operator/aggregation/split/#mongodb-expression-exp.-split)
```
{ $split: [ <string expression>, <delimiter> ] }
```
Field |Type |Description
---|---|---
string expression|string|The string to be split. string expression can be any valid expression as long as it resolves to a string. For more information on expressions, see Expressions.
delimiter|string|The delimiter to use when splitting the string expression. delimiter can be any valid expression as long as it resolves to a string.

The goal of following aggregation operation is to find the total quantity of deliveries for each state and sort the list in descending order. It has five pipeline stages:

- The $project stage produces documents with two fields, qty (integer) and city_state (array). The $split operator creates an array of strings by splitting the city field, using a space (" ") as a delimiter.
- The $unwind stage creates a separate record for each element in the city_state field.
- The $match stage uses a regular expression to filter out the city documents, leaving only those containing a state.
- The $group stage groups all the states together and sums the qty field.
- The $sort stage sorts the results by total_qty in descending order.
```
db.deliveries.aggregate([
  { $project : { city_state : { $split: ["$city", ", "] }, qty : 1 } },
  { $unwind : "$city_state" },
  { $match : { city_state : /[A-Z]{2}/ } },
  { $group : { _id: { "state" : "$city_state" }, total_qty : { "$sum" : "$qty" } } },
  { $sort : { total_qty : -1 } }
]);
```

[$size (aggregation)](https://docs.mongodb.com/manual/reference/operator/aggregation/size/#mongodb-expression-exp.-size)

Counts and returns the total number of items in an array.

`$size` has the following syntax:

`{ $size: <expression> }`

The argument for $size can be any expression as long as it resolves to an array. For more information on expressions, see Expressions.

```
db.inventory.aggregate([
   {
      $project: {
         item: 1,
         numberOfColors: { $cond: { if: { $isArray: "$colors" }, then: { $size: "$colors" }, else: "NA"} }
      }
   }
] )
```
### Lab - Computing Fields
Our movies dataset has a lot of different documents, some with more convoluted titles than others. If we'd like to analyze our collection to find movie titles that are composed of only one word, we could fetch all the movies in the dataset and do some processing in a client application, but the Aggregation Framework allows us to do this on the server!

Using the Aggregation Framework, find a count of the number of movies that have a title composed of one word. To clarify, "Cinderella" and "3-25" should count, where as "Cast Away" would not.

Make sure you look into the [`$split` String expression](https://docs.mongodb.com/manual/meta/aggregation-quick-reference/#string-expressions) and the [`$size` Array expression](https://docs.mongodb.com/manual/meta/aggregation-quick-reference/#array-expressions)

To get the count, you can append `itcount()` to the end of your pipeline
```
db.movies.aggregate([ [{$project: { title_word: { $split: ["$title", " "] }}}, {$match: { title_word: { $size: 1}}}] ]).itcount()
```

### Optional Lab - Expressions with `$project`
This lab will have you work with data within **arrays**, a common operation.

Specifically, one of the arrays you'll work with is `writers`, from the `movies` collection.

There are times when we want to make sure that the **field is an array**, and that **it is not empty**. We can do this within `$match`
```
{ $match: { writers: { $elemMatch: { $exists: true } } }
```
However, the entries within `writers` presents another problem. A good amount of entries in `writers` look something like the following, where the writer is attributed with their specific contribution
```
"writers" : [ "Vincenzo Cerami (story)", "Roberto Benigni (story)" ]
```
But the `writer` also appears in the `cast` array as "Roberto Benigni"!

```
db.movies.findOne({title: "Life Is Beautiful"}, { _id: 0, cast: 1, writers: 1})
```
This presents a problem, since comparing "Roberto Benigni" to "Roberto Benigni (story)" will definitely result in a difference.

`$map` lets us iterate over an array, element by element, performing some transformation on each element. The result of that transformation will be **returned in the same place** as the original element.

Within `$map`, the argument to `input` can be any expression as long as it resolves to an array. The argument to `as` is the name of the variable we want to use to refer to each element of the array when performing whatever logic we want. The field `as` is optional, and if omitted each element must be referred to as `$$this`:: The argument to `in` is the expression that is applied to each element of the `input` array, referenced with the variable name specified in `as`, and prepending two dollar signs:
```
writers: {
  $map: {
    input: "$writers",
    as: "writer",
    in: "$$writer"
  }
}
```
in is where the work is performed. Here, we use the `$arrayElemAt` expression, which takes two arguments, the array and the index of the element we want. We use the `$split` expression, splitting the values on " (".

If the string did not contain the pattern specified, the only modification is it is wrapped in an array, so `$arrayElemAt` will always work
```
writers: {
  $map: {
    input: "$writers",
    as: "writer",
    in: {
      $arrayElemAt: [
        {
          $split: [ "$$writer", " (" ]
        },
        0
      ]
    }
  }
}
```
pipeline:
```
var pipeline = [{$match: {
  writers: { $elemMatch: { $exists: true } }
}}, {$project: {
  writers: {
  $map: {
    input: "$writers",
    as: "writer",
    in: {
      $arrayElemAt: [
        {
          $split: [ "$$writer", " (" ]
        },
        0
      ]
    }
  }
}, "cast": 1, "_id": 0
}}]
```

`$setIntersection`
Takes two or more arrays and returns an array that contains the elements that appear in every input array.

`$setIntersection` has the following syntax:

`{ $setIntersection: [ <array1>, <array2>, ... ] }`

The arguments can be any valid expression as long as they each resolve to an array. For more information on expressions, see [Expressions](https://docs.mongodb.com/manual/meta/aggregation-quick-reference/#std-label-aggregation-expressions).

The following operation uses the $setIntersection operator to return an array of elements common to both the A array and the B array:
```
db.experiments.aggregate(
   [
     { $project: { A: 1, B: 1, commonToBoth: { $setIntersection: [ "$A", "$B" ] }, _id: 0 } }
   ]
)
```

### Problem:

Let's find how many movies in our `movies` collection are a "labor of love", where the same person appears in `cast`, `directors`, and `writers`

Hint: You will need to use `$setIntersection` operator in the aggregation pipeline to find out the result.

Note that your dataset may have duplicate entries for some films. You do not need to count the duplicate entries.

To get a count after you have defined your pipeline, there are two simple methods.

// add the `$count` stage to the end of your pipeline
// you will learn about this stage shortly!
```
db.movies.aggregate([
  {$stage1},
  {$stage2},
  {...$stageN},
  { $count: "labors of love" }
])

// or use itcount()
db.movies.aggregate([
  {$stage1},
  {$stage2},
  {...$stageN}
]).itcount()
```
How many movies are "labors of love"?

With our first `$match` stage, we filter out documents that are not an array or have an empty array for the fields we are interested in.
```
{
  $match: {
    cast: { $elemMatch: { $exists: true } },
    directors: { $elemMatch: { $exists: true } },
    writers: { $elemMatch: { $exists: true } }
  }
},
```
Next is a `$project` stage, removing the `_id` field and retaining both the `directors` and `cast` fields. We replace the existing `writers` field with a new computed value, cleaning up the strings within `writers`
```
  {
    $project: {
      _id: 0,
      cast: 1,
      directors: 1,
      writers: {
          $map: {
            input: "$writers",
            as: "writer",
            in: {
              $arrayElemAt: [
                {
                  $split: ["$$writer", " ("]
                },
                0
              ]
            }
          }
        }
      }
    }
  }
},
```
We use another `$project` stage to computer a new field called `labor_of_love` that ensures the intersection of `cast`, `writers`, and our newly cleaned `directors` is greater than `0`. This definitely means that at least one element in each array is identical! `$gt` will return true or false.
```
{
  $project: {
    labor_of_love: {
      $gt: [
        { $size: { $setIntersection: ["$cast", "$directors", "$writers"] } },
        0
      ]
    }
  }
},
```
Lastly, we follow with a `$match` stage, only allowing documents through where `labor_of_love` is `true`. In our example we use a `$match` stage, but `itcount()` works too.
```
{
  $match: { labor_of_love: true }
},
{
  $count: "labors of love"
}

// or

  {
    $match: { labor_of_love: true }
  }
]).itcount()
```

```
var pipeline = [{$project: {
  "_id": 0,
  "countries": 1,
  "tomatoes.viewer.rating": 1,
  "title": 1,
  "cast": 1,
  "favs": {$setIntersection: [ "$cast", ["Sandra Bullock", "Tom Hanks", "Julia Roberts", "Kevin Spacey", "George Clooney"]] },
}}, {$match: {
 favs: { $elemMatch: { $exists: true } },
 countries: "USA",
 "tomatoes.viewer.rating": { $gte: 3 },
}}, {$addFields: {
  num_favs: { $size: "$favs"}
}}, {$sort: {
  "num_favs": -1,
  "tomatoes.viewer.rating": -1, 
  "title": -1
}}, {$skip: 24}]
db.movies.aggregate( pipeline )
```