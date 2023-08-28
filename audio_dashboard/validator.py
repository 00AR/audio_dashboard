from datetime import timedelta
import os
import magic
from django.core.exceptions import ValidationError
import mimetypes


def validate_is_audio_file(file):
    valid_mime_types = ['audio/mp3', 'audio/mpeg']
    file_mime_type = magic.from_buffer(file.read(2048), mime=True)
    if file_mime_type == "application/octet-stream":
        initial_pos = file.tell()
        file.seek(0)
        mime_type, _ = mimetypes.guess_type(file.name)
        file.seek(initial_pos)
        if mime_type is None or mime_type.split('/')[0] != 'audio':
            raise ValidationError('Unsupported file type')
    else:
        if file_mime_type not in valid_mime_types:
            raise ValidationError('Unsupported file type')
    valid_file_extensions = ['.mp3']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension')


def validate_duration_longer(duration):
    """Check if the duration of the audio is within 10 minutes limit"""
    if duration > timedelta(seconds=600):
        return False
    return True
