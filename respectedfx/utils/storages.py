from storages.backends.s3 import S3Storage


class StaticS3Storage(S3Storage):
    location = "static"
    default_acl = "public-read"


class MediaS3Storage(S3Storage):
    location = "media"
    default_acl = "public-read"
    file_overwrite = False

class PrivateMediaStorage(S3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
