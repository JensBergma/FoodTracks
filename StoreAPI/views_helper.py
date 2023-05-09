from rest_framework import status
from rest_framework.response import Response

from StoreAPI.models import Address, OpeningHours
from StoreAPI.serializer import AddressSerializer, OpeningHoursSerializer

class GeneralFuntions:
    def get_instance_or_error(model, object_id, error_message):
        obj = model.objects.filter(id=object_id).first()
        if not obj:
            return Response({"error": "{}{}".format(error_message, object_id)}, status=status.HTTP_400_BAD_REQUEST)
        return obj

    def get_address_list_or_error(address_data):
        address_list = []
        for address in address_data:
            address_id = address.pop('id', None)
            if address_id is not None:
                address_instance = GeneralFuntions.get_instance_or_error(Address, address_id, "Invalid addressId: ")
                if isinstance(address_instance, Response):
                    return address_instance
                address_serializer = AddressSerializer(address_instance, data=address, partial=True)
                if address_serializer.is_valid(raise_exception=True):
                    address = address_serializer.save()
                    address_list.append(address)
            else:
                address_serializer = AddressSerializer(data=address)
                if address_serializer.is_valid(raise_exception=True):
                    address = address_serializer.save()
                    address_list.append(address)
        return address_list

    def get_opening_hours_list_or_error(openingHours_data, storeId):
        opening_hours_list = []
        for opening_hours in openingHours_data:
            opening_hours_id = opening_hours.pop('id', None)
            opening_hours['store'] = storeId
            if opening_hours_id is not None:
                openingHours_instance_or_error = GeneralFuntions.get_instance_or_error(OpeningHours, opening_hours_id, "Invalid openingHoursId: ")
                if isinstance(openingHours_instance_or_error, Response):
                    return openingHours_instance_or_error
                opening_hours_serializer = OpeningHoursSerializer(openingHours_instance_or_error, data=opening_hours, partial=True)
                if opening_hours_serializer.is_valid(raise_exception=True):
                    opening_hours = opening_hours_serializer.save()
                    opening_hours_list .append(opening_hours)
            else:
                opening_hours_serializer = OpeningHoursSerializer(data=opening_hours)
                if opening_hours_serializer.is_valid(raise_exception=True):
                    opening_hours = opening_hours_serializer.save()
                    opening_hours_list .append(opening_hours)
        return opening_hours_list