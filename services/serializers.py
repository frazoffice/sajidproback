from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response
from core.models import User_Profile
from rest_framework import serializers

from services.models import Order, Pricing, Paper_type, Services_Level, Services_Type, Coupen


class ServicesLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Services_Level
        fields= "__all__"

class PaperTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Paper_type
        fields= "__all__"

class ServicesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Services_Type
        fields= "__all__"

class PricingSerializer(serializers.ModelSerializer):
    services_level = ServicesLevelSerializer()
    services_type=ServicesTypeSerializer()
    paper_type=PaperTypeSerializer()
    class Meta:
        model=Pricing
        fields= ["id","price","services_level","services_type","paper_type","deadline"]
        # fields= "__all__"


class OrderSerializer(serializers.ModelSerializer):

    pricing = PricingSerializer()
    class Meta:
        model=Order
        fields= ["order_price","media_file","topic","deadline","description","total_price","order_status","is_active","topic","total_pages","actual_price","pricing"]
        # fields= "__all__"
        # extra_field=["services_type"]



class SaveOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model=Order
        # fields= ["topic","total_pages","pricing"]
        fields= "__all__"
        # extra_field=["services_type"]

class ChangeOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields= "__all__"


class CoupenSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupen
        fields= "__all__"


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pricing
        fields= "__all__"

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response({"Success": "msb blablabla"})


