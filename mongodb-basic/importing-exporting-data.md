Data in MongoDB *stored* in BSON but *viewed* in JSON.  
To learn more about other mongoimport supported formats [check out this documentation page](https://docs.mongodb.com/manual/reference/program/mongoimport/#compatibility).  

| JSON | BSON | process |  
| mongoimport | mongorestore| download data from cluster |  
| mongoexport | mongodump | upload data from local to cluster |  

URI - Uniforn Recource Identifier. srv - establishes a secure connection.  
SRV connection string - a specific format used to establish a connection between your application and a MongoDB instance. [Click here to learn more](https://docs.mongodb.com/manual/reference/connection-string/#connections-dns-seedlist).  



---

```mongodump --uri "mongodb+srv://<your username>:<your password>@<your cluster>.mongodb.net/<database>"```

```mongoexport --uri="mongodb+srv://<your username>:<your password>@<your cluster>.mongodb.net/<database>" --collection=<name> --out=<name.json>```

```mongorestore --uri "mongodb+srv://<your username>:<your password>@<your cluster>.mongodb.net/<database>"  --drop dump```

```mongoimport --uri="mongodb+srv://<your username>:<your password>@<your cluster>.mongodb.net/<database>" --drop <filename>.json```

---
