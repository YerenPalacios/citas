from rest_framework import serializers

from citas_app.models import User

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField()

    def create(self):
        return User.objects.create_user(
            self.data['name'], 
            self.data["phone"], 
            self.data["email"],
            self.data["password"],
        )