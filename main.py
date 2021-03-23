from fastapi import FastAPI

app = FastAPI()

# @app is path operation decortor / Base path and get function
@app.get('/') 
def index(): #Path operation function
    return {'data': 'Blog list'}

# About path and get function 
@app.get('/blogs/{id}') #Path operation function
def fetchBlogsById(id):
    return {"data": id}

@app.get('/blogs/comments/{id}')
def getBlogComments(id):
    return {"data": {"1","2"}}

