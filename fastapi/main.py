# Importing the necessary modules for the application to run.
from fastapi import FastAPI, Body, Depends
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session 

# Creating the database.
Base.metadata.create_all(engine)

#This creates a session, yields it to the caller, and then closes it when the caller is done
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Creating an instance of the FastAPI class.
app = FastAPI()

#Here I am initializing the CRUD operation for the DB
#Read operation 
@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items

#Read operation for specific id
@app.get("/{id}")
def getItem(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item

#Create operation
@app.post("/")
def addItem(item:schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

#Update operation
@app.put("/{id}")
def updateItem(id:int, item:schemas.Item, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject

#Delete operation
@app.delete("/{id}")
def deleteItem(id:int, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted...'