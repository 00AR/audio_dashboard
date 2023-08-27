from django.shortcuts import render
from django.http import HttpResponse
from . import forms
from .models import Audio, User
from datetime import datetime, timedelta
from django.shortcuts import redirect


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
            for file in request.FILES.getlist("files"):
                instance = Audio.objects.create(
                    file=file,
                    user=user,
                    title="rain and tears2",
                    date_of_upload=datetime.now(),
                    size=1900,
                    extension="mp3",
                    duration=timedelta(seconds=58),
                    is_song=False,
                )
    else:
        form = forms.MultiUploadAudioForm()
    audio_list = Audio.objects.filter(user=user)
    context = {
        "audio_list": audio_list,
        "form": form,
    }
    return render(request, "user_home.html", context)

