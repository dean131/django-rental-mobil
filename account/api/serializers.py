from rest_framework import serializers
from ..models import User


class RegistrationModelSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = '__all__'


    def save(self):
        user = User.objects.create_user(
            full_name=self.validated_data['full_name'],
            email=self.validated_data['email'],
            gender=self.validated_data['gender'],
            birth_date=self.validated_data['birth_date'],
            phone_number=self.validated_data['phone_number'],
            nik=self.validated_data['nik'],
            profile_picture=self.validated_data['profile_picture'],
            license_card_image=self.validated_data['license_card_image'],
            id_card_image=self.validated_data['id_card_image'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password doesn\'t match'})
        
        user.set_password(password)
        user.save()
        return user
    

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'full_name', 
            'email', 
            'gender',
            'birth_date',
            'phone_number',
            'nik',
            'profile_picture',
            'license_card_image',
            'id_card_image'
        ]