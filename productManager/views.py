
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


from .forms import Loginform


def get_name(request):

    if request.user.is_authenticated:
        # Already logged in, redirect to the dashboard
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
                return render(request, "dashboard.html")
            else:
                return render(request, "index.html", {"form": form})
    else:
        form = Loginform()

    return render(request, "index.html", {"form": form})

def index(request):

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')



def logout_view(request):
    if request.user.is_authenticated == True:
        logout(request)
    return HttpResponseRedirect("/")

        