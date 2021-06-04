

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
```
{
  $group: {
    _id: {
      numDirectors: {
        $cond: [ { $isArray: "$directors" }, { $size: "$directors" }, 0 ]
         } 
       },
    numFilms:  { $sum: 1 },
    averageMetacritic: { $avg: "$metacritic" }
   }
 }
```