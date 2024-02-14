from rest_framework import serializers

from .models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    students = StudentSerializer(read_only=True, many=True)
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, order):
        return order.owner.name

    def get_moderator(self, order):
        if order.moderator:
            return order.moderator.name

        return ""

    class Meta:
        model = Order
        fields = "__all__"


class OrdersSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, order):
        return order.owner.name

    def get_moderator(self, order):
        if order.moderator:
            return order.moderator.name

        return ""

    class Meta:
        model = Order
        fields = "__all__"