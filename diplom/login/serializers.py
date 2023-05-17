from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Income


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class IncomeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    amount = serializers.IntegerField(read_only=True)
    time = serializers.DateTimeField()
    category = serializers.CharField(max_length=100)
    paymentMethod = serializers.CharField(max_length=4)

    def create(self, validated_data):
        return Income.objects.create(**validated_data)

    def update(self):
        pass
