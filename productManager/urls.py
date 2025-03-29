"""
URL configuration for productManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard_view),
    path('parts/', views.parts_view),
    path('elements/<int:id>', views.element_details_view),
    path('elements/delete/<int:id>', views.element_delete),
    path('elements/modify_icon/<int:element_id>/<str:media_path>', views.modify_icon),

    path('parts/add', views.element_add, {"type" : "Part", "url" : "/parts"}),

    path('operations/', views.operations_view),
    path('operations/add', views.element_add, {"type" : "Operation", "url" : "/operations"}),
    
    path('assemblies/', views.assemblies_view),
    path('assemblies/add', views.element_add, {"type" : "Assembly", "url" : "/assemblies"}),

    path('products/', views.products_view),
    path('products/add', views.element_add, {"type" : "Product", "url" : "/products"}),

    path('projects/', views.projects_view),
    path('projects/add', views.element_add, {"type" : "Project", "url" : "/projects"}),

    path('media/', views.media_view),
    path('media/delete/<int:id>', views.media_delete),
    path('media/<str:path>', views.openMedia),

    path('vendors/', views.vendors_view),
    path('vendors/add', views.vendor_add),
    path('vendors/delete/<int:id>', views.vendor_delete),

   path('inventory/', views.inventory_view),

    path('users/', views.users_view),
    path('myaccount/', views.myaccount_view),

    path('aboutus/', views.aboutus_view),


    path('logout/', views.logout_view, name='logout'),

    
]
