
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .elements import get_all_parts
from .elements import Part

from .forms import Loginform
from .forms import NewPartForm


def get_name(request):

    if request.user.is_authenticated:
        # Already logged in, redirect to the dashboard
        print("1")
        return render(request, "dashboard.html")
    
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = Loginform(request.POST)

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("2")
                return render(request, "dashboard.html")
            else:
                print("3")
                return render(request, "index.html", {"form": form})
    else:
        form = Loginform()
    print("4")
    return render(request, "index.html", {"form": form})

def index(request):

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

def parts_view(request):
    all_parts = get_all_parts()
    for item in all_parts:
        print(str(item))
    newPartForm = NewPartForm()
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'parts.html', {"parts": all_parts, "newPartForm" : newPartForm})

def parts_add_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NewPartForm(request.POST)
            if form.is_valid():
                newPart = Part(0, request.POST["name"], 0, request.POST["code"], 0)
                newPart.createInDatabase()
    return HttpResponseRedirect("/parts")

def logout_view(request):
    if request.user.is_authenticated == True:
        logout(request)
    return HttpResponseRedirect("/")

        