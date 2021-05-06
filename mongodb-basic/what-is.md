# What is MongoDB?
MongoDB is a *__NoSQL__ database*.  
There can be many collections per database and many documents per collection.  

**Collection** - an organized store of documents in MongoDB usually with common fields between documents.  
**Document** - a way to organize and store data as a set of *field-value pairs*.  
**Field** - a unique identifier for a datapoint.  
**Value** - data related to a given identifier.   

---

# What is MongoDB Atlas?
**Cluster** - group of servers that store your data.  
**Replica Set** - a few connected MongoDB instances that store the same data.    
**Instance** - a single machine locally or in the cloud running the a certain software (MongoDB).  
Single cluster in Atlas automatically configured as a replica set.  

Since you've set up an Atlas cluster, you can access to the content through the *User Interface (UI)* or 
connect to it from the shell using the *in-browser Interactive Development Environment (in-browser IDE)*.
There are two ways to connect from the shell:  

> 1. in general: ```mongo "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/admin"```  
> or in our case: ```mongo "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.8h1hn.mongodb.net/admin"```  
>  
> 2. ```mongo "mongodb+srv://sandbox.8h1hn.mongodb.net/myFirstDatabase" --username m001-student```  
> when you will be prompted, pass the password: ```m001-mongodb-basics```  

