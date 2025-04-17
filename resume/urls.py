from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_resume, name='create_resume'),
    path('<slug:slug>/preview/', views.resume_preview, name='resume_preview'),
    path('<slug:slug>/edit/<str:section>/', views.edit_resume_section, name='edit_resume_section'),
    path('<slug:slug>/delete/', views.delete_resume, name='delete_resume'),
    path('<slug:slug>/duplicate/', views.duplicate_resume, name='duplicate_resume'),
    path('<slug:slug>/toggle-visibility/', views.toggle_resume_visibility, name='toggle_resume_visibility'),
    path('<slug:slug>/download-pdf/', views.download_pdf, name='download_pdf'),
    path('public/<slug:slug>/', views.public_resume, name='public_resume'),
]
