from rest_framework import serializers

from basic_app import models

from django.contrib.auth import authenticate


class SigninSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, request):
        users = models.User.objects.filter(username=request.data["username"])
        if users:
            user = authenticate(request=self.context.get('request'),
                                username=request.data["username"], password=request.data["password"])
            request['user'] = user
            return request
        msg = {
            'detail': 'Unable to log in with provided credentials.', 'register': True}
        raise serializers.ValidationError(msg, code='authorization')


class SignupSerializer(serializers.Serializer):
    user_first_name = serializers.CharField()
    user_last_name = serializers.CharField()
    user_email = serializers.EmailField()
    password = serializers.CharField()
    gender = serializers.CharField()
    languange_preference = serializers.CharField()
    user_designation = serializers.CharField()
    user_mobile_number = serializers.IntegerField()


class SaveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user


class AddProductSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    product_details = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class FetchProductId(serializers.Serializer):
    product_id = serializers.CharField()


class UpdateProductSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    product_name = serializers.CharField()
    product_details = serializers.CharField()
