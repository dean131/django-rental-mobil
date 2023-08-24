from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    # email = serializers.EmailField(required = True)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password', 'password2',]
        # fields = ('full_name', 'gender', 'birth_date', 'phone_number', 'nik',)

    def save(self):
        user = User.objects.create_user(
            first_name=self.validated_data['first_name'],
            email=self.validated_data['email'],
            username=self.validated_data['email'].split('@')[0]
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password tidak cocok'})
        
        user.set_password(password)
        user.save()
        return user