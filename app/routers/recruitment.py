from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy import Boolean, desc, true
from sqlalchemy.orm import Session
from typing import List
import json

from ..database import get_db
from .. import models, schemas, utils


router = APIRouter()

@router.get("/recruitments/listids/{walletid}", status_code=status.HTTP_200_OK, response_model=List[schemas.RecruitmentId])
def get_recruitments(walletid: int, db: Session = Depends(get_db)):

    recruitment_query = db.query(models.Recruitment).filter(models.Recruitment.walletid == walletid )

    if recruitment_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no recruitments found.")
    else:
        recruitments = recruitment_query.all()

    return recruitments

# deletes all missions not completed (these are the missions that can be updated in the future. The rest will stay)
@router.delete("/recruitments/cleanup/{walletid}", status_code=status.HTTP_204_NO_CONTENT)
def cleanup_recruitments(walletid: int, db: Session = Depends(get_db)):
    wallet = db.query(models.Recruitment).filter(models.Recruitment.walletid == walletid).filter(models.Recruitment.missioncomplete == False)

    if wallet.first() != None:

        wallet.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/recruitments", status_code=status.HTTP_201_CREATED)
def post_recruitments(recruitments: schemas.RecruitmentBase, db: Session = Depends(get_db)):

    wallet = db.query(models.Recruitment).filter(models.Recruitment.walletid == recruitments.walletid).filter(models.Recruitment.recruitmentid == recruitments.recruitmentid)
    if wallet.first() == None:
        myrecruitments = models.Recruitment(**recruitments.dict())
        db.add(myrecruitments)
        db.commit()
        db.refresh(myrecruitments)
        return myrecruitments
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="recruitmentid {0} already registered".format(recruitments.recruitmentid))

    
