**JSON**, or *JavaScript Object Notation*, is the wildly popular standard for data interchange on the web, on which **BSON** (Binary JSON) is based.  
JavaScript objects are simple associative containers, wherein a string key is mapped to a value (which can be a number, string, function, or even another object).  

```
{
  "_id": 1,
  "name" : { "first" : "John", "last" : "Backus" },
  "contribs" : [ "Fortran", "ALGOL", "Backus-Naur Form", "FP" ],
  "awards" : [
    {
      "award" : "W.W. McDowell Award",
      "year" : 1967,
      "by" : "IEEE Computer Society"
    }, {
      "award" : "Draper Prize",
      "year" : 1993,
      "by" : "National Academy of Engineering"
    }
  ]
}
```  

*MongoDB stores data in BSON* format both internally, and over the network, but that doesn’t mean you can’t think of MongoDB as a JSON database. *Anything you can represent in JSON* can be natively stored in MongoDB, and retrieved just as easily in JSON.  
The following are some example documents (in JavaScript / Python style syntax) and their corresponding BSON representations.  
```{"hello": "world"}```  
> \x16\x00\x00\x00           // total document size  
> \x02                       // 0x02 = type String  
> hello\x00                  // field name  
> \x06\x00\x00\x00world\x00  // field value  
> \x00                       // 0x00 = type EOO ('end of object')  

```{"BSON": ["awesome", 5.05, 1986]}```  
> \x31\x00\x00\x00  
> \x04BSON\x00  
> \x26\x00\x00\x00  
> \x02\x30\x00\x08\x00\x00\x00awesome\x00  
> \x01\x31\x00\x33\x33\x33\x33\x33\x33\x14\x40  
> \x10\x32\x00\xc2\x07\x00\x00  
> \x00  
> \x00  

---  

|  | JSON | BSON |  
| Encoding | UTF-8 String | Binary |  
| Data Support | String, Boolean, Number, Array | String, Boolean, Number (Integer, Float, Long, Decimal128...), Array, Date, Raw Binary |   
| Readability | Human and Machine | Machine Only | 

--- 

One of the big attractions for developers using databases with JSON and BSON data models is the dynamic and flexible schema they provide when compared to the rigid, tabular data models used by relational databases.

Firstly, JSON documents are polymorphic – fields can vary from document to document within a single collection (analogous to table in a relational database). Documents make modeling diverse record attributes easy for developers, elegantly handling data of any structure.

Secondly, there is no need to declare the structure of documents to the database – documents are self-describing. Developers can start writing code and persist objects as they are created.

Thirdly, if a new field needs to be added to a document, it can be created without affecting all other documents in the collection, without updating a central system catalog and without taking the database offline. When you need to make changes to the data model, the document database continues to store the updated objects without the need to perform costly ALTER TABLE operations – or worse, having to redesign the schema from scratch.  

While a flexible schema is a powerful feature, there are situations where you might want more control over the data structure and content of your documents. Most document databases push enforcement of these controls back to the developer to implement in application code. However more advanced document databases provide schema validation, using approaches such as the [IETF JSON Schema standard](https://json-schema.org/) adopted by MongoDB.
