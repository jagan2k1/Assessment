import string
import random

from django.contrib.auth.hashers import check_password
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, GenericAPIView,UpdateAPIView,ListAPIView,RetrieveAPIView
from rest_framework import permissions

from basic_app import serializers, models, data_serialization
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class OrganisationSignup(CreateAPIView):
    """This class is to add new user with organisation and the user role in respective tables"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.SignupSerializer

    def post(self, request, *args, **kwargs):
        try:
            # saving the data in users table
            username = request.data['user_email'].split('@')[0] + "_"
            user_data = {
                "user_id": "USER_"+"".join(random.choices(string.ascii_uppercase, k=3)) + ''.join(
                            random.choices(string.digits, k=3)),
                "email": request.data["user_email"],
                "username": username,
                "password": request.data["password"],
                "is_staff": 1,
                "is_superuser": 1,
                "is_active": 1,
                "profile": {"gender": request.data["gender"],
                            "languange_preference": request.data["languange_preference"],
                            "user_designation": request.data["user_designation"],
                            "user_mobile_number": request.data["user_mobile_number"]},
                "status": 1,
                "is_verified": 1
            }
            user_serializer_class = serializers.SaveUserSerializer(data=user_data)
            if user_serializer_class.is_valid(raise_exception=True):
                user_serializer_class.save()
                data = {
                    'response_code': 200,
                    'message': 'User Signed Up Successfully',
                    'status': 'SUCCESS',
                    'errorDetails': None,
                    'data': "User added successfully"
                }
                return Response(data)
        except Exception as error:
            data = {
                'response_code': 500,
                'message': 'Unable Signup user',
                'status': 'FAILED',
                'errorDetails': str(error),
                'data': {}
            }
            return Response(data)


class Login(CreateAPIView):
    """This class is to authenticate the user and accessing the resource"""
    serializer_class = serializers.SigninSerializer

    def post(self, request, *args, **kwargs):
        try:
            username = request.data['username']
            password = request.data['password']
            user = models.User.objects.filter(username=username).first()
            if user and check_password(password, user.password):
                data = data_serialization.get_tokens_for_user(user)
                data_response = {
                    'response_code': 200,
                    'message': 'User SignedIn Successfully',
                    'status': 'SUCCESS',
                    'errorDetails': None,
                    'data': data
                }
                return Response(data_response)
            data_response = {
                'response_code': 400,
                'message': 'user does not exist',
                'status': 'FAILED',
                'errorDetails': "username or password is incorrect",
                'data': []
            }
            return Response(data_response)
        except Exception as error:
            data = {
                'response_code': 500,
                'message': 'Unable to Signin user',
                'status': 'FAILED',
                'errorDetails': str(error),
                'data': {}
            }
            return Response(data)


class AddProductDetails(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AddProductSerializer

    def post(self, request, *args, **kwargs):
        try:
            product_name = request.data['product_name']
            product_info = models.Product.objects.filter(product_name=product_name)
            if product_info:
                data = {
                    'response_code': 400,
                    'message': 'Product already exists',
                    'status': 'SUCCESS',
                    'errorDetails': None,
                    'data': "Product already exists"
                }
                return Response(data)
            else:
                serializer_class = serializers.ProductSerializer(data=request.data)
                if serializer_class.is_valid(raise_exception=True):
                    serializer_class.save()
                    data = {
                        'response_code': 200,
                        'message': 'Product added Successfully',
                        'status': 'SUCCESS',
                        'errorDetails': None,
                        'data': serializer_class.data
                    }
                    return Response(data)
                else:
                    data_response = {
                        'response_code': 400,
                        'message': str(serializer_class.errors),
                        'statusFlag': False,
                        'status': 'FAILED',
                        'errorDetails': str(serializer_class.errors),
                        'data': {}
                    }
                # _logger.error(str(serializer_class.errors))
                return Response(data_response)
        except Exception as error:
            data = {
                'response_code': 500,
                'message': 'Unable to added Product',
                'status': 'FAILED',
                'errorDetails': str(error),
                'data': {}
            }
            return Response(data)


class FetchProductDetails(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            product_exists = models.Product.objects.filter(product_id=kwargs["product_id"])
            if product_exists:
                data = product_exists.values()
                data = {
                    'response_code': 200,
                    'message': 'Product added Successfully',
                    'status': 'SUCCESS',
                    'errorDetails': None,
                    'data': data
                }
                return Response(data)
            else:
                data_response = {
                    'response_code': 404,
                    'message': "product doesn't Exists",
                    'statusFlag': False,
                    'status': 'FAILED',
                    'errorDetails': "product doesn't Exists" ,
                    'data': {}
                }
                # _logger.error(str(serializer_class.errors))
                return Response(data_response)

        except Exception as error:
            data = {
                'response_code': 500,
                'message': 'Unable to added Product',
                'status': 'FAILED',
                'errorDetails': str(error),
                'data': {}
            }
            return Response(data)


class UpdateProductDetails(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UpdateProductSerializer

    def post(self, request, *args, **kwargs):
        try:
            product_exists = models.Product.objects.filter(product_id=request.data["product_id"])
            if product_exists:
                product_exists.update(
                    product_name=request.data["product_name"],
                    product_details=request.data["product_details"]
                )

                data = {
                    'response_code': 200,
                    'message': 'Product added Successfully',
                    'status': 'SUCCESS',
                    'errorDetails': None,
                    'data': product_exists.values()
                }
                return Response(data)
            else:
                data_response = {
                    'response_code': 404,
                    'message': "product doesn't Exists",
                    'statusFlag': False,
                    'status': 'FAILED',
                    'errorDetails': "product doesn't Exists" ,
                    'data': {}
                }
                # _logger.error(str(serializer_class.errors))
                return Response(data_response)

        except Exception as error:
            data = {
                'response_code': 500,
                'message': 'Unable to added Product',
                'status': 'FAILED',
                'errorDetails': str(error),
                'data': {}
            }
            return Response(data)


class DeleteProductDetails(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            product_id = kwargs['product_id']
            product_info = models.Product.objects.filter(product_id=product_id).first()
            if product_info:
                product_info.delete()
                data = {
                    'response_code': 200,
                    'message': 'Product deleted Successfully',
                    'status': 'SUCCESS',
                    'errorDetails': None,
                    'data': "Product deleted Successfully"
                }
                return Response(data)
            else:
                data = {
                    'response_code': 404,
                    'message': "Product doesn't exists",
                    'status': 'SUCCESS',
                    'errorDetails': None,
                    'data': "Product doesn't exists"
                }
                return Response(data)
        except Exception as error:
            data = {
                'response_code': 500,
                'message': "Product doesn't exists",
                'status': 'FAILED',
                'errorDetails': str(error),
                'data': {}
            }
            return Response(data)