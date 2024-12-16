from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role']

class UserCreateSerializer(serializers.ModelSerializer):
    career = serializers.CharField(write_only=True)
    age = serializers.IntegerField(write_only=True)
    gender = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role', 'career', 'age', 'gender']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
            # Extraer los datos del perfil
            career = validated_data.pop('career')
            age = validated_data.pop('age')
            gender = validated_data.pop('gender')

            # Crear el usuario
            user = User.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password'],
                role=validated_data.get('role', 'STUDENT')  # Rol predeterminado: STUDENT
            )

            # Crear el perfil asociado
            Profile.objects.create(
                user=user,
                career=career,
                age=age,
                gender=gender
            )

            return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'age', 'gender', 'career']
