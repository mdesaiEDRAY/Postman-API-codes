# This is importing the FastAPI module, the Body module, the Depends module, the schemas module, the
# models module, the Base, engine, SessionLocal module, and the Session module.
from fastapi import FastAPI, Body, Depends
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

#This will create our database if it doesent already exists
Base.metadata.create_all(engine)

#This creates a session, yields it to the caller, and then closes it when the caller is done
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Creating a new FastAPI app.
app = FastAPI()

# Creating a fake database. Basically a dictionary with keys and values.
fakeDatabase = {
    1:{'task':'Clean Car'},
    2:{'task':'Write Blog'},
    3:{'task':'Start Stream'}
}

#Get Request (Read)

#Fake DB
@app.get("/{id}")
def getItem(id:int):
    return fakeDatabase[id]
#Real DB
"""@app.get("/{id}")
def getItem(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item"""

# Post Request (Create)
@app.post("/")
def addItem(item:schemas.Item, session = Depends(get_session)):
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

#Put Request (Update)
@app.put("/{id}")
def updateItem(id:int, item:schemas.Item, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject

#Delete Request (Delete)
@app.delete("/{id}")
def deleteItem(id:int, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted'
