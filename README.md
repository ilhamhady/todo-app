# Todo App

---

## Requirement

This app is built based on Python 3 so you only need to make sure you did a Python installation and make sure what Python version is installed on your machine by running this terminal command

```
which python3
```

or

```
python3 --version
```

### Next Step

To run this app on your local machine, run this command `bash run.sh`

open the app on your browser at `http:\\localhost:5001`

1. If somehow you get an error related to python and pip you can check `run.sh` file

   - Modify the commands on `run.sh` by changing `python3` and `pip` to the Python and pip versions on your local machine.

2. If you get an error related to PORT you can check `run.sh` file

   - Modify the commands on `run.sh` by changing `--port=5001` to `--port=YOUR_PORT`

---

## Core classes, functions, and methods

In the code, there are several core classes, functions, and methods:

### Classes

1. **Flask Application Class**

   - `app` from `app.py`: Instance of the Flask class and represents the web application.

2. **Database Class**

   - `db` from `app.py`: Instance of the SQLAlchemy class and represents the database.

3. **User Class**

   - `User` from `models.py`: Represents a user in the application.

4. **Collection Class**

   - `Collection` from `models.py`: Represents a collection of tasks.

5. **Task Class**
   - `Task` from `models.py`: Represents a task in a collection.

### Methods

1. **User Methods**

   - `set_password(self, password)` from `models.py`: Sets the password for a user.
   - `check_password(self, password)` from `models.py`: Checks a password against the stored hash.

2. **Task Methods**
   - `start(self)` from `models.py`: Starts a task.
   - `pause(self)` from `models.py`: Pauses a task.
   - `complete(self)` from `models.py`: Completes a task.

### Functions

1. **Route Handlers**

   - `index()`: Renders the main page of the application.
   - `create_collection()`: Creates a new task collection.
   - `create_task(collection_id)`: Creates a new task in a specific collection.
   - `toggle_collection(collection_id)`: Toggles the 'enabled' status of a specific collection.
   - `start_task(task_id)`, `pause_task(task_id)`, `complete_task(task_id)`: Start, pause, and complete a specific task, respectively.
   - `delete_task(task_id)`, `delete_collection(collection_id)`: Delete a specific task or collection, respectively.
   - `signup()`: Handles user registration.
   - `signin()`: Handles user sign-in.
   - `signout()`: Handles user sign-out.
   - `close_popup()`: Closes a popup.
   - `set_timezone_offset()`: Sets the timezone offset.

2. **Helper Functions**
   - `get_local_time(utc_time)`: Converts a UTC time to local time using a timezone offset.
