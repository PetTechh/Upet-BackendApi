from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.petOwner import PetOwner
from models.notification import Notification
from schemas.notification import NotificationSchemaGet, NotificationSchemaPost

notifications = APIRouter()
tag = "Notifications"

endpoint = "/notifications"

@notifications.post(endpoint, response_model=NotificationSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_notification(notification: NotificationSchemaPost, db: Session = Depends(get_db)):
    pet_owner = db.query(PetOwner).filter(PetOwner.id == notification.petOwnerId).first()
    if not pet_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El propietario de mascota no existe.")
    
    new_notification = Notification(**notification.dict())
    db.add(new_notification)
    db.commit()
    return new_notification

@notifications.get(endpoint, response_model=list[NotificationSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_notifications(db: Session = Depends(get_db)):
    return db.query(Notification).all()

@notifications.get(endpoint + "/petowner/{petowner_id}", response_model=list[NotificationSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_notifications_by_petowner_id(petowner_id: int, db: Session = Depends(get_db)):
    pet_owner = db.query(PetOwner).filter(PetOwner.id == petowner_id).first()
    if not pet_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El propietario de mascota no existe.")
    
    notifications = db.query(Notification).filter(Notification.petOwnerId == petowner_id).all()
    
    if notifications == []:
        print("El propietario de mascota no tiene notificaciones.")
    
    return notifications