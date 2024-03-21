# Project Title:

URL Scissors ✂️ With FastAPI and Python

## 1. What is the project?

We have built a fully functional FastAPI-driven Python web app that creates shortened URLs that forward to target URLs. URLs can be extremely long and not user-friendly. This is where a URL Scissors can come in handy. Url Scissors reduces the number of characters in a URL, making it easier to read, remember, and share.

## 2. Tech Stack:

- Swagger UI
- Python 3
- FastAPI
- Postgresql
- SQLAlchemy
- Uvicorn server
- Render Deployment/DB

## 3. Project Dependencies (env file):

- .env file

```
ENV_NAME="XXXXXXXX"
BASE_URL="http://127.0.0.1:XXXX"
DB_URL="postgresql://<user>:<password>@<localhost>:<port>/<db_name>"
```

## 4. Installing:

i. Clone the git repo

```
git clone https://github.com/Eze-Tg/Url-Scissors-Project-With-FastApi-and-Python.git
```

ii. Open project folder and create virtual environment
```commandline
$ python3 -m venv .env
```

iii. Install dependencies

```commandline
(venv) $ pip install -r requirements.txt
```

iv. Explore

😎

## 5. How To Use:

i. Open project in preferred IDE. I'm using VsCode.

ii. cd to the project folder

```commandline
(venv) $ cd app
```
ii. Run the live server using uvicorn.

```commandline
(venv) $ uvicorn main:app --reload
```

## TO Deploy on Render

i. uvicorn main:app --host 0.0.0.0 --port 8080

- Create SQLite database

> When the server restarted, sqlalchemy automatically created your database in the location that you defined in your DB_URL environment variable. If you used sqlite:///./shortener.db as the value of DB_URL, then there should be a file named shortener.db in the root directory of your project now. That’s your SQLite database!

iii. Open "http://127.0.0.1:8000/docs" in any web browser

## 6. Demo:

![This is an image](screenshot.jpeg)

## 7. Contributing:

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 7. Awaiting Tasks:
- Users to be able to see history of previous shortened urls
- Users SHould be able to login

