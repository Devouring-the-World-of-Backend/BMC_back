from fastapi import FastAPI
from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    published_year: int
    
app = FastAPI()

@app.get("/")
def root():
    return "Hello Library!"