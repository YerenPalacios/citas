from django.urls import path

from citas_app.views import AppointmentView, RegisterView, LoginView

urlpatterns = [
    path('login/', RegisterView.as_view()),
    path('signin/', LoginView.as_view()),
    path('appointments/', AppointmentView.as_view()),
]