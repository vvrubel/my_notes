# `$addFields` and how it is similar to `$project`

[$addFields](https://docs.mongodb.com/manual/reference/operator/aggregation/addFields/?jmp=university) documentation page.

Adds new fields to documents. `$addFields` outputs documents that contain all existing fields from the input documents and newly added fields.

The `$addFields` stage is equivalent to a `$project` stage that explicitly specifies all existing fields in the input documents and adds the new fields.
>Starting in version 4.2, MongoDB adds a new aggregation pipeline stage `$set` that is an alias for `$addFields`.

`$addFields` has the following form:
```
{ $addFields: { <newField>: <expression>, ... } }
```

`$addFields` appends new fields to existing documents. You can include one or more `$addFields` stages in an aggregation operation.

To add field or fields to embedded documents (including documents in arrays) use the `dot notation`. See [example](https://docs.mongodb.com/manual/reference/operator/aggregation/addFields/?jmp=university#std-label-add-field-to-embedded).

To add an element to an existing array field with $addFields, use with `$concatArrays`. See [example](https://docs.mongodb.com/manual/reference/operator/aggregation/addFields/?jmp=university#std-label-addFields-add-element-to-array).
```
db.scores.aggregate([
   { $match: { _id: 1 } },
   { $addFields: { homework: { $concatArrays: [ "$homework", [ 7 ] ] } } }
])
```



MongoDB has another movie night scheduled. This time, we polled employees for their favorite actress or actor, and got these results
```
favorites = [
  "Sandra Bullock",
  "Tom Hanks",
  "Julia Roberts",
  "Kevin Spacey",
  "George Clooney"]
```
For movies released in the `USA` with a `tomatoes.viewer.rating` greater than or equal to `3`, calculate a new field called `num_favs` that represets how many `favorites` appear in the `cast` field of the movie.

Sort your results by `num_favs`, `tomatoes.viewer.rating`, and `title`, all in descending order.

What is the `title` of the 25th film in the aggregation result?