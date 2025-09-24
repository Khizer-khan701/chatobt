from django.contrib import admin
from django.urls import path, include
from qa_app import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.ask_question, name='home'),
    path("", include("qa_app.urls")),  # hook qa_app urls
]
