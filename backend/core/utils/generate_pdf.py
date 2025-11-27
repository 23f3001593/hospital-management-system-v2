from reportlab.lib.pagesizes import A5
from reportlab.platypus import BaseDocTemplate,PageTemplate,Paragraph,Spacer,Frame,PageBreak,Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
from core.utils.format import format_slot_range

def add_page_number(canvas, doc):
    if getattr(doc, "disable_page_numbers", False):
        return
    pdf_page = canvas.getPageNumber()
    display_page = pdf_page - 1
    if display_page >= 1:
        canvas.setFont("Helvetica", 9)
        canvas.drawCentredString(doc.pagesize[0] / 2, 0.5 * inch, f"Page {display_page}")

def doctor_report(doctor, appointments, output_path):
    styles = getSampleStyleSheet()
    centered_large = ParagraphStyle("CenteredLarge", parent=styles["Heading1"], alignment=1, fontSize=22, leading=28)
    centered_medium = ParagraphStyle("CenteredMedium", parent=styles["Heading2"], alignment=1, fontSize=16, leading=20)
    centered_small = ParagraphStyle("CenteredSmall", parent=styles["Normal"], alignment=1, fontSize=16, leading=22)
    normal = styles["Normal"]
    bold = ParagraphStyle("Bold", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=12)
    doc = BaseDocTemplate(
        output_path,
        pagesize=A5,
        leftMargin=50,
        rightMargin=50,
        topMargin=60,
        bottomMargin=60
    )
    doc.disable_page_numbers = (len(appointments) == 0)
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id='frame'
    )
    template = PageTemplate(id='doctor_report', frames=frame, onPage=add_page_number)
    doc.addPageTemplates([template])
    story = []
    month_name = datetime.now().strftime("%B %Y")
    story.append(Spacer(1, 2.5 * inch))
    story.append(Paragraph(f"Monthly Report", centered_large))
    story.append(Paragraph(f"({month_name})", centered_large))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(f"{doctor.user.full_name}", centered_large))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(f"Department of {doctor.department.department_name}", centered_small))
    story.append(PageBreak())
    if not appointments:
        story.append(Paragraph("<b>No treatments recorded for this month.</b>", centered_medium))
    else:
        for appointment in appointments:
            treatment = appointment.treatment
            date_str = appointment.appointment_date.strftime("%d %B %Y")
            story.append(Spacer(1, 0.5 * inch))
            story.append(Paragraph(date_str, centered_medium))
            story.append(Spacer(1, 0.5 * inch))
            slot_range = format_slot_range(appointment.slot.slot_time)
            table_data = [[
                Paragraph(f"<b>Patient:</b> {appointment.patient.user.full_name}", normal),
                Paragraph(f"<b>Time:</b> {slot_range}", normal)
            ]]
            table = Table(table_data, colWidths=[doc.width*0.6, doc.width*0.4])
            table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(table)
            story.append(Spacer(1, 0.3 * inch))
            story.append(Paragraph("Treatment:", bold))
            story.append(Spacer(1, 0.2 * inch))
            details = (
                f"<b>Tests:</b> {treatment.tests or '—'}<br/><br/>"
                f"<b>Diagnosis:</b> {treatment.diagnosis or '—'}<br/><br/>"
                f"<b>Prescription:</b> {treatment.prescription or '—'}<br/><br/>"
                f"<b>Medicines:</b> {treatment.medicines or '—'}<br/><br/>"
                f"<b>Notes:</b> {treatment.notes or '—'}"
            )
            story.append(Paragraph(details, normal))
            story.append(PageBreak())
    doc.build(story)
    return output_path