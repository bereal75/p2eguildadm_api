from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

print(f"This api is running on {settings.dcgdb_host}")

app = FastAPI()


retries = 0
while retries <= 2:
    try:
        # TODO has to be put into environment variables
        conn = psycopg2.connect(host=settings.dcgdb_host
                                , database = settings.dcgdb_dbname
                                , user = settings.dcgdb_user
                                , password = settings.dcgdb_pass
                                , cursor_factory=RealDictCursor )
        cursor = conn.cursor()
        print("Database connection established")
        break

    except Exception as error:
        print("Database connection could not be established!")
        print("Error: ", error)
        retries = retries + 1
        time.sleep(8 * retries)

class Person(BaseModel):
    personid: int
    firstname: Optional[str]
    lastname: Optional[str]
    tgusername: Optional[str]
    isadmin: Optional[bool]
    createdatetime:  Optional[datetime]


# get all persons
@app.get("/persons")
def get_persons():
    cursor.execute(""" SELECT * FROM public.person """)
    persons = cursor.fetchall()
    print(persons)
    return {"data": persons}

# Get admin persons
@app.get("/persons/admins", status_code=status.HTTP_200_OK)
def get_admin_person():
    cursor.execute("""SELECT * FROM public.person WHERE isadmin = TRUE """)
    persons = cursor.fetchall()
    print(persons)

    if not persons:
         # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no admin found. Contact your guild contact!")

    return {"data": persons}

# Get a specific person
@app.get("/persons/{personid}", status_code=status.HTTP_200_OK)
def get_personsbytgchatid(personid: int, response: Response):
    cursor.execute("""SELECT * FROM public.person WHERE personid = {0} """.format(personid))
    person = cursor.fetchone()
    print(person)

    if not person:
         # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"person with telegramchatid <{personid}> was not found!")

    return {"data": person}





# Create a person
@app.post("/persons", status_code=status.HTTP_201_CREATED)
def post_person(person: Person):
    cursor.execute("""INSERT INTO public.person (personid, firstname, lastname, tgusername) VALUES(%s, %s, %s,NULLIF(%s,'')) RETURNING * """,
                        (person.personid, person.firstname, person.lastname, person.tgusername))
    new_person = cursor.fetchone()
    conn.commit()
    return {"data": new_person}


# Delete a person
@app.delete("/persons/{personid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(personid: int, response: Response):
    cursor.execute("""DELETE FROM public.person WHERE personid = {0} RETURNING * """.format(personid))
    deleted_person = cursor.fetchone()
    conn.commit()    

    if deleted_person == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="person with id: {0} does not exist".format(personid))

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a person (isadmin cannot be updated via API)
@app.put("/persons/{personid}", status_code=status.HTTP_202_ACCEPTED)
def update_person(personid: int, person: Person):
    cursor.execute("""UPDATE public.person SET firstname = %s, lastname = %s, tgusername = %s WHERE personid = %s  RETURNING * """,
                        (person.firstname, person.lastname, person.tgusername, personid))
    updated_person = cursor.fetchone()
    conn.commit()

    if updated_person == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"person <{personid}> was not found!")

    return {"data": updated_person}


