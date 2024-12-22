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
    path('', views.get_name),
    path('parts/', views.parts_view),
    path('parts/<int:id>', views.element_details_view),
    path('parts/add', views.parts_add_view),

    path('operations/', views.operations_view),
    path('operations/<int:id>', views.element_details_view),
    path('operations/add', views.operations_add_view),

    path('assemblies/', views.assemblies_view),
    path('assemblies/<int:id>', views.element_details_view),
    path('assemblies/add', views.assemblies_add_view),

    path('products/', views.products_view),
    path('products/<int:id>', views.element_details_view),
    path('products/add', views.products_add_view),

    path('projects/', views.projects_view),
    path('projects/<int:id>', views.element_details_view),
    path('projects/add', views.projects_add_view),

    path('media/', views.media_view),
    path('media/<str:path>', views.openMedia),
    path('logout/', views.logout_view, name='logout'),

    
]
