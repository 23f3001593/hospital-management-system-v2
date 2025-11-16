from datetime import time
from core.celery_app import celery
from core.extensions import db
from core.models.models import User,Doctor,Slot

@celery.task(name="core.jobs.doctor_jobs.update_doctor_slots")
def update_doctor_slots():
    doctors = Doctor.query.join(User).filter(User.is_archived==False, Doctor.is_availability_updated==True).all()
    if not doctors:
        return "No doctor found."
    forenoon_times = [time(10,0), time(11,0), time(12,0)]
    afternoon_times = [time(16,0), time(17,0), time(18,0)]
    for doctor in doctors:
        availabilities = {availability.week_day: availability for availability in doctor.availabilities}
        for week_day, availability in availabilities.items():
            for t in forenoon_times:
                slot = Slot.query.filter_by(doctor_id=doctor.doctor_id, week_day=week_day, slot_time=t).first()
                if slot:
                    slot.status = "available" if availability.forenoon_slot else "unavailable"
            for t in afternoon_times:
                slot = Slot.query.filter_by(doctor_id=doctor.doctor_id, week_day=week_day, slot_time=t).first()
                if slot:
                    slot.status = "available" if availability.afternoon_slot else "unavailable"
    db.session.commit()
    return "Doctor slots updated successfully."