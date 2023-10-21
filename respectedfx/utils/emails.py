from django.core.mail import EmailMessage

def send_email(to_email, subject, body, filepath=None, filename=None):
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
    if filepath or filename:
        with open(filepath, "rb") as file_data:
            # Determine the content type based on the file extension
            if filename.endswith('.pdf'):
                content_type = "application/pdf"
            else:
                content_type = "image/jpeg"  # Change to the appropriate image content type

            # Attach the file
            message.attach(filename, file_data.read(), content_type)

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
