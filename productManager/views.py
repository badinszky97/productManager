
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
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect





from .forms import Loginform
from .forms import NewElementForm

from .settings import PRODUCTMANAGER_VARIABLES


def dashboard_view(request):

    if request.user.is_authenticated:
        # Already logged in, redirect to the dashboard
        return render(request, "dashboard.html",{"parts": str(len(get_all_elements("Part"))), "operations":str(len(get_all_elements("Operation"))), "assemblies" : str(len(get_all_elements("Assembly"))) , "products":str(len(get_all_elements("Product"))), "projects":str(len(get_all_elements("Project"))) })
    
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = Loginform(request.POST)

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "dashboard.html",{"parts": str(len(get_all_elements("Part"))), "operations":str(len(get_all_elements("Operation"))), "assemblies" : str(len(get_all_elements("Assembly"))) , "products":str(len(get_all_elements("Product"))), "projects":str(len(get_all_elements("Project"))) })
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
    alerts = []
    print("get code: " + str(id))
    if request.user.is_authenticated:
        vendors = get_all_vendors()
        filtered_parts = []
        active_modal_vendor = False
        active_consist_modal = False
        current_element = Element()
        current_element.load_parameters_from_database(id)
        active_tab="media" # default tab

        if request.method == "POST":
            if(request.POST["formType"] == "uploadForm"):
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    handle_uploaded_file(request.FILES["file"], id, request.POST["description"])

            elif(request.POST["formType"] == "vendorFilter"):
                vendors = get_all_vendors(request.POST["company"], request.POST["address"])
                active_modal_vendor = True
                active_tab="vendors"

            elif(request.POST["formType"] == "addVendor"):
                res = current_element.add_purchase_opportunity(request.POST["vendorID"],
                                                         request.POST["price_unit"],
                                                         request.POST["price"],
                                                         request.POST["unit"],
                                                         request.POST["code"],
                                                         request.POST["link"]
                                                         )
                if( not res):
                    alerts.append({"text": 'Recursive list error during adding the element', "type" : "error"})
                active_tab="vendors"

            elif(request.POST["formType"] == "consistFilter"):
                filtered_parts = get_all_elements(request.POST["element_type"],request.POST["name"],request.POST["code"])
                active_consist_modal = True
                active_tab="consist"

            elif(request.POST["formType"] == "addConsist"):
                active_consist_modal = True
                active_tab="consist"
                result = current_element.add_consist_element(request.POST["childID"], request.POST["pieces"])
                if( not result):
                    alerts.append({"text": 'Adding was unsuccessfull', "type" : "error"})

            elif(request.POST["formType"] == "consistModify"):
                active_tab="consist"
                result = current_element.modify_consist_element(request.POST["childID"], request.POST["pieces"])
                if( not result):
                    alerts.append({"text": 'Modifying was unsuccessfull', "type" : "error"})

            elif(request.POST["formType"] == "consistDelete"):
                result = current_element.delete_consist_element(request.POST["childID"])
                if(not result):
                    alerts.append({"text": 'Deleting was unsuccessfull', "type" : "error"})
                active_tab="consist"
                

            elif(request.POST["formType"] == "vendorDelete"):
                result = current_element.delete_purchase_opportunity(request.POST["orderID"])
                if(not result):
                    alerts.append({"text": 'Deleting was unsuccessfull', "type" : "error"})
            elif(request.POST["formType"] == "modifyFundamentals"):
                name_res = current_element.modify_name(request.POST["element_name"])
                code_res = current_element.modify_code(request.POST["element_code"])
                if(name_res and code_res):
                    alerts.append({"text": 'Modifying was successfull', "type" : "success"})
                else:
                    alerts.append({"text": 'Modifying was unsuccessfull', "type" : "error"})
            current_element.load_parameters_from_database(id)          

        return render(request, 'element_detail.html', {"element": current_element, "active_tab" : active_tab, "all_media" : get_all_media(), "vendors" : vendors, "newFileForm" : UploadFileForm(), "active_modal_vendor" : active_modal_vendor, "active_consist_modal" : active_consist_modal, "price_units" : get_all_price_units(), "filtered_parts" : filtered_parts, "alerts" : alerts})
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
        result = current_element.delete()
        

        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

def element_add(request, type, url):
    if request.user.is_authenticated:
        if request.method == "POST":    
            form = NewElementForm(request.POST)
            if form.is_valid():
                newPart = Element(0, request.POST["name"], type, request.POST["code"], 0)
                try:
                    result = newPart.createInDatabase()
                    return HttpResponseRedirect(url) # redirect if successful
                except:
                    alerts = []
                    alerts.append({"text": 'Already existing code', "type" : "error"})
                    return render(request, 'dashboard.html', {"alerts" : alerts})
                    
        
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
        result = current_element.delete()

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
    result = part.change_icon(media_path)
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
                result = newVendor.createInDatabase()
        return HttpResponseRedirect("/vendors")
    else:
        return HttpResponseRedirect("/")
    
def vendor_delete(request, id):
    if request.user.is_authenticated:
        current_vendor = Vendor(0,"","")
        current_vendor.load_parameters_from_database(id)
        result = current_vendor.delete()
        

        return HttpResponseRedirect("/vendors")
    else:
        return HttpResponseRedirect("/")
    
# **************************************************
# Inventory
# **************************************************
def inventory_view(request):
    alerts = []
    element_list = get_all_elements()
    
    if request.user.is_authenticated:
        if request.method == "POST":
            if(request.POST["formType"] == "consistFilter"):
                element_list = get_all_elements(request.POST["element_type"],request.POST["name"],request.POST["code"])
            elif(request.POST["formType"] == "addToInventory"):
                current_element = Element()
                current_element.load_parameters_from_database(request.POST["elementID"])
                allowed = current_element.add_to_inventory(request.POST["pieces"], request.POST["description"])
                if(allowed):
                    alerts.append({"text": 'Adding to inventory was successfull', "type" : "success"})
                else:
                    alerts.append({"text": 'Adding to inventory was unsuccessfull', "type" : "error"})
                

    else:
        return HttpResponseRedirect("/")
    
    return render(request, 'inventory.html', {"element_list": element_list, "alerts" : alerts})

# **************************************************
# Users
# **************************************************
def users_view(request):
    if request.user.is_authenticated:
        user = request.user
        if(user.is_superuser):
            all_users = User.objects.values()
            return render(request, 'users.html', {"users": all_users})
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
    
def myaccount_view(request):
    alerts = []
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            alerts.append({"text":"Password successfully changed!", "type" : "success" })
            form = PasswordChangeForm(request.user)
            return render(request, 'my_account.html', {'form': form, 'alerts' : alerts})

        else:
            alerts.append({"text": 'Password change was not successful', "type" : "error"})
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'my_account.html', {'form': form, 'alerts' : alerts})

def aboutus_view(request):
    return render(request, 'aboutus.html')

def logout_view(request):
    if request.user.is_authenticated == True:
        logout(request)
    return HttpResponseRedirect("/")

        