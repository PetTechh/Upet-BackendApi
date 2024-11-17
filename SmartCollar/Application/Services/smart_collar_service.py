from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from SmartCollar.Domain.Models.smart_colllar_model import SmartCollar
from SmartCollar.Application.Schema.smart_collar_schema import SmartCollarRequest, SmartCollarResponse
from SmartCollar.Domain.ValueObject.location_type import LocationType
from models.pet import Pet

class SmartCollarService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_smart_collars(self) -> list[SmartCollarResponse]:
        collars = self.db.query(SmartCollar).all()

        collar_responses = []
        for collar in collars:
            location = LocationType(latitude=collar.latitude, longitude=collar.longitude)
            collar_responses.append(SmartCollarResponse(
                id=collar.id,
                serial_number=collar.serial_number,
                temperature=collar.temperature,
                lpm=collar.lpm,
                battery=collar.battery,
                location=location,
                pet_id=collar.pet_id
            ))

        return collar_responses


    def add_smart_collar(self, collar_data: SmartCollarRequest) -> SmartCollarResponse:
        try:
            location = LocationType(latitude=collar_data.location.latitude, longitude=collar_data.location.longitude)

            new_collar = SmartCollar(
                serial_number=collar_data.serial_number,
                temperature=collar_data.temperature,
                lpm=collar_data.lpm,
                battery=collar_data.battery,
                latitude=location.latitude,
                longitude=location.longitude,
                pet_id=None
            )

            self.db.add(new_collar)
            self.db.commit()
            self.db.refresh(new_collar)

            return SmartCollarResponse(
                id=new_collar.id,
                serial_number=new_collar.serial_number,
                temperature=new_collar.temperature,
                lpm=new_collar.lpm,
                battery=new_collar.battery,
                location=location, 
                pet_id=new_collar.pet_id
            )
        
        except IntegrityError as e:
            self.db.rollback()  # Rollback the transaction
            raise ValueError(f"Duplicate serial number: {collar_data.serial_number}. The collar already exists.") from e

    def delete_smart_collar(self, collar_id: int) -> bool:
        collar_to_delete = self.db.query(SmartCollar).filter(SmartCollar.id == collar_id).first()
        if collar_to_delete:
            self.db.delete(collar_to_delete)
            self.db.commit()
            return True
        return False

    def change_pet_association(self, collar_id: int, new_pet_id: int) -> SmartCollarResponse:
        collar = self.db.query(SmartCollar).filter(SmartCollar.id == collar_id).first()
        
        if not collar:
            raise NoResultFound(f"No collar found with id {collar_id}")
        
        # Verificar si el nuevo pet_id existe
        pet = self.db.query(Pet).filter(Pet.id == new_pet_id).first()
        if not pet:
            raise NoResultFound(f"No pet found with id {new_pet_id}")

        # Actualizar el pet_id
        collar.pet_id = new_pet_id
        self.db.commit()
        self.db.refresh(collar)

        return f"{pet.name} is now associated with collar {collar.serial_number}"