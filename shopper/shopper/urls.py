"""shopper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path

from . import views

app_name = 'shopper'
urlpatterns = [
    path('', views.default, name='default'),
    path('search/', views.search, name='search'),
    path('search/prod_name:<str:prod_details>/', views.prod_page, name='prod_details'),
    # path('search/<str:prod_details>/', views.prod_page, name='prod_details'),

    path('search/drug_name:<str:drug_details>/', views.drug_page, name='drug_details'),
    # path('admin/', admin.site.urls),
    # path('polls/', include('polls.urls')),

    # path('shopper/', include('shopper.urls')),
    
]