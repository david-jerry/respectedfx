from __future__ import absolute_import

import os

import magic
from django.core.exceptions import ValidationError


def validate_uploaded_file(value, valid_mime_types, valid_file_extensions, error_message):
    file_mime_type = magic.from_buffer(value.read(2048), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError(error_message)
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError("Unacceptable file extension.")



# Usage for this function
# upload_image = models.FileField(
#     upload_to="images/",
#     validators=[
#         lambda f: validate_uploaded_file(
#             f,
#             ["image/svg+xml", "image/jpeg", "image/png"],
#             [".svg", ".jpg", ".png"],
#             "Unsupported image file type."
#         ),
#     ]
# )

# upload_pdf = models.FileField(
#     upload_to="pdfs/",
#     validators=[
#         lambda f: validate_uploaded_file(
#             f,
#             ["image/jpeg", "application/pdf"],
#             [".pdf", ".jpg"],
#             "Unsupported upload file type."
#         ),
#     ]
# )

# upload_zip = models.FileField(
#     upload_to="zips/",
#     validators=[
#         lambda f: validate_uploaded_file(
#             f,
#             ["application/x-7z-compressed", "application/gzip", "application/zip"],
#             [".zip", ".7z", ".gz"],
#             "Unsupported upload file type."
#         ),
#     ]
# )
