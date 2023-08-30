from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Card, Possesion
from .forms import RegisterForm, ProfileForm, VideoForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
import os
import subprocess
import sys
from .createDatabase import aaa

sys.path.insert(
    0, "../MTGScanWebsite/mtgscan/darkflow"
)
import run, guess_cards


def index(request):
    if request.GET.get("Sign Up") == "Sign Up":
        return redirect(register)
    if request.GET.get("Log In") == "Log In":
        return redirect("accounts/login")
    return render(request, "welcome_page.html")


def card_by_id(request, card_id):
    card = Card.objects.get(pk=card_id)
    return render(request, "show_test_card.html", {"card": card.name})


def register(request):
    print("awdaadwdaw")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        print("!!!!!!!!", form.is_valid())
        print(form.errors)
        if form.is_valid():
            form.save()
    else:
        form = RegisterForm()

    return render(request, "registration/registration.html", {"form": form})


def show_collection(request):
    print(request.user.id, request.user)
    collection = []
    try:
        cards = Possesion.objects.filter(userId=request.user.id)
    except Possesion.DoesNotExist:
        pass
    for i in cards:
        collection.append(
            {"name": i.cardId.all()[:1].get().name, "jpg": i.cardId.all()[:1].get().networkName}
        )
    return render(request, "show_cards.html", {"collection": collection, "penult": len(collection) - 1})


def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            val = form.cleaned_data.get("btn")
            print(request.user.id, val)
            if val == "Go to my collection":
                return redirect(show_collection)
            else:
                return redirect(add_cards)

    else:
        form = ProfileForm()
    return render(request, "accounts/profile.html", locals())


def add_to_database(cards, request):
    for c in cards:
        # check if card is in database, if not add
        card = Card.objects.filter(networkName=c+".jpg")
        print(c+".jpg", card)

        new_possesios = Possesion.objects.create()
        user = User.objects.filter(username=request.user.username)
        new_possesios.userId.set(user)
        new_possesios.cardId.set(card)
    return redirect(profile)


@ensure_csrf_cookie
def add_cards(request):
    if request.GET.get("Add to database") == "Add to database":
        print(request.session.get("saved"))
        return add_to_database(request.session.get("saved"), request)
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            file = request.FILES["file"]
            print(file.name, file.name[-4:])
            # if file.name[-4:] != ".mp4":
            #     return render(request, "add_cards.html", {"form": form})

            handle_uploaded_file(file)
            new_cards = guess_cards.guess_cards()
            card_names = []
            for c in new_cards:
                card = Card.objects.filter(networkName=c+".jpg").values('name')[0]['name']
                card_names.append(card)

            request.session["saved"] = new_cards.tolist()
            return render(
                request, "add_cards.html", {"filename": file.name, "cards": card_names}
            )
    else:
        form = VideoForm()
    return render(request, "add_cards.html", {"form": form})


def handle_uploaded_file(f):
    here = os.path.dirname(os.path.abspath(__file__))
    s = os.path.join(here, "media", f.name)
    with open(s, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        run.run(s)
