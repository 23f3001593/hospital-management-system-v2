import os
from datetime import date,time,timedelta
from tempfile import NamedTemporaryFile
from core.celery_app import celery
from core.extensions import db
from core.models.models import User,Doctor,Appointment,Slot
from core.utils.generate_pdf import doctor_report
from core.utils.send_email import send_email

@celery.task(name="core.jobs.doctor_jobs.update_slots")
def update_slots():
    doctors = Doctor.query.join(User).filter(User.is_archived==False).all()
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
    return "Slots updated successfully."

@celery.task(name="core.jobs.doctor_jobs.send_reports", bind=True)
def send_reports(self):
    today = self.request.eta.date() if self.request.eta else date.today()
    first_day_this_month = today.replace(day=1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = last_day_last_month.replace(day=1)
    # first_day_last_month = first_day_this_month
    # last_day_last_month = first_day_this_month.replace(day=30)
    doctors = Doctor.query.join(User).filter(User.is_archived==False).all()
    if not doctors:
        return "No doctor found."
    for doctor in doctors:
        appointments = (
            Appointment.query
            .join(Slot, Appointment.slot_id == Slot.slot_id)
            .filter(
                Appointment.doctor_id == doctor.doctor_id,
                Appointment.status == "completed",
                Appointment.appointment_date >= first_day_last_month,
                Appointment.appointment_date <= last_day_last_month
            )
            .order_by(
                Appointment.appointment_date.asc(),
                Slot.slot_time.asc()
            )
            .all()
        )
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            pdf_path = tmp_pdf.name
        pdf_path = doctor_report(doctor, appointments, pdf_path)
        subject = f"Monthly Report - {first_day_last_month:%B %Y}"
        body = f"""
Dear {doctor.user.full_name},

Please find attached your monthly treatment summary report for the period {first_day_last_month:%d %B %Y} to {last_day_last_month:%d %B %Y}.

Thank you for your service and dedication.
If you have any questions or require further information, please feel free to reach out.

Warm regards,
MediFlow
"""
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        attachments = [{
            "filename": f"monthly_report_{first_day_last_month:%B_%Y}.pdf".lower(),
            "content_type": "application/pdf",
            "data": pdf_bytes
        }]
        send_email(recipient=doctor.user.email, subject=subject, body=body, attachments=attachments)
        os.remove(pdf_path)
    return "Reports sent successfully."