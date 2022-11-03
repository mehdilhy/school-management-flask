# School Management System API

Heroku Link: https://my-school-udacity.herokuapp.com/

Local : http://localhost:5000

## Motivation for Project

This project is a school management system API that allows users to view, add, update and delete students, teachers ,classes and subjects. The API is built using Flask and SQLAlchemy.

This READMe file contains instructions on how to run the project locally and how to run the tests.

It doesn't contain complete documentation of the API endpoints. This is a capstone project and the focus is to show the ability to build a RESTful API using Flask and SQLAlchemy and having it well tested and documented + the ability to deploy the API to Heroku and using RBAC to secure the API.


## Getting Started

### Installing Dependencies

#### Python 3.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment

Recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

## Running the server

To run the server, execute:

```bash
export DATABASE_URL=<database-connection-url>
export FLASK_APP=app.py
flask run --reload
```

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application.

Using the `--reload` flag will detect file changes and restart the server automatically.

## API Reference

## Getting Started

Base URL: This application can be run locally. The hosted version is at `https://my-school-udacity.herokuapp.com/`.

Authentication: This application requires authentication to perform various actions. All the endpoints require
various permissions, except the root (or health) endpoint, that are passed via the `Bearer` token.

The application has three different types of roles:

- Student
  - has `get:class get:result get:student get:subject get:subjects` permissions
- Teacher
  - has `get:class get:result get:student get:subject get:subject post:class post:result get students get:teachers get:teacher get:classes get:results patch:subject patch:result delete:result`
- Admin
  - can perform all the CRUD operations on all the resources

## Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "error": 404,
    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
    "success": false
}
```

The API will return the following errors based on how the request fails:

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 405: Method Not Allowed
- 422: Unprocessable Entity
- 500: Internal Server Error

## Endpoints

#### GET /

- General

  - root endpoint
  - can also work to check if the api is up and running
  - is a public endpoint, requires no authentication

- Sample Request
  - `https://my-school-udacity.herokuapp.com/`

<details>
<summary>Sample Response</summary>

```
{"error":404,"message":"resource not found","success":false}
```

</details>

#### GET /students

- General

  - gets the list of all the students
  - requires `get:students` permission

- Sample Request
  - `https://my-school-udacity.herokuapp.com/students`

<details>
<summary>Sample Response</summary>

```
{
  "students": [
    {
      "age": 12,
      "class": 2,
      "id": 6,
      "name": "medos"
    },
    {
      "age": 12,
      "class": 2,
      "id": 8,
      "name": "Jack"
    },
    {
      "age": 10,
      "class": 2,
      "id": 10,
      "name": "Speed"
    },
    {
      "age": 10,
      "class": 2,
      "id": 11,
      "name": "Pie Face"
    }
  ],
  "success": true
}
```

</details>

#### GET /students/{student_id}

- General

  - gets the complete info for an student
  - requires `get:student` permission

- Sample Request
  - `https://my-school-udacity.herokuapp.com/students/6`

<details>
<summary>Sample Response</summary>

```
{
  "student": {
    "age": 12,
    "class": 2,
    "id": 6,
    "name": "medos"
  },
  "success": true
}
```

</details>

#### POST /students

- General

  - creates a new student
  - requires `post:student` permission

- Request Body

  - name: string, required
  - age: integer, required
  - class_id: integer, required

- Sample Request
  - `https://my-school-udacity.herokuapp.com/students`
  - Request Body
    `{ "age": 12, "class_id": 2, "name": "new mehdi" } `

<details>
<summary>Sample Response</summary>

```
{
  "student": {
    "age": 12,
    "class": 2,
    "id": 12,
    "name": "new mehdi"
  },
  "success": true
}
```

</details>

#### PATCH /students/{student_id}

- General

  - updates the info for an student
  - requires `patch:students` permission

- Request Body (at least one of the following fields required)

  - name: string, optional
  - age: number, optional
  - class_id: number, optional

- Sample Request
  - `https://my-school-udacity.herokuapp.com/students/2`
  - Request Body
    ```
      {
           "name":"neew"
      }
    ```

<details>
<summary>Sample Response</summary>

```
{
  "student": {
    "age": 12,
    "class": 2,
    "id": 6,
    "name": "neew"
  },
  "success": true
}
```

</details>

#### DELETE /students/{student_id}

- General

  - deletes the student
  - requires `delete:student` permission

- Sample Request
  - `https://my-school-udacity.herokuapp.com/students/6`

<details>
<summary>Sample Response</summary>

```
{
  "student": 6,
  "success": true
}
```

</details>

#### GET /teachers

- General

  - gets the list of all the teachers
  - requires `get:teachers` permission

- Sample Request
  - `https://my-school-udacity.herokuapp.com/teachers`

<details>
<summary>Sample Response</summary>

```
{
  "success": true,
  "teachers": [
    {
      "address": "test",
      "email": "medos",
      "id": 1,
      "name": "mehdi",
      "phone": "123"
    },
    {
      "address": "hello",
      "email": "medos@gmail.com",
      "id": 2,
      "name": "Hamid",
      "phone": "0657483"
    },
    {
      "address": "hello",
      "email": "medos@gmail.com",
      "id": 3,
      "name": "Hamid",
      "phone": "0657483"
    },
    {
      "address": "hello",
      "email": "medos@gmail.com",
      "id": 4,
      "name": "Hamid",
      "phone": "0657483"
    }
  ]
}
```

</details>

#### GET /teachers/{teacher_id}

- General

  - gets the complete info for a teacher
  - requires `get:teacher` permission

- Sample Request
  - `https://my-school-udacity.herokuapp.com/teachers/2`

<details>
<summary>Sample Response</summary>

```
{
  "success": true,
  "teacher": {
    "address": "hello",
    "email": "mehdilhy@gmail.com",
    "id": 2,
    "name": "Hamid",
    "phone": "0657483"
  }
}
```

</details>

#### POST /teachers

- General

  - creates a new teacher
  - requires `post:teacher` permission

- Request Body

  - name: string, required
  - email: string, required
  - phone: string, required
  - address: string, required
  - class_id: integer, optional

- NOTE

  - class_id if passed must be in request body must already exist in the database prior to making this request.
  - If not, the request will fail with code 422.

- Sample Request
  - `https://my-school-udacity.herokuapp.com/post`
  - Request Body
    `{ "address": "Rube Ha le ", "email": "medso@gmail.com", "name": "Hamid", "phone": "0657483" } `

<details>
<summary>Sample Response</summary>

```
{
  "success": true,
  "teacher": {
    "address": "Rube Ha le ",
    "email": "medso@gmail.com",
    "id": 5,
    "name": "Hamid",
    "phone": "0657483"
  }
}
```

</details>

#### PATCH /teacher/{teacher_id}

- General

  - updates the info for a teacher
  - requires `patch:teachers` permission

- Request Body (at least one of the following fields required)

  - name: string, optional
  - email: string, optional
  - phone: string, optional
  - address: string, optional
  - class_id: integer, optional

- NOTE

  - Value passed in the `class_id` in request body will completely replace the existing relationship.
  - So, if you want to affect a teacher to a class, you must pass the `class_id` in the request body.

- Sample Request
  - `https://my-school-udacity.herokuapp.com/teachers/6`
  - Request Body
    `{ "address": "The moon" } `

<details>
<summary>Sample Response</summary>

```
{
  "success": true,
  "teacher": {
    "address": "The moon",
    "email": "medso@gmail.com",
    "id": 6,
    "name": "Hamid",
    "phone": "0657483"
  }
}
```

</details>

#### DELETE /teachers/{teacher_id}

- General

  - deletes the teacher
  - requires `delete:teacher` permission
  - will delete class to teacher relationship if any

- Sample Request
  - `https://my-school-udacity.herokuapp.com/teachers/3`

<details>
<summary>Sample Response</summary>

```
{
    "teacher": 3,
    "success": true
}
```

</details>

## Testing

For testing the backend, run the following commands (in the exact order):

```
dropdb my-school-test
createdb my-school-test
python test.py
```

The database will be automatically populated with some dummy data using `faker` library.
