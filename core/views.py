import random
import re
import string
# from _multiprocessing import send
from datetime import datetime, tzinfo
from datetime import timedelta
import datetime
from django.utils import timezone
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
from django.db import transaction, IntegrityError
from google.auth.transport._http_client import Response
from rest_framework.utils import json
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

import core
import re
import string
# from _multiprocessing import send
from datetime import datetime, tzinfo
from datetime import timedelta
import datetime
from django.utils import timezone
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
from django.db import transaction, IntegrityError
from google.auth.transport._http_client import Response
from rest_framework.utils import json
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

import core
from .core_functions import generateOTP, days_hours_minutes, twilio_otp, otp_verification_check, Pagination, qdict_to_dict
# from .serializers import *
from .serializers import *
from rest_framework import status, viewsets, mixins, generics, response
from django.contrib.auth.models import User
from django.core.mail import send_mail
# Generate Jwt-Token
from rest_framework_jwt.settings import api_settings
wt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from password_strength import PasswordPolicy, stats
from password_strength import PasswordStats
from datetime import datetime, timezone
policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)


policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)

#=========================Function start
def emailsending(key,template,email,msg):
    message = get_template(template).render(key)
    email = EmailMessage(msg, message, to=[email])
    email.content_subtype = 'html'
    email.send()
    print('Email Send Successfully')


def password_strenght(password):
    stats = PasswordStats(password)
    strenght = stats.strength()
    print(strenght)
    return strenght

def isNum(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


def set_if_not_none(mapping, key, value):
    if value is not None:
        mapping[key] = value


#================================Views Start

class User_Profiles(viewsets.ViewSet):#User class
    # {
    #     "email": "farz.mirza@argonteq.com",
    #     "password": "MMMirza@1213AAA"
    # }

    @action(detail=False,methods=['post'])
    def user_login(self, request):
        # host=request.META['HTTP_ORIGIN']
        username=request.data["email"]
        password=request.data["password"]

        if (User.objects.filter(username=username).exists()):
            object_user = User.objects.get(username=username)
            user_profile_object = User_Profile.objects.get(user=object_user.id)

            newapi='http://127.0.0.1:8000/core/login/'
            # newapi='http://18.118.201.66/core/login/'
            data1 = {"username": object_user.username,
                     "password": password}


            response = requests.post(newapi, data=data1).json()
            if 'token' in response:
                key = response['token']
                return Response({"Token": key, "Role": user_profile_object.role,"Verfication_Status":user_profile_object.verfication_status}, status=status.HTTP_200_OK)

            else:
                return Response({"Message": "Wrong password"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"Message": "Email does not Exist"}, status=status.HTTP_404_NOT_FOUND)




    # {
    #     "email": "frazmirza58@gmail.com",
    #     "password": "MMMirza@1213AAA",
    #     "phone": "546567"
    # }


    @action(detail=False, methods=['post','put'])
    def signup(self,request):#user_login
        if request.method=="POST":
            if User.objects.filter(Q(username=request.data['email'])).exists():
                return Response({"msg": "Already Registered"}, status.HTTP_306_RESERVED)
            else:
                user = User.objects.create_user(
                            username=request.data['email'],
                            password=request.data['password']

                )
                if user != '':

                    email = request.data['email']
                    user = User.objects.get(username=email)
                    data={"user":user.id,"registration_status":False}
                    if 'phone' in request.data:
                        data['phone']=request.data['phone']
                    print(data)
                    serializer = UserProfileSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        while True:
                            v_code = generateOTP()
                            if User_Profile.objects.filter(verfication_code=v_code).exists():
                                print("Code allready exist!!!!")
                            else:
                                User_Profile.objects.filter(user=user.id).update(verfication_code=v_code)
                                break

                        otp={
                            'otp':v_code
                        }
                        emailsending(otp, 'Activation_Email.html', email, 'Email Confirmation')
                        return Response({'Message': 'Successfully'}, status.HTTP_200_OK)
                    else:
                        print(serializer.errors)
                        return Response({'error': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'Message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        # {
        #     "code": "6430417640"
        # }
        if request.method == "PUT":
            user_obj=User_Profile.objects.filter(verfication_code=request.data["code"])
            if user_obj.exists():
                user_obj.update(verfication_status=True)
                return Response({'Message': 'Status Updated'}, status=status.HTTP_200_OK)
            else:
                return Response({"Message": "Code does not exist"}, status=status.HTTP_404_NOT_FOUND)
