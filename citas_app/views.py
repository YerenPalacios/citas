from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class LoginView(APIView):
    def post(self, request):
        return Response({"hola": "login"})
    
    def get(self, request):
        return Response({"hola": "login"})
    

class RegisterView(APIView):
    def post():
        return Response({"hola": "registro"})
    
    def get(self, request):
        return Response({"hola": "registro"})
    

class AppointmentView(APIView):
    def post(self, request):
        return Response({"hola": "Crear cita"})
    
    def get(self, request):
        return Response({"hola": "listado de citas disponibles"})
    