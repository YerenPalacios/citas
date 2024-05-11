from datetime import datetime
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from citas_app.models import Appointment, User
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
        date = request.data["date"]
        name = request.data["name"]
        date = datetime.strptime(request.data["date"], "%Y-%m-%d %I:%M %p")
        date_appointments = Appointment.objects.filter(date=date)
        doctor = User.objects.filter(role="DOCTOR").order_by('?').first()

        if not doctor:
            return Response({"result": "No hay doctores"}, status=400)
        
        if date_appointments.exists():
            return Response({"result": "La cita para la fecha y hora seleccionadas ya está ocupada."}, status=400)
        
        Appointment.objects.create(name=name, date=date, patient_id=request.auth.user.id, doctor=doctor)

        return Response({"result": "Cita agendada con éxito."})
    
    def get(self, request):
        result = []
        appointments = Appointment.objects.filter(patient_id=request.auth.user.id)
        if not appointments:
            return Response({"result": "No hay citas agendadas para esta fecha."})
        for i in appointments:
            result.append({"id":i.pk, "name": i.name, "date": i.date.strftime("%Y-%m-%d %I:%M %p"), "doctor": i.doctor.name})
        return Response({"result": result})
    
    def delete(self, request):
        appointment_id = request.data["id"]
        appointment = Appointment.objects.filter(pk=appointment_id, patient=request.auth.user.id)
        if not appointment:
            return Response({"result": "No se encontró una cita"})
        
        appointment.first().delete()
        return Response({"result": "ok"})
    