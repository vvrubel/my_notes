

[`$group`](https://docs.mongodb.com/manual/reference/operator/aggregation/group/?jmp=university) documentation page.

- groups input documents by the specified _id expression and for each distinct grouping, outputs a document. 
- The _id field of each output document contains the unique group by value. 
- The output documents can also contain computed fields that hold the values of some accumulator expression.
- does not order its output documents

```
{
  $group:
    {
      _id: <expression>, // Group By Expression
      <field1>: { <accumulator1> : <expression1> },
      ...
    }
 }
```
(https://docs.mongodb.com/manual/reference/operator/aggregation/#group-accumulator-operators)
// grouping as before, then sorting in descending order based on the count
```
db.movies.aggregate([
  {
    "$group": {
      "_id": "$year",
      "count": { "$sum": 1 }
    }
  },
  {
    "$sort": { "count": -1 }
  }
])
```
// grouping on the number of directors a film has, demonstrating that we have to
// validate types to protect some expressions
```
db.movies.aggregate([
  {
    "$group": {
      "_id": {
        "numDirectors": {
          "$cond": [{ "$isArray": "$directors" }, { "$size": "$directors" }, 0]
        }
      },
      "numFilms": { "$sum": 1 },
      "averageMetacritic": { "$avg": "$metacritic" }
    }
  },
  {
    "$sort": { "_id.numDirectors": -1 }
  }
])
```
// showing how to group all documents together. By convention, we use null or an
// empty string, ""
```
db.movies.aggregate([
  {
    "$group": {
      "_id": null,
      "count": { "$sum": 1 }
    }
  }
])
```
// filtering results to only get documents with a numeric metacritic value
```
db.movies.aggregate([
  {
    "$match": { "metacritic": { "$gte": 0 } }
  },
  {
    "$group": {
      "_id": null,
      "averageMetacritic": { "$avg": "$metacritic" }
    }
  }
])
```

# Accumulator Stages with `$project`


// run to get a view of the document schema
```
db.icecream_data.findOne()
```
// using $reduce to get the highest temperature
```
db.icecream_data.aggregate([
  {
    "$project": {
      "_id": 0,
      "max_high": {
        "$reduce": {
          "input": "$trends",
          "initialValue": -Infinity,
          "in": {
            "$cond": [
              { "$gt": ["$$this.avg_high_tmp", "$$value"] },
              "$$this.avg_high_tmp",
              "$$value"
            ]
          }
        }
      }
    }
  }
])
```
// performing the inverse, grabbing the lowest temperature
```
db.icecream_data.aggregate([
  {
    "$project": {
      "_id": 0,
      "min_low": {
        "$reduce": {
          "input": "$trends",
          "initialValue": Infinity,
          "in": {
            "$cond": [
              { "$lt": ["$$this.avg_low_tmp", "$$value"] },
              "$$this.avg_low_tmp",
              "$$value"
            ]
          }
        }
      }
    }
  }
])
```
// note that these two operations can be done with the following operations can
// be done more simply. The following two expressions are functionally identical
```
db.icecream_data.aggregate([
  { "$project": { "_id": 0, "max_high": { "$max": "$trends.avg_high_tmp" } } }
])

db.icecream_data.aggregate([
  { "$project": { "_id": 0, "min_low": { "$min": "$trends.avg_low_tmp" } } }
])
```
// getting the average and standard deviations of the consumer price index
```
db.icecream_data.aggregate([
  {
    "$project": {
      "_id": 0,
      "average_cpi": { "$avg": "$trends.icecream_cpi" },
      "cpi_deviation": { "$stdDevPop": "$trends.icecream_cpi" }
    }
  }
])
```
// using the $sum expression to get total yearly sales
```
db.icecream_data.aggregate([
  {
    "$project": {
      "_id": 0,
      "yearly_sales (millions)": { "$sum": "$trends.icecream_sales_in_millions" }
    }
  }
])
```
## Lab - $group and Accumulators
In the last lab, we calculated a normalized rating that required us to know what the minimum and maximum values for `imdb.votes` were. These values were found using the `$group` stage!

For all films that won at least 1 Oscar, calculate the standard deviation, highest, lowest, and average `imdb.rating`. Use the `sample standard deviation` expression.

*HINT* - All movies in the collection that won an Oscar begin with a string resembling one of the following in their `awards` field
- "Won 13 Oscars"
- "Won 1 Oscar"

Select the correct answer from the choices below. Numbers are truncated to 4 decimal places.  

> Correct answer:  
>
> { "highest_rating" : 9.2,  
> "lowest_rating" : 4.5,  
> "average_rating" : 7.5270,  
> "deviation" : 0.5988 }
```
db.movies.aggregate([
  {
    $match: {
      awards: /Won \d{1,2} Oscars?/
    }
  },
  {
    $group: {
      _id: null,
      highest_rating: { $max: "$imdb.rating" },
      lowest_rating: { $min: "$imdb.rating" },
      average_rating: { $avg: "$imdb.rating" },
      deviation: { $stdDevSamp: "$imdb.rating" }
    }
  }
])
```

# [`$unwind`](https://docs.mongodb.com/manual/reference/operator/aggregation/unwind/)
Deconstructs an array field from the input documents to output a document for each element. Each output document is the input document with the value of the array field replaced by the element.


## Lab - `$unwind`
### Problem:

Let's use our increasing knowledge of the Aggregation Framework to explore our movies collection in more detail. We'd like to calculate how many movies every cast member has been in and get an average imdb.rating for each cast member.

What is the name, number of movies, and average rating (truncated to one decimal) for the cast member that has been in the most number of movies with English as an available language?

Provide the input in the following order and format

{ "_id": "First Last", "numFilms": 1, "average": 1.1 }

```
db.movies.aggregate([
  {
    $match: {
      languages: "English",
      "imdb.rating": { $exists: true, $ne: ""} 
    }
  },
  {
    $project: { _id: 0, cast: 1, "imdb.rating": 1 }
  },
  {
    $unwind: "$cast"
  },
  {
    $group: {
      _id: "$cast",
      numFilms: { $sum: 1 },
      average: { $avg: "$imdb.rating" }
    }
  },
  {
    $project: {
      numFilms: 1,
      average: {
        $divide: [{ $trunc: { $multiply: ["$average", 10] } }, 10]
      }
    }
  },
  {
    $sort: { numFilms: -1 }
  },
  {
    $limit: 1
  }
])
```

# The [`$lookup` Stage](https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/)

- you can only specify another collection to `from` within the same database
- The collection specified in `from` cannot be sharded
- `$lookup` matches between `localField` and `foreignField` with an equality match
- Specifying an existing field name to `as` will overwrite the existing field

## Lab - Using $lookup
### Problem:

Which alliance from air_alliances flies the most routes with either a Boeing 747 or an Airbus A380 (abbreviated 747 and 380 in air_routes)?

```
db.air_routes.aggregate([
  {
    $match: {
      airplane: /747|380/
    }
  },
  {
    $lookup: {
      from: "air_alliances",
      foreignField: "airlines",
      localField: "airline.name",
      as: "alliance"
    }
  },
  {
    $unwind: "$alliance"
  },
  {
    $group: {
      _id: "$alliance.name",
      count: { $sum: 1 }
    }
  },
  {
    $sort: { count: -1 }
  }
])
```
