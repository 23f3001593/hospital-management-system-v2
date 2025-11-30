import csv
from io import StringIO
from datetime import date
from core.celery_app import celery
from core.models.models import User,Slot,Appointment,Treatment
from core.services.patient_services import PatientServices
from core.utils.send_email import send_email
from core.utils.format import format_slot_range

@celery.task(name="core.jobs.patient_jobs.send_appointment_reminders", bind=True)
def send_appointment_reminders(self):
    today = self.request.eta.date() if self.request.eta else date.today()
    appointments = Appointment.query.filter_by(appointment_date=today, status="booked").all()
    if not appointments:
        return "No appointments found."
    for appointment in appointments:
        patient = appointment.patient.user
        doctor = appointment.doctor.user
        department = appointment.doctor.department
        slot_range = format_slot_range(appointment.slot.slot_time)
        body = f"""
Hello {patient.full_name},

This is a reminder for your medical appointment scheduled today.

Date: {today.strftime("%d %B %Y")}
Time: {slot_range}
Doctor: {doctor.full_name}
Department: {department.department_name}

Please arrive 10-15 minutes early for a smooth check-in process.

Thank you,
MediFlow
"""
        send_email(
            recipient=patient.email,
            subject=f"Appointment Reminder - {doctor.full_name}, {today.strftime('%d %b %Y')}",
            body=body
        )
    return "Appointment reminders sent successfully."

@celery.task(name="core.jobs.patient_jobs.delete_stale_appointments", bind=True)
def delete_stale_appointments(self):
    today = self.request.eta.date() if self.request.eta else date.today()
    appointments = Appointment.query.filter_by(appointment_date=today, status="booked").all()
    if not appointments:
        return "No appointments found."
    for appointment in appointments:
        PatientServices.delete_appointment(appointment.appointment_id)
    return "Stale appointments deleted successfully."

@celery.task(name="core.jobs.patient_jobs.send_treatments_history")
def send_treatments_history(id):
    user = User.query.get(id)
    if not user or not hasattr(user, "patient") or not user.patient:
        return "Patient not found."
    if user.is_archived:
        return "Patient not found."
    treatments = (
        Treatment.query
        .join(Appointment, Treatment.appointment_id == Appointment.appointment_id)
        .join(Slot, Appointment.slot_id == Slot.slot_id)
        .filter(Appointment.patient_id == user.patient.patient_id)
        .order_by(
            Appointment.appointment_date.asc(),
            Slot.slot_time.asc()
        )
        .all()
    )
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow([
        "Date",
        "Time",
        "Department",
        "Doctor",
        "Tests",
        "Diagnosis",
        "Prescription",
        "Medicines",
        "Notes",
        "Fees (INR)"
    ])
    for treatment in treatments:
        writer.writerow([
            treatment.appointment.appointment_date.strftime("%d-%b-%Y"),
            format_slot_range(treatment.appointment.slot.slot_time),
            treatment.appointment.doctor.department.department_name,
            treatment.appointment.doctor.user.full_name,
            treatment.tests,
            treatment.diagnosis,
            treatment.prescription,
            treatment.medicines,
            treatment.notes,
            f"{treatment.appointment.doctor.fees:.2f}"
        ])
    csv_bytes = buffer.getvalue().encode("utf-8")
    buffer.close()
    subject = "Treatments History - CSV Export"
    body = f"""
Hello {user.full_name},

Please find the CSV file attached to this email for your treatment records.

Warm regards,
MediFlow
"""
    attachments = [{
        "filename": "treatments_history.csv",
        "content_type": "text/csv",
        "data": csv_bytes
    }]
    send_email(recipient=user.email, subject=subject, body=body, attachments=attachments)
    return f"Treatments history for Patient #{user.patient.patient_id} sent successfully."