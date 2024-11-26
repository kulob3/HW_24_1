from django.core.exceptions import ValidationError
import re

def validate_youtube_url(value):
    youtube_regex = re.compile(
        r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    )
    if not youtube_regex.match(value):
        raise ValidationError('Only YouTube URLs are allowed.')