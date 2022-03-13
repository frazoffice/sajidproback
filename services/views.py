import base64
import os
import random
import re
import string
# from _multiprocessing import send
from datetime import datetime, tzinfo
from datetime import timedelta
import datetime
from itertools import count

from django.utils import timezone
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
from django.db import transaction, IntegrityError
from google.auth.transport._http_client import Response
# from numpy import all
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
# from .serializers import *
from .models import Coupen
from .serializers import *
from rest_framework import status, viewsets, mixins, generics, response
from django.contrib.auth.models import User
from django.core.mail import send_mail
# Generate Jwt-Token
from rest_framework_jwt.settings import api_settings
wt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from datetime import datetime, timezone



class Order_Class(viewsets.ViewSet):#Place order
    # {
    #     "order_price": "farz.mirza@argonteq.com",
    #     "media_file": "MMMirza@1213AAA"
    # }

    @action(detail=False,methods=['post','get','patch'])
    def Place_order(self, request):
        if request.method == "POST":
            data=request.data
            data['user']=request.user.id
            serializer = SaveOrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Successfully'}, status.HTTP_200_OK)
            else:
                print(serializer.errors)
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == "GET":
            all_order=Order.objects.all()
            print(all_order)
            serializer = OrderSerializer(all_order, many=True)
            return Response({"AllProfiles": serializer.data})
        if request.method == "PATCH":
            try:
                order_obj = Order.objects.get(id=request.data['id'])
            except Order.DoesNotExist:
                return Response({"Message": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ChangeOrderStatusSerializer(order_obj, data={"order_status":request.data['status']},partial=True)  # set partial=True to update a data partially
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Order Changed Successfully'}, status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['post'])
    def all_services(self, request):
        category =request.data['category']
        services={}
        all_service_type=Services_Type.objects.all()
        for data in all_service_type:
            pricing_object=Pricing.objects.filter(services_type__services_type_name=data,services_level__services_level_name=category).values('deadline','price')
            services[data.services_type_name]=list(pricing_object)
        pp_json = json.dumps(services)
        loaded_r = json.loads(pp_json)
        return Response({"All Services": loaded_r})

    @action(detail=False, methods=['get'])
    def specific_user_oders(self, request):
        try:
            user_obj = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        oder_data=Order.objects.filter(user=user_obj)
        serializer = OrderSerializer(oder_data, many=True)
        return Response({"AllProfiles": serializer.data})



    @action(detail=False, methods=['patch'])
    def upload_media_coordinator(self, request):
        if request.method == "PATCH":
            try:
                order_obj = Order.objects.get(id=request.data['id'])
            except Order.DoesNotExist:
                return Response({"Message": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ChangeOrderStatusSerializer(order_obj, data=request.data,partial=True)  # set partial=True to update a data partially
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Upload Media file Successfully'}, status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def price_calulator(self, request):
        if request.method == "POST":
            if "services_type_name" in request.data and "services_level_name" in request.data  and "paper_name" in request.data and "deadline" in request.data:
                service_object=Pricing.objects.values_list('id', flat = True).filter(services_type__services_type_name=request.data['services_type_name'],services_level__services_level_name=request.data['services_level_name'],paper_type__paper_name=request.data['paper_name'],deadline=request.data['deadline'])
                if service_object.exists():
                    get_service = Pricing.objects.get(id=service_object[0])
                    pages=request.data['pages']
                    calculated_price=float(get_service.price)*int(pages)
                    print(calculated_price)
                    if "coupen_code" in request.data:
                        coupen_obejct = Coupen.objects.filter(coupen_code=request.data['coupen_code'])
                        if (coupen_obejct).exists():
                            if(coupen_obejct[0].coupen_percentage_price!=None):
                                dis_per_price=coupen_obejct[0].coupen_percentage_price
                                calculated_price = calculated_price - (calculated_price * float(dis_per_price) / 100)
                                return Response({"Service Price": calculated_price,"Percentage Discount":dis_per_price,"Service ID":service_object[0]})
                            else:
                                dis_fix_price=coupen_obejct[0].coupen_fixed_price
                                calculated_price=calculated_price-float(dis_fix_price)
                                return Response({"Service Price": calculated_price,"Fixed Price Discount":dis_fix_price,"Service ID":service_object[0]})
                        return Response({"Message": "Invalid Coupen!!"}, status=status.HTTP_404_NOT_FOUND)
                    return Response({"Service Price": calculated_price,"Service ID":service_object[0]})
                else:

                    return Response({"Message": "Not Found!!"},status=status.HTTP_404_NOT_FOUND)

            return Response({"Error": "Missing Parameter"},status=status.HTTP_400_BAD_REQUEST)


class Coupens(viewsets.ViewSet):#Place order

    @action(detail=False,methods=['post','get','put'])
    def create_coupen(self, request):
        # {
        #     "coupen_name": "testing",
        #     "coupen_percentage_price": "10"
        # }
        if request.method == "POST":
            try:
                def secure_rand(len=8):
                    token = os.urandom(len)
                    return base64.b64encode(token)

                generated_code=secure_rand()
                generated_code=generated_code.decode(encoding="utf-8")
                print(generated_code)
                coupen_obj = Coupen.objects.filter(~Q(coupen_code=generated_code))
                print("============")
                data=request.data
                data['coupen_code']=generated_code
                print(data)
                serializer = CoupenSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"Message": "Coupen Code", "Code": generated_code}, status=status.HTTP_200_OK)
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            except :
                return Response({"Message":"Coupen Already Exist"},status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            all_coupens = Coupen.objects.filter(is_active=True)
            serializer = CoupenSerializer(all_coupens, many=True)
            return Response({"All Coupens": serializer.data})
        if request.method == "PUT":
            # {
            #     "coupen_id": "1"
            # }
            try:
                coupen_obj = Coupen.objects.get(id=request.data['coupen_id'])
            except Coupens.DoesNotExist:
                return Response({"Message": "Coupen does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CoupenSerializer(coupen_obj, data={"is_active":False}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Delete Coupen Successfully!'}, status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Support_Coordinator(viewsets.ViewSet):
    @action(detail=False,methods=['post','patch','get'])
    def support_coordinator(self, request):
        if request.method == "POST":
            try:
                user_obj = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
            data={
                'user':user_obj.id,
                'phone':request.data['phone']
            }
            serializer = SupportSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Successfully!'}, status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == "PATCH":
            try:
                user_obj = User.objects.get(id=request.user.id)
                sup_obj=Support.objects.get(user=user_obj.id)
            except User.DoesNotExist:
                return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

            serializer = SupportSerializer(sup_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Update status Successfully!'}, status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == "GET":
            try:
                user_obj = User.objects.get(id=request.user.id)
                sup_obj = Support.objects.get(user=user_obj.id)
            except User.DoesNotExist:
                return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
            sup_obj = Support.objects.get(user=user_obj.id)
            serializer = SupportSerializer(sup_obj)
            return Response({"Support Coordinator": serializer.data})


class Payments(viewsets.ViewSet):
    @action(detail=False,methods=['post'])
    def create_payment(self, request):
        # print(request.data['idempotency_key'])
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'Bearer '+request.data['token'],
            'Square-Version': '2019-08-14'

        }

        # data ={
        #         "idempotency_key": request.data['idempotency_key'],
        #         "amount_money": {
        #             "amount": request.data['amount'],
        #             "currency": request.data['currency']
        #         },
        #         "source_id": request.data['source_id']
        #
        #     }

        data={
    "idempotency_key": request.data['idempotency_key'],
    "amount_money": {
      "amount": int(request.data['amount']),
      "currency": request.data['currency']
    },
    "source_id": request.data['source_id']

}
        response = requests.post('https://connect.squareupsandbox.com/v2/payments', headers=headers, data=str(data))
        return Response(response.json())




