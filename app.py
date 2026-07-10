from fastapi import FastAPI
import sqlite3
import redis

app = FastAPI()

r = redis.Redis(host="redis", port=6379, decode_responses=True)


def create_database():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


create_database()


@app.get("/")
def home():

    r.incr("api_requests")

    return {
        "message": "Employee Task Manager"
    }


@app.get("/health")
def health():

    return {
        "status": "UP"
    }


@app.get("/stats")
def stats():

    return {
        "api_requests": r.get("api_requests")
    }


@app.get("/tasks")
def get_tasks():

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    data = cursor.fetchall()

    conn.close()

    r.incr("api_requests")

    return data


@app.post("/tasks")
def create_task(title: str, status: str):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks(title,status) VALUES(?,?)",
        (title, status)
    )

    conn.commit()
    conn.close()

    r.incr("api_requests")

    return {
        "message": "Task Created"
    }


@app.put("/tasks/{task_id}")
def update_task(task_id: int, status: str):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (status, task_id)
    )

    conn.commit()
    conn.close()

    r.incr("api_requests")

    return {
        "message": "Task Updated"
    }


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    r.incr("api_requests")

    return {
        "message": "Task Deleted"
    }