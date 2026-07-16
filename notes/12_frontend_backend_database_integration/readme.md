# Merging frontend + backend + psql

# Frontend Definition

A **frontend** is the part of a software application that **users directly interact with**. It is responsible for displaying information, receiving user input, and communicating those interactions to the backend.

## What the frontend does

- Displays the user interface (UI).
- Handles user interactions (clicks, typing, scrolling).
- Validates simple input (e.g., checking if an email field is empty).
- Sends requests to the backend (typically via HTTP APIs or WebSockets).
- Updates the interface with data received from the backend.

## Common frontend technologies

Frontends are commonly built using:

- HTML – Defines the structure of a webpage.
- CSS – Controls the appearance and layout.
- JavaScript or TypeScript – Adds interactivity and application logic.
- Frameworks and libraries such as React, Vue.js, Angular, and Svelte.

## Concise Definition

> **Frontend:** The client-side portion of an application that users see and interact with. It is responsible for presenting information, collecting user input, and communicating with the backend to access application data and services.


# Backend Definition

A **backend** is the part of a software application that **runs behind the scenes**, handling business logic, processing requests, managing data, and communicating with databases or other services. Users do not interact with it directly—they access it through the frontend.

## What the backend does

- Receives requests from the frontend.
- Executes application logic (business rules).
- Reads from and writes to databases.
- Authenticates and authorizes users.
- Communicates with external services or hardware.
- Returns responses to the frontend.

## Common backend technologies

Backends can be written in many languages and frameworks, including:

- Python (e.g., FastAPI, Django, Uvicorn)
- Java (e.g., Spring Boot)
- C# (e.g., ASP.NET Core)
- JavaScript/TypeScript (e.g., Node.js with Express)


## Concise Definition

> **Backend:** The server-side portion of an application that processes requests, executes application logic, manages data, communicates with databases and external systems, and provides services and data to the frontend.

# Software Architecture for login_project
<img src="./software_architecture.png" width="500">


## login_project Overview

This project is a simple full-stack application built for **user authentication (login/register)** and **time tracking (clock out system)**.
It allows employees to create an account with an email and password, then later they can login to their account to "clock in". When the employee is done with his shift he can press the "clock out" button, which will sign the employee out and log his work time. 

It uses:
- Backend: FastAPI (Python)
- Server: Uvicorn
- Frontend : React (running on http://localhost:5173)
- Database layer: Postgresql (handled inside `crud.py`)


# steps to get login_project to work
## Dependencies
* You can install docker and use dockerfile in [.devcontainer](../../.devcontainer/Dockerfile) and review [notes](../../notes/01_intro_psql/readme.md/)
* Install: node(for react), python and pip(then pip install uvicorn, fastapi, psycopg), postgresql 

## postgresql
1. ```cd ./notes/12_frontend_database/login_project/backend```
2. ```psql -h localhost -U postgres -f ./migration.sql```

## frontend 
1. ```cd ./notes/12_frontend_database/login_project/frontend```
2. ```npm i```
3. ```npm run dev```


# backend
1. In another terminal from frontend server:
2. ```cd ./notes/12_frontend_database/login_project/backend```
3. ```uvicorn app:app --reload```



# app.py code breakdown 
[app.py](./login_project/backend/app.py)


The backend is built using FastAPI and defines three main API endpoints:
- /login
- /register
- /clockout

It also configures CORS so the frontend can communicate with it.

---

# Code Breakdown

## 1. FastAPI App Initialization
```python
app = FastAPI()
```

Creates the backend server that handles HTTP requests.

---

## 2. CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This allows the frontend (React app) to send requests to the backend without browser blocking (CORS protection).

---

## 3. Data Models (Request Validation)(import pydantics)
```python
class User(BaseModel):
    email: str
    password: str
```
Used for:
- login
- register


```python
class ClockOut(BaseModel):
    email: str
    clock_in: str
    clock_out: str
```
Used for clock-out tracking.

FastAPI automatically validates incoming JSON using these models.

---

# API Endpoints

## /login
```python
@app.post("/login")
def login(user: User):
    success = login_(user.email, user.password)
    return {"success": success}
```
Flow:
1. Frontend sends email + password
2. Backend calls login_() from crud.py
3. crud.py checks credentials in database
4. Returns success or failure


## /register
```python
@app.post("/register")
def register(user: User):
    if user.email == "" or user.password == "":
        return {"success": False}

    success = register_(user.email, user.password)
    return {"success": success}
```

Flow:
1. Frontend sends email + password
2. Backend validates inputs (no empty fields)
3. Calls register_() in crud.py
4. Stores user in database
5. Returns success status

---

## /clockout
```python
@app.post("/clockout")
def clockout(data: ClockOut):
    clock_out_(data.email, data.clock_in, data.clock_out)
    return {"success": True}
```

Flow:
1. Frontend sends email + clock_in + clock_out
2. Backend calls clock_out_() in crud.py
3. Stores time session in database
4. Returns success

---

# crud.py Breakdown
[crud.py](./login_project/backend/crud.py)

The `crud.py` file is responsible for all interactions with the PostgreSQL database. The name CRUD stands for:

- Create
- Read
- Update
- Delete

Instead of placing SQL queries directly inside the API routes (`main.py`), they are separated into this file. This keeps the backend organized by separating application logic from database logic.

The three database operations implemented are:

- Login (Read)
- Register (Create)
- Clock Out (Create)

---

# Import Statement

```python
import psycopg2
```

`psycopg2` is the PostgreSQL driver for Python. It allows Python programs to:

- Connect to a PostgreSQL database.
- Execute SQL statements.
- Retrieve query results.
- Insert, update, and delete records.

Without this library, Python would not be able to communicate with PostgreSQL.

---

# Database Connection

```python
connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="hello1234"
)
```

This creates a connection to the PostgreSQL server.

Parameters:

- `host` – Location of the database server.
- `database` – Database to connect to.
- `user` – PostgreSQL username.
- `password` – PostgreSQL password.

The returned connection object is reused throughout the program whenever SQL queries need to be executed.

---

# Autocommit

```python
connection.autocommit = True
```

Normally, PostgreSQL requires every INSERT, UPDATE, or DELETE operation to be committed before the changes become permanent.

Setting

```python
connection.autocommit = True
```

causes every SQL statement to be committed automatically, eliminating the need to call:

```python
connection.commit()
```

after every modification.

---

# login_()

```python
def login_(email, password):
```

Purpose:

Checks whether a user with the given email and password exists in the database.

This is a Read operation.

---

## Step 1: Create Cursor

```python
cursor = connection.cursor()
```

A cursor is created from the database connection.

The cursor is responsible for executing SQL statements and retrieving query results.

Think of it as a temporary object used to "talk" to the database.

---

## Step 2: Execute SQL Query

```python
cursor.execute(
    """
    SELECT *
    FROM users
    WHERE email=%s
    AND password=%s
    """,
    (email, password)
)
```

This executes a parameterized SQL query.

The placeholders `%s` are replaced by:

```python
(email, password)
```

For example, if

```python
email = "alice@gmail.com"
password = "secret"
```

the query becomes

```sql
SELECT *
FROM users
WHERE email='alice@gmail.com'
AND password='secret';
```

Using placeholders prevents SQL injection attacks.

---

## Step 3: Retrieve Result

```python
user = cursor.fetchone()
```

`fetchone()` retrieves the first row returned by the query.

If a matching user exists:

```python
(3, "alice@gmail.com", "secret")
```

If no matching user exists:

```python
None
```

---

## Step 4: Close Cursor

```python
cursor.close()
```

Once the query has completed, the cursor is no longer needed and is closed to free resources.

---

## Step 5: Return Result

```python
return user is not None
```

This returns:

```python
True
```

if a user was found.

Otherwise it returns:

```python
False
```

---

# register_()

```python
def register_(email, password):
```

Purpose:

Creates a new user account.

This is a Create operation.

---

## Step 1: Create Cursor

```python
cursor = connection.cursor()
```

Creates a cursor for executing SQL statements.

---

## Step 2: Check if Email Already Exists

```python
cursor.execute(
    "SELECT * FROM users WHERE email=%s",
    (email,)
)
```

Searches the database for an existing user with the same email address.

Notice the comma:

```python
(email,)
```

This creates a one-element tuple.

Without the comma, Python would treat it as a string instead of a tuple.

---

## Step 3: Duplicate Check

```python
if cursor.fetchone():
    cursor.close()
    return False
```

If a row is returned:

- The email already exists.
- Registration fails.
- The function returns `False`.

---

## Step 4: Insert New User

```python
cursor.execute(
    """
    INSERT INTO users(email,password)
    VALUES(%s,%s)
    """,
    (email, password)
)
```

A new user record is inserted into the `users` table.

For example:

```sql
INSERT INTO users(email,password)
VALUES('alice@gmail.com','secret');
```

---

## Step 5: Close Cursor

```python
cursor.close()
```

The cursor is closed after the INSERT operation.

---

## Step 6: Return Success

```python
return True
```

Indicates that the new user was successfully created.

---

# clock_out_()

```python
def clock_out_(email, clock_in, clock_out):
```

Purpose:

Stores a user's work session in the database.

This is also a Create operation.

---

## Step 1: Create Cursor

```python
cursor = connection.cursor()
```

Creates a cursor for executing SQL.

---

## Step 2: Insert Time Log

```python
cursor.execute(
    """
    INSERT INTO timelog(email, clock_in, clock_out)
    VALUES(%s,%s,%s)
    """,
    (email, clock_in, clock_out)
)
```

Adds a new record to the `timelog` table.

Example:

```sql
INSERT INTO timelog(email, clock_in, clock_out)
VALUES(
    'alice@gmail.com',
    '08:00',
    '17:00'
);
```

---

## Step 3: Close Cursor

```python
cursor.close()
```

Closes the cursor after the INSERT completes.

---

## Step 4: Return Success

```python
return True
```

Returns `True` to indicate the operation completed successfully.


---

# Full Request Flow Example

## Login Example

1. User enters credentials in frontend
2. Frontend sends POST /login
3. Backend receives request and validates it
4. Backend calls login_()
5. Database verifies user
6. Response:
   { "success": true }
7. Frontend logs user in

---

## Clock-out Example

1. User clicks "Clock Out"
2. Frontend sends clock_in + clock_out data
3. Backend calls clock_out_()
4. Data is stored in database
5. Response:
   { "success": true }



# backend with javascript and express
Here I will link an example project that uses node/express/javascript to implement the backend instead of python with fastapi: [LINK](https://github.com/canizalesjaime/workshops/tree/main/docker-workshop/authentication)