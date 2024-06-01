from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.availability import Availability
from models.appointment import Appointment  # Importa la clase Appointment
from models.veterinarian import Veterinarian
from schemas.availability import AvailabilitySchema

class AvailabilityService:
    @staticmethod
    def create_availability(availability: AvailabilitySchema, db: Session):
        availability_db = Availability.from_orm(availability)
        db.add(availability_db)
        db.commit()
        return availability_db
    
    @staticmethod
    def create_weekly_availabilities(db: Session):
        today = datetime.now().date()
        start_of_week = today
        end_of_week = start_of_week + timedelta(days=(5 - today.weekday()))  # Sábado de esta semana

        # Obtener todos los veterinarios
        veterinarians = db.query(Veterinarian).all()

        for vet in veterinarians:
            # Obtener el horario de la clínica del veterinario
            clinic_start_time = vet.clinic.office_hours_start
            clinic_end_time = vet.clinic.office_hours_end

            # Crear horarios de disponibilidad para cada día de la semana, hasta el sábado
            for i in range((end_of_week - start_of_week).days + 1):
                date = start_of_week + timedelta(days=i)

                # Si el día actual no es domingo, crea el horario de disponibilidad
                availability = Availability(
                    date=date,
                    start_time=clinic_start_time,
                    end_time=clinic_end_time,
                    veterinarian_id=vet.id,
                    is_available=True
                )
                db.add(availability)

        db.commit()

    @staticmethod
    def delete_weekly_availabilities(db: Session):
        today = datetime.now().date()
        start_of_week = today
        end_of_week = start_of_week + timedelta(days=(5 - today.weekday()))  # Sábado de esta semana

        # Obtener todos los horarios de disponibilidad para la semana actual
        availabilities_to_delete = db.query(Availability).filter(Availability.date >= start_of_week, Availability.date <= end_of_week).all()

        # Eliminar los horarios de disponibilidad
        for availability in availabilities_to_delete:
            db.delete(availability)

        db.commit()