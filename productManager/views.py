
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import FileResponse
from django.contrib.auth import authenticate, login, logout
from .elements import get_all_elements
from .elements import Element
from .media import get_all_media
from .media import Media
from .vendor import get_all_vendors
from .forms import UploadFileForm
from .forms import NewVendorForm
from .vendor import Vendor
from .vendor import get_all_price_units
import os.path, random, string
from django.core.files.storage import FileSystemStorage



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
    return render(request, 'index.html')

# **************************************************
# Elements
# **************************************************

def handle_uploaded_file(f, id, description):  
    # printing lowercase
    characters = string.ascii_letters
    filename = ''.join(random.choice(characters) for i in range(10)) + "." + f.name.split('.')[-1]

    with open(PRODUCTMANAGER_VARIABLES["media_path"] + "/" + filename, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  
    newMedia = Media(filename, description)
    newMedia.createInDatabase()
    newMedia.attachFileToElement(id)


def element_details_view(request, id):
    print("get code: " + str(id))
    if request.user.is_authenticated:
        vendors = get_all_vendors()
        active_modal_vendor = False
        current_element = Element()
        current_element.load_parameters_from_database(id)
        if request.method == "POST":
            if(request.POST["formType"] == "uploadForm"):
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    handle_uploaded_file(request.FILES["file"], id, request.POST["description"])
            elif(request.POST["formType"] == "vendorFilter"):
                vendors = get_all_vendors(request.POST["company"], request.POST["address"])
                active_modal_vendor = True
            elif(request.POST["formType"] == "addVendor"):
                current_element.add_purchase_opportunity(request.POST["vendorID"],
                                                         request.POST["price_unit"],
                                                         request.POST["price"],
                                                         request.POST["unit"],
                                                         request.POST["code"],
                                                         request.POST["link"]
                                                         )


                current_element.load_parameters_from_database(id)
            elif(request.POST["formType"] == "vendorDelete"):
                current_element.delete_purchase_opportunity(request.POST["orderID"])
                current_element.load_parameters_from_database(id)          

        print(str(current_element))
        return render(request, 'element_detail.html', {"element": current_element, "all_media" : get_all_media(), "vendors" : vendors, "newFileForm" : UploadFileForm(), "active_modal_vendor" : active_modal_vendor, "price_units" : get_all_price_units()})
    else:
        return HttpResponseRedirect("/")
    
def element_delete(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES["file"], id, request.POST["description"])

        current_element = Element()
        current_element.load_parameters_from_database(id)
        current_element.delete()
        

        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

def element_add(request, type, url):
    if request.user.is_authenticated:
        if request.method == "POST":    
            form = NewElementForm(request.POST)
            if form.is_valid():
                newPart = Element(0, request.POST["name"], type, request.POST["code"], 0)
                newPart.createInDatabase()
        return HttpResponseRedirect(url) # redirect if successful
    else:
        return HttpResponseRedirect("/")

# **************************************************
# Operations
# **************************************************
def operations_view(request):
    all_operations = get_all_elements("Operation")
    return render(request, 'elements.html', {"elements": all_operations, "newElementForm" : NewElementForm(), "type" : "Operation"})

# **************************************************
# Parts
# **************************************************
def parts_view(request):
    all_parts = get_all_elements("Part")
    return render(request, 'elements.html', {"elements": all_parts, "newElementForm" : NewElementForm(), "type" : "Part"})

# **************************************************
# Assemblies
# **************************************************
def assemblies_view(request):
    all_assemblies = get_all_elements("Assembly")
    return render(request, 'elements.html', {"elements": all_assemblies, "newElementForm" : NewElementForm(), "type" : "Assembly"})

# **************************************************
# Products
# **************************************************
def products_view(request):
    all_products = get_all_elements("Product")
    return render(request, 'elements.html', {"elements": all_products, "newElementForm" : NewElementForm(), "type" : "Product"})
    
# **************************************************
# Projects
# **************************************************
def projects_view(request):
    all_projects = get_all_elements("Project")
    return render(request, 'elements.html', {"elements": all_projects, "newElementForm" : NewElementForm(), "type" : "Project"})

# **************************************************
# Media
# **************************************************
def media_view(request):
    if request.user.is_authenticated:
        all_media = get_all_media()
        return render(request, 'media.html', {"all_media": all_media})
    else:
        return HttpResponseRedirect("/")
    
def media_delete(request, id):
    if request.user.is_authenticated:
        current_element = Media("-","-")
        current_element.load_parameters_from_database(id)
        current_element.delete()

        return HttpResponseRedirect("/media")
    else:
        return HttpResponseRedirect("/")
    
def openMedia(request, path):
    if(os.path.isfile(PRODUCTMANAGER_VARIABLES["media_path"] + "/" + path)):
        img = open(PRODUCTMANAGER_VARIABLES["media_path"] + "/" + path, 'rb')
        return FileResponse(img)
    else:
        img = open("./productManager/static/image.svg", 'rb')
        return FileResponse(img)

def modify_icon(self, element_id, media_path):
    part = Element()
    part.load_parameters_from_database(element_id)
    part.change_icon(media_path)
    return HttpResponseRedirect(f"/elements/{element_id}")


# **************************************************
# Vendors
# **************************************************
def vendors_view(request):
    return render(request, 'vendors.html', {"vendors": get_all_vendors(), "newVendorForm" : NewVendorForm()})

def vendor_add(request):
    if request.user.is_authenticated:
        if request.method == "POST":    
            form = NewVendorForm(request.POST)
            if form.is_valid():
                newVendor = Vendor(0,request.POST["company"], request.POST["address"])
                newVendor.createInDatabase()
        return HttpResponseRedirect("/vendors")
    else:
        return HttpResponseRedirect("/")
    
def vendor_delete(request, id):
    if request.user.is_authenticated:
        current_vendor = Vendor(0,"","")
        current_vendor.load_parameters_from_database(id)
        current_vendor.delete()
        

        return HttpResponseRedirect("/vendors")
    else:
        return HttpResponseRedirect("/")

def logout_view(request):
    if request.user.is_authenticated == True:
        logout(request)
    return HttpResponseRedirect("/")

        