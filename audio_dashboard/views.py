from django.shortcuts import render
from . import forms
from .models import Audio, User
from datetime import datetime, timedelta
from django.shortcuts import redirect
import mutagen
from .validator import validate_duration_longer


def demo_login_required(view):
    def inner(request):
        user_id = request.session.get("user")
        try:
            request.user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect("index")
        return view(request)
    return inner


def demo_login(request, user):
    request.session["user"] = user.id


def index(request):
    """ Asks for the login details """
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user, _ = User.objects.get_or_create(username=form.cleaned_data["username"])
            demo_login(request, user)
            return redirect("user_home")
    else:
        form = forms.LoginForm()
    return render(request, "index.html", { "form": form })


@demo_login_required
def user_home(request):
    """Dashboard which allows the user to upload and view uploaded files"""
    user = request.user
    if request.method == "POST":
        form = forms.MultiUploadAudioForm(request.POST, request.FILES)
        if form.is_valid():
            instances = []
            is_valid = False
            for file in request.FILES.getlist("files"):
                metadata = extract_metadata(file)
                is_valid = validate_duration_longer(metadata.get("duration", 0))
                if not is_valid:
                    form.add_error("files", "Unable to upload! Audio file duration exceeded 10 minutes")
                    break
                instances.append(Audio(
                    file=file,
                    user=user,
                    title=metadata.get('title', "Untitled"),
                    date_of_upload=datetime.now(),
                    size=metadata.get('filesize'),
                    extension=metadata.get('extension'),
                    duration=metadata.get('duration'),
                    is_song=metadata.get('is_song'),
                    artist=metadata.get('artist') or "",
                    album=metadata.get('album') or "",
                    genre=metadata.get('genre') or "",
                    release_date=metadata.get('release_date')
                ))
            if is_valid and instances:
                Audio.objects.bulk_create(instances)
    else:
        form = forms.MultiUploadAudioForm()
    audio_list = Audio.objects.filter(user=user).order_by("-date_of_upload")
    context = {
        "audio_list": audio_list,
        "form": form,
    }
    return render(request, "user_home.html", context)


def extract_metadata(file):
    """
        Extract all the required metadata from audio file. Also 
        makes the checks such as if the filetype is audio and 
        if the duration is not longer than 10 minutes
    """
    tags = mutagen.File(file)
    metadata = {}

    if tags is not None:
        # title
        # Check if the 'title' metadata exists in the tags
        if 'title' in tags:
            metadata['title'] = tags['title'][0]
        elif 'TIT2' in tags:
            metadata['title'] = tags['TIT2'][0]
        elif tags.filename:
            metadata['title'] = tags.filename

        # duration
        metadata['duration'] = timedelta(seconds=int(tags.info.length))
        # extension
        metadata['extension'] = tags.mime[0][6:]
        # filesize
        metadata['filesize'] = int(tags.info.length*tags.info.bitrate/(8*1024))

        ### Check if it is a song with the API here ###
        # is_song = api_call.is_song(file)
        is_song = True  # for now this is hard coded
        metadata['is_song'] = is_song

        # if it is a song, add some more tags
        if is_song:
            # artist
            if 'artist' in tags:
                metadata['artist'] = tags['artist'][0]
            elif 'TPE1' in tags:
                metadata['artist'] = tags['TPE1'][0]
            else:
                metadata['artist'] = None
            # album
            if 'album' in tags:
                metadata['album'] = tags['album'][0]
            elif 'TALB' in tags:
                metadata['album'] = tags['TALB'][0]
            else:
                metadata['album'] = None
            # genre
            if 'genre' in tags:
                metadata['genre'] = tags['genre'][0]
            elif 'TCON' in tags:
                metadata['genre'] = tags['TCON'][0]
            else:
                metadata['genre'] = None
            # release date
            if 'date' in tags:
                release_date = tags['date'][0]
                metadata['release_date'] = release_date.split('T')[0]
            elif 'TDRC' in tags:
                release_date = tags['TDRC'][0]
                metadata['release_date'] = release_date.split('T')[0]
            else:
                metadata['release_date'] = None
        
    return metadata
