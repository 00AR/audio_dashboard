from django.db import models

class User(models.Model):
    """User's detail"""

    username = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.username


class Audio(models.Model):
    """Metadata of the audio file"""

    file = models.FileField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date_of_upload = models.DateTimeField(null=False)
    size = models.IntegerField(null=False)
    extension = models.CharField(max_length=10, null=False)
    duration = models.DurationField()
    is_song = models.BooleanField() # shall we give a default value to be 0
    
    # if audio file is a Song, display more metadata
    artist = models.CharField(blank=True, max_length=200)
    album = models.CharField(blank=True, max_length=200)
    genre = models.CharField(blank=True, max_length=200)
    release_date = models.DateField(null=True)

    # def __str__(self):
    #     return self.title
