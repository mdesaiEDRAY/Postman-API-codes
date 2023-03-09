#Run this fake DB using the following command : uvicorn fakemain:app --reload

from fastapi import FastAPI


app = FastAPI()


fakedatabase = {
    1: {'task1' : 'red car'},
    2: {'task2' : 'blue car'},
    3: {'task3' : 'green car'}
}

@app.get("/")
def getItems():
    return fakedatabase
