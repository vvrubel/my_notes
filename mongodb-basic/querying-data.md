Atlas User Interface (UI) provides us with Data Explorer so that we can query data using the GUI.  
*Namespace* - The concatenation of the database name and collection name is called a namespace.  
Quiery must use valid JSON.  
Returned documents will contain the requested *field:value* pairs in them. 

> We looked at the sample_training.zips collection and issued the following queries:  
> ```{"state": "NY"}```
> ```{"state": "NY", "city": "ALBANY"}```  

---

Also you can query using Command line Interface of the shell.  

`mongo "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/admin"`  # connect to the Atlas cluster

`show dbs`  # show the list of database   

`use sample_training`  # choose the database  

`show collections`  # show the list of collections  

`db.zips.find({"state": "NY"})`  # choose the collection  

`it`  # iterates through the cursor

`db.zips.find({"state": "NY"}).count()`  # count a number od documents 

`db.zips.find({"state": "NY", "city": "ALBANY"})`  # query more then one field

`db.zips.find({"state": "NY", "city": "ALBANY"}).pretty()`  # show in pretty look
