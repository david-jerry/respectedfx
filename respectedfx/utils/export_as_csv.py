import csv
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from respectedfx.newsletter.tasks import send_newsletter_mails

class ExportCsvPdfMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected Fields as CSV"

    def export_as_pdf(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename={meta}.pdf"

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        data = [field_names]
        for obj in queryset:
            data.append([str(getattr(obj, field)) for field in field_names])

        table = Table(data, colWidths=100, rowHeights=30)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(Paragraph(f"{meta} Data", getSampleStyleSheet()["Title"]))
        elements.append(table)

        doc.build(elements)

        return response

    export_as_pdf.short_description = "Export Selected Fields as PDF"

    def send_pdf_email(self, request, queryset, to_email):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename={meta}.pdf"

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        data = [field_names]
        for obj in queryset:
            data.append([str(getattr(obj, field)) for field in field_names])

        table = Table(data, colWidths=100, rowHeights=30)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(Paragraph(f"{meta} Data", getSampleStyleSheet()["Title"]))
        elements.append(table)

        doc.build(elements)

        body = "Please find the attached PDF file for the report this month."
        attachment = {
            "filepath": response,
            "filename": f"{meta}.pdf",
        }

        send_newsletter_mails.delay(to_email, f"PDF Export - {meta}", body, attachment)
        return HttpResponse("Email task added to Celery queue.")

    send_pdf_email.short_description = "Send PDF via Email"
