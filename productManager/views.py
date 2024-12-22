
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import mysql.connector
from .settings import DATABASES
import mariadb


from .forms import Loginform


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

    try:
        conn = mariadb.connect(
            user=DATABASES["product_manager"]["user"],
            password=DATABASES["product_manager"]["passwd"],
            host=DATABASES["product_manager"]["host"],
            port=3306,
            database=DATABASES["product_manager"]["database"]

        )
                # Get Cursor
        cur = conn.cursor()
        cur.execute("SELECT * FROM file_types")
        for (id, desc) in cur:
            print(f"First Name: {id}, Last Name: {desc}")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")




    # Render the HTML template index.html with the data in the context variable
    return render(request, 'parts.html')

def logout_view(request):
    if request.user.is_authenticated == True:
        logout(request)
    return HttpResponseRedirect("/")

        