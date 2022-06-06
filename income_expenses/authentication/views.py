from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer,EmailVerificationSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework.views import APIView

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True) # validate()
        serializer.save() # create()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email_verify')


        absurl = 'http://' + current_site + relativeLink + '?token=' + str(token)

        email_body = 'Hi ' + user.username + 'Use link below to verify you email.\n' + 'domain: ' +  absurl
        data = {
            'to_email': user.email,
            'email_body': email_body,
            'email_subject': 'verify your email'
        }
        Util.send_email(data)

        return Response(user_data,status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):

    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True 
            user.save()

            return Response({'email': 'Successfully activated'},status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token or expired.'},status=status.HTTP_400_BAD_REQUEST)
        