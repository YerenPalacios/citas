from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from citas_app.serializers import RegisterSerializer
# Create your views here.

class LoginView(APIView):
    def post(self, request):
        user = authenticate(email=request.data["email"], password=request.data["password"])
        if not user:
            return Response({"error": "Authentication failed"})
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    
    def get(self, request):
        return Response({"hola": "login"})
    

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.create()
        except IntegrityError:
            return Response({"error": "User already exists"})
        return Response({"status": "ok"})
    
    def get(self, request):
        return Response({"hola": "registro"})
    

class AppointmentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response({"hola": "Crear cita"})
    
    def get(self, request):
        return Response({"hola": "listado de citas disponibles"})
    