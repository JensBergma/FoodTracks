from rest_framework import serializers
from .models import Address, Store, OpeningHours


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'houseNumber', 'location', 'postcode']


class OpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = ['id', 'dayOfWeek', 'openingTime', 'closingTime', 'isClosed', 'isSpecialTime']


class StoreSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True, read_only=True)
    openingHours = OpeningHoursSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ['id', 'name', 'address', 'openingHours']
