from django.core.mail import EmailMessage

def send_email(to_email, subject, body, attachment=None):
    # Common parameters for all emails
    common_params = {
        "body": body,
        "from_email": "info@respectedfx.com",
        "to": to_email,
        "bcc": ["newsletter@respectedfx.com"],
    }

    # Create an email message with a subject
    message = EmailMessage(subject=subject, **common_params)

    # Attach a PDF file if an attachment is provided
    if attachment:
        with open(attachment["filepath"], "rb") as file_data:
            message.attach(attachment["filename"], file_data.read(), "application/pdf")

    # Send the email
    message.content_subtype="html"
    message.send()

# Example usage:
# to_email = "recipient@example.com"
# subject = "Your subject"
# body = "<html><body>Your HTML content</body></html>"
# attachment = {
#     "filepath": "/path/to/your/file.pdf",
#     "filename": "attachment.pdf"
# }

# Send a plain email
# send_email(to_email, subject, body)

# Send an email with a PDF attachment
# send_email(to_email, subject, body, attachment)
