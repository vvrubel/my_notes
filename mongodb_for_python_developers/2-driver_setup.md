[App Architecture](http://localhost:8888/notebooks/m220p_app_arch.ipynb)

# Running the Jupyter Notebooks
```
vasilevaaa@MacBook-Pro-Annas ~                                        [4:27:34]
(base) > $ cd test/mflix-python

vasilevaaa@MacBook-Pro-Annas ~/test/mflix-python                      [4:34:02]
(base) > $ conda activate mflix

vasilevaaa@MacBook-Pro-Annas ~/test/mflix-python                      [4:34:09]
(mflix) > $ cd notebooks
```
This lesson, as many lessons in this course, was created using a Jupyter Notebook. These notebooks facilitate a more modular approach to writing Python.

Jupyter was included in `requirements.txt`, so it should already be installed in your environment.

To open and run the notebooks in this course, navigate to the notebooks directory and launch the Jupyter notebook server:
```
cd mflix-python/notebooks
jupyter notebook
```
This should give you a URL link to the notebook server (this server is running on your machine), and you can paste it into your browser to view the notebooks. Navigate between cells in the notebook with the arrow keys. You can run each cell in the notebook with Shift-Enter. Feel free to edit the individual cells and re-run the notebook.

The SRV string in the notebooks will not work, because the demo Atlas cluster for this course has been shut off. Please replace this with your own connection string.

>
> [I 04:39:12.353 NotebookApp] Serving notebooks from local directory: /Users/vasilevaaa/test/mflix-python/notebooks
> [I 04:39:12.353 NotebookApp] The Jupyter Notebook is running at:
> [I 04:39:12.353 NotebookApp] http://localhost:8888/?token=84266b4005bc31ba846f87f9e1fa2a6b363a95c7fce37ac7
> [I 04:39:12.353 NotebookApp]  or http://127.0.0.1:8888/?token=84266b4005bc31ba846f87f9e1fa2a6b363a95c7fce37ac7
> [I 04:39:12.353 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
> [C 04:39:12.360 NotebookApp]
>
>    To access the notebook, open this file in a browser:
>        file:///Users/vasilevaaa/Library/Jupyter/runtime/nbserver-28757-open.html
>    Or copy and paste one of these URLs:
>        http://localhost:8888/?token=84266b4005bc31ba846f87f9e1fa2a6b363a95c7fce37ac7
>     or http://127.0.0.1:8888/?token=84266b4005bc31ba846f87f9e1fa2a6b363a95c7fce37ac7
> 

[MongoClient](http://localhost:8888/notebooks/MongoClient.ipynb)
```
from pymongo import MongoClient
uri = "mongodb+srv://m220student:m220password@cluster0.f5gcj.mongodb.net/test"
client = MongoClient(uri, connectTimeoutMS=200, retryWrites=True)
client.stats
>>> Database(MongoClient(host=['cluster0-shard-00-02.f5gcj.mongodb.net:27017', 'cluster0-shard-00-00.f5gcj.mongodb.net:27017', 'cluster0-shard-00-01.f5gcj.mongodb.net:27017'], document_class=dict, tz_aware=False, connect=True, authsource='admin', replicaset='atlas-jq5ziz-shard-0', ssl=True, connecttimeoutms=200, retrywrites=True), 'stats')
client.list_database_names()
>>> ['sample_airbnb',
 'sample_analytics',
 'sample_geospatial',
 'sample_mflix',
 'sample_restaurants',
 'sample_supplies',
 'sample_training',
 'sample_weatherdata',
 'admin',
 'local']
mflix = client.sample_mflix // or // mflix = client['sample_mflix']
# property accessors // vs // dictionary accessors
mflix.list_collection_names()
>>> ['movies', 'comments', 'users', 'sessions', 'theaters']
movies = mflix.movies
movies.count_documents({})
>>> 23530
```

## Chapter 1: Driver Setup

# Ticket: Projection

---

### Problem:

## User Story

"As a user, I'd like to be able to search `movies` by `country` and see a list of movie `titles`. I should be able to specify a `comma-separated list` of `countries` to search multiple countries."
---

### Task

Implement the `get_movies_by_country` method in `db.py` to search movies by country and use `projection` to return the `title` and `_id` field. The `_id` field will be returned by default.

You can find examples in [notebooks/your_first_read.ipynb](http://localhost:8888/notebooks/your_first_read.ipynb)

### MFlix Functionality

Once you complete this ticket, the UI will allow movie searches by one or more countries.

### Testing and Running the Application

Make sure to look at the tests in `test_projection.py` to understand what is expected.

You can run the unit tests for this ticket by running:

```
pytest -m projection
```
 
Once the unit tests are passing, run the application with:
```
python run.py
```
Now proceed to the status page to run the full suite of integration tests and get your validation code.

After passing the relevant unit tests, what is the validation code for Projection?
```python
def get_movies_by_country(countries):
    try:
        # here's an example of the find() query
        return list(db.movies.find(
            {"countries": {"$in": countries}},
            {"title": 1}
        ))
    except Exception as e:
        return e
```

# Ticket: Text and Subfield Search
### Problem:

## User Story

"As a user, I'd like to be able to search movies by cast members, genre, or perform a text search of the plot summary, full plot, and title."

### Task

For this ticket, you will need to modify the method build_query_sort_project in db.py to allow the following movie search criteria:

genres: finds movies that include any of the wanted genres.
Already, the build_query_sort_project method is able to return results for two different types of movie search criteria:

- text: performs a text search in the movies collection
- cast: finds movies that include any of the wanted cast

You just need to construct the query that queries the movies collection by the genres field.

### Hint

Check the implementation of similar formats of search criteria - the genres query should be similar.
## MFlix Functionality

Once you complete this ticket, the UI will allow movie searches by members of the cast, movie genres, movie title, and plot summary.

A text index was created for you when you restored the collections with mongorestore, so these queries will be performant once they are implemented.

esting and Running the Application

Make sure to look at the tests in test_text_and_subfield_search.py to understand what is expected.

You can run the unit tests for this ticket with:
```
pytest -m text_and_subfield_search
```
Once the unit tests are passing, run the application with:
```
python run.py
```
Now proceed to the status page to run the full suite of integration tests and get your validation code.

After passing the relevant tests, what is the validation code for Text and Subfield Search?


