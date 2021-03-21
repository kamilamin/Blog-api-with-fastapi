from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {"data": {"name": "kamil"}}

@app.get('/about')
def about():
    return {"data": {"about": "This is about section"}}
