from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy import Boolean, desc, true
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas, utils

router = APIRouter()

# get all persons
@router.get("/persons", status_code=status.HTTP_200_OK, response_model=List[schemas.Person])
def get_persons(db: Session = Depends(get_db)):
    persons = db.query(models.Person).all()
    return persons  


# Get a specific person
@router.get("/persons/{personid}", status_code=status.HTTP_200_OK, response_model=schemas.Person)
def get_personsbytgchatid(personid: int, db: Session = Depends(get_db)):

    person = db.query(models.Person).filter(models.Person.personid == personid).first()

    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"person with telegramchatid <{personid}> was not found!")

    return person


# Create a person
@router.post("/persons", status_code=status.HTTP_201_CREATED, response_model=schemas.Person)
def post_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):

    new_person = models.Person(**person.dict())
    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return new_person


   


# Delete a person
@router.delete("/persons/{personid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(personid: int, db: Session = Depends(get_db)):

    person = db.query(models.Person).filter(models.Person.personid == personid)
    
    if person.first() == None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="person with id: {0} does not exist".format(personid))

    person.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a person (isadmin cannot be updated via API)
@router.put("/persons/{personid}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Person)
def update_person(personid: int, updated_person: schemas.PersonUpdate, db: Session = Depends(get_db)):
    
    person_query = db.query(models.Person).filter(models.Person.personid == personid)

    persontoupdate = person_query.first()

    if persontoupdate == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"person <{personid}> was not found!")    

    person_query.update(updated_person.dict(), synchronize_session=False)
    db.commit()

    return person_query.first()