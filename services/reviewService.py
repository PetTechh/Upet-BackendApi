from fastapi import HTTPException
from models.review import Review

from sqlalchemy.orm import Session
from models.petOwner import PetOwner
from models.veterinarian import Veterinarian
from schemas.review import ReviewSchemaGet, ReviewSchemaPost
from sqlalchemy.orm import joinedload

class ReviewService:

    @staticmethod
    def create_new_review(petowner_id: int, vet_id: int, review: ReviewSchemaPost, db: Session):
        # Verificar si el petowner existe
        petowner = db.query(PetOwner).filter(PetOwner.id == petowner_id).first()
        if not petowner:
            raise HTTPException(status_code=404, detail="Petowner not found")

        # Verificar si el vet existe
        vet = db.query(Veterinarian).filter(Veterinarian.id == vet_id).first()
        if not vet:
            raise HTTPException(status_code=404, detail="Vet not found")
        
        # Crear la nueva reseña vinculada al petowner y al vet
        new_review = review.to_model(petowner_id, vet_id)
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return ReviewSchemaGet.from_orm(new_review)
    
    @staticmethod
    def get_all_reviews(db: Session) -> list[ReviewSchemaGet]:
        reviews = (
            db.query(Review)
            .options(joinedload(Review.petowner).joinedload(PetOwner.user))
            .all()
        )
        return [ReviewSchemaGet.from_orm(review) for review in reviews]
    
    @staticmethod
    def get_reviews_by_veterinarian_id(vet_id: int, db: Session) -> list[ReviewSchemaGet]:
            reviews = (
                db.query(Review)
                .filter(Review.veterinarian_id == vet_id)
                .options(joinedload(Review.petowner).joinedload(PetOwner.user))
                .all()
            )
            return [ReviewSchemaGet.from_orm(review) for review in reviews]