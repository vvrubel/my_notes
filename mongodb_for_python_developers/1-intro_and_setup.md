```
mongodb+srv://m220student:m220password@cluster0.f5gcj.mongodb.net/test
```

We are going to have series of README instructions to be able to setup our MFLIX application successfully. With MFLIX application, you will learn to create and share a database connection, perform the basic Create, Read, Update, and Delete operations through the driver, handle errors, utilize the MongoDB best practices and more.

Mflix is composed of two main components:

Frontend: All the UI functionality is already implemented for you, which includes the built-in React application that you do not need to worry about.
Backend: The project that provides the necessary service to the application. The code flow is already implemented except some functions.
You'll only be implementing the functions which directly call to MongoDB.

# Database Layer
We will be using MongoDB Atlas, MongoDB's official Database as a Service (DBaaS), so you will not need to manage the database component yourself. However, you will still need to install MongoDB locally to access the command line tools that interact with Atlas, to load data into MongoDB and potentially do some exploration of your database with the shell.

The following README sections are here to get you setup for this course.

# Setting Up mflix:
Project Structure
Local Development Environment Configuration
Python Library Dependencies
Running the Application
Running the Unit Tests
In order to run properly, the MFlix software project has some installation requirements and environmental dependencies.

These requirements and dependencies are defined in this lesson, and they can also be found in the README.rst file from the mflix-python project, which you will download shortly. This lesson serves as a guide for setting up these necessary tools. After following this README, you should be able to successfully run the MFlix application. First, you will need to download the mflix-python project, as described below.

Download the mflix-python.zip file
You can download the mflix-python.zip file by clicking the link in the "Handouts" section of this page. Downloading this handout may take a few minutes. When the download is complete, unzip the file and cd into the project's root directory, mflix-python.

# Project Structure
Everything you will implement is located in the mflix/db.py file, which contains all database interfacing methods. The API will make calls to db.py to interact with MongoDB.

The unit tests in tests will test these database access methods directly, without going through the API. The UI will run these methods in integration tests, and therefore requires the full application to be running.

The API layer is fully implemented, as is the UI. If you need to run on a port other than 5000, you can edit the index.html file in the build directory to modify the value of window.host.

Please do not modify the API layer in any way, movies.py and user.py under the mflix/api directory. Doing so will most likely result in the frontend application failing to validate some of the labs.

# Local Development Environment Configuration
## Anaconda
We're going to use Anaconda to install Python 3 and to manage our Python 3 environment.

### Installing Anaconda for Mac

You can download Anaconda from their MacOS download site. The installer will give you the option to "Change Install Location", so you can choose the path where the anaconda3 folder will be placed. Remember this location, because you will need it to activate the environment.

Once installed, you will have to create and activate a conda environment:
```
# navigate to the mflix-python directory
cd mflix-python

# enable the "conda" command in Terminal
echo ". /anaconda3/etc/profile.d/conda.sh" >> ~/.bash_profile
source ~/.bash_profile

# create a new environment for MFlix
conda create --name mflix

# activate the environment
conda activate mflix

# You can deactivate the environment with the following command:
conda deactivate
```


## Virtualenv
Note: If you installed Anaconda instead, skip this step.

As an alternative to Anaconda, you can also use virtualenv, to define your Python 3 environment. You are required to have a Python 3 installed in your workstation.

You can find the virtualenv installation procedure on the PyPA website.

Once you've installed Python 3 and virtualenv, you will have to setup a virtualenv environment:

navigate to the mflix-python directory
```
cd mflix-python
```
create the virtual environment for MFlix
```
virtualenv -p YOUR_LOCAL_PYTHON3_PATH mflix_venv
```
activate the virtual environment
```
source mflix_venv/bin/activate
```
You can deactivate the virtual environment with the following command:
```
deactivate
 ```
# Python Library Dependencies
Once the Python 3 environment is activated, we need to install our python dependencies. These dependencies are defined in the requirements.txt file, and can be installed with the following command:
```
pip install -r requirements.txt
```
# Running the Application
In the mflix-python directory you can find a file called dotini.

Open this file and enter your Atlas SRV connection string as directed in the comment. This is the information the driver will use to connect. Make sure not to wrap your Atlas SRV connection between quotes:
```
MFLIX_DB_URI = mongodb+srv://m220student:m220password@cluster0.f5gcj.mongodb.net/test
```
To start MFlix, run the following command:
```
python run.py
```
This will start the application. You can then access the MFlix application at http://localhost:5000/.

# Running the Unit Tests
To run the unit tests for this course, you will use pytest and needs to be run from mflix-python directory. Each course lab contains a module of unit tests that you can call individually with a command like the following:
```
pytest -m LAB_UNIT_TEST_NAME
```
Each ticket will contain the command to run that ticket's specific unit tests. For example to run the Connection Ticket test your shell command will be:
```
pytest -m connection
```