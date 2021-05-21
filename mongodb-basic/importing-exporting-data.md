Data in MongoDB *stored* in BSON but *viewed* in JSON.  
To learn more about other mongoimport supported formats [check out this documentation page](https://docs.mongodb.com/manual/reference/program/mongoimport/#compatibility).  

| JSON | BSON | what to do? | 
|---|---|---|  
| mongoimport | mongorestore | download data from cluster |  
| mongoexport | mongodump | upload data from local to cluster |
**URI** - Uniforn Recource Identifier.    
**SRV connection string** - a specific format used to establish a connection between your application and a MongoDB instance. [Click here to learn more](https://docs.mongodb.com/manual/reference/connection-string/#connections-dns-seedlist).  
> To connect to MongoDB
> ```
> mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"
> ```

```
mongodump --uri "mongodb+srv://<your username>:<your password>@<your cluster>.mongodb.net/<database>"
```
```
mongoexport --uri="mongodb+srv://<your username>:<your password>@<your cluster>.mongodb.net/<database>" --collection=<name> --out=<name.json>
```
```
mongorestore --uri "mongodb+srv://<your username>:<your password>@<your cluster>.mongodb.net/<database>"  --drop dump
```
```
mongoimport --uri="mongodb+srv://<your username>:<your password>@<your cluster>.mongodb.net/<database>" --drop <filename>.json
```
---

Atlas User Interface (UI) provides us with Data Explorer so that we can query data using the GUI.  
*Namespace* - The concatenation of the database name and collection name is called a namespace.  
The query must use valid JSON.  
Returned documents will contain the requested *field:value* pairs in them.
> We looked at the sample_training.zips collection and issued the following queries:  
> ```{"state": "NY"}```  
> ```{"state": "NY", "city": "ALBANY"}```  

In other way, you can query using Command line Interface of the shell.  
```
$ mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"
$ show databases
$ use sample_training
$ show collections  
$ db.zips.find({"state": "NY"})
$ it                                                         # iterates through the cursor
$ db.zips.find({"state": "NY"}).count()`                     # count a number od documents 
$ db.zips.find({"state": "NY", "city": "ALBANY"})`           # query more then one field
$ db.zips.find({"state": "NY", "city": "ALBANY"}).pretty()`  # show in pretty look
