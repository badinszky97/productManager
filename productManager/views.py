
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import FileResponse
from django.contrib.auth import authenticate, login, logout
from .elements import get_all_elements
from .elements import Element
from .media import get_all_media
from .media import Media
import os.path


from .forms import Loginform
from .forms import NewElementForm

from .settings import PRODUCTMANAGER_VARIABLES


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

# **************************************************
# Elements
# **************************************************
def element_details_view(request, id):
    if request.user.is_authenticated:
        current_element = Element()
        current_element.load_parameters_from_database(id)
        return render(request, 'element_detail.html', {"element": current_element})
    else:
        return HttpResponseRedirect("/")

def element_add(request, type, url):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NewElementForm(request.POST)
            if form.is_valid():
                newPart = Element(0, request.POST["name"], type, request.POST["code"], 0)
                newPart.createInDatabase()
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect("/")

# **************************************************
# Operations
# **************************************************
def operations_view(request):
    all_parts = get_all_elements("Operation")
    for item in all_parts:
        print("****" + str(item))
    newElementForm = NewElementForm()
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'elements.html', {"elements": all_parts, "newElementForm" : newElementForm, "type" : "Operation"})

def operations_add_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NewElementForm(request.POST)
            if form.is_valid():
                newPart = Element(0, request.POST["name"], "Operation", request.POST["code"], 0)
                newPart.createInDatabase()
        return HttpResponseRedirect("/operations")
    else:
        return HttpResponseRedirect("/")

# **************************************************
# Parts
# **************************************************
def parts_view(request):
    all_parts = get_all_elements("Part")
    return render(request, 'elements.html', {"elements": all_parts, "newElementForm" : NewElementForm(), "type" : "Part"})

def parts_add_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NewElementForm(request.POST)
            if form.is_valid():
                newPart = Element(0, request.POST["name"], "Part", request.POST["code"], 0)
                newPart.createInDatabase()
        return HttpResponseRedirect("/parts")
    else:
        return HttpResponseRedirect("/")

# **************************************************
# Assemblies
# **************************************************
def assemblies_view(request):
    all_assemblies = get_all_elements("Assembly")
    return render(request, 'elements.html', {"elements": all_assemblies, "newElementForm" : NewElementForm(), "type" : "Assembly"})

def assemblies_add_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NewElementForm(request.POST)
            if form.is_valid():
                newPart = Element(0, request.POST["name"], "Assembly", request.POST["code"], 0)
                newPart.createInDatabase()
        return HttpResponseRedirect("/assemblies")
    else:
        return HttpResponseRedirect("/")

# **************************************************
# Products
# **************************************************
def products_view(request):
    all_products = get_all_elements("Product")
    return render(request, 'elements.html', {"elements": all_products, "newElementForm" : NewElementForm(), "type" : "Product"})

def products_add_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NewElementForm(request.POST)
            if form.is_valid():
                newPart = Element(0, request.POST["name"], "Product", request.POST["code"], 0)
                newPart.createInDatabase()
        return HttpResponseRedirect("/products")
    else:
        return HttpResponseRedirect("/")
    

# **************************************************
# Projects
# **************************************************
def projects_view(request):
    all_projects = get_all_elements("Project")
    return render(request, 'elements.html', {"elements": all_projects, "newElementForm" : NewElementForm(), "type" : "Project"})

def projects_add_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NewElementForm(request.POST)
            if form.is_valid():
                newPart = Element(0, request.POST["name"], "Project", request.POST["code"], 0)
                newPart.createInDatabase()
        return HttpResponseRedirect("/projects")
    else:
        return HttpResponseRedirect("/")


# **************************************************
# Media
# **************************************************
def media_view(request):
    if request.user.is_authenticated:
        all_media = get_all_media()
        return render(request, 'media.html', {"all_media": all_media})
    else:
        return HttpResponseRedirect("/")
    
def openMedia(request, path):
    if(os.path.isfile(PRODUCTMANAGER_VARIABLES["media_path"] + "/" + path)):
        img = open(PRODUCTMANAGER_VARIABLES["media_path"] + "/" + path, 'rb')
        return FileResponse(img)
    else:
        img = open("./productManager/static/image.svg", 'rb')
        return FileResponse(img)

def logout_view(request):
    if request.user.is_authenticated == True:
        logout(request)
    return HttpResponseRedirect("/")

        