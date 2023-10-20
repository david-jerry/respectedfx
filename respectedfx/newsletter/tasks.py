from celery import shared_task

from respectedfx.utils.emails import send_email

# attachment = {
#     "filepath": "/path/to/your/file.pdf",
#     "filename": "attachment.pdf"
# }

@shared_task(bind=True)
def send_newsletter_mails(self, to_email, subject, body, attachment=None):
    send_email(to_email, subject, body, attachment)
