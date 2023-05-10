from rest_framework import status
from rest_framework.response import Response

from StoreAPI.models import Address, OpeningHours, Store
from StoreAPI.serializer import AddressSerializer, OpeningHoursSerializer
import datetime

class GeneralFuntions:
    def get_instance_or_error(model, object_id, error_message):
        obj = model.objects.filter(id=object_id).first()
        if not obj:
            return Response({"error": "{}{}".format(error_message, object_id)}, status=status.HTTP_400_BAD_REQUEST)
        return obj

    def get_address_list_or_error(address_data, store_id):
        address_list = []

        # check for changes
        keys_to_check = ['location', 'street',
                            'houseNumber', 'postcode']

        for address in address_data:
            address_id = address.pop('id', None)
            if address_id is not None:
                address_instance = GeneralFuntions.get_instance_or_error(
                    Address, address_id, "Invalid addressId: ")
                if isinstance(address_instance, Response):
                    return address_instance

                if any(key in address for key in keys_to_check):
                    key_value_pairs = [(key, address.get(key), getattr(
                        address_instance, key)) for key in keys_to_check if key in address]
                    # check if the values for the keys that are present in both address and address_instance match
                    if all(old_value == new_value for _, old_value, new_value in key_value_pairs):
                        address_list.append(address_instance)
                    else:
                        # check if there is an other store using the same address
                        existing_store = Store.objects.filter(
                            address__id=address_id).exclude(id=store_id).first()
                        if existing_store is not None:
                            return Response({'error': f"Address is already being used by '{existing_store.name}' store and can not be changed."}, status=status.HTTP_400_BAD_REQUEST)

                address_serializer = AddressSerializer(
                    address_instance, data=address, partial=True)
                if address_serializer.is_valid(raise_exception=True):
                    address = address_serializer.save()
                    address_list.append(address)
            else:
                # if this is a new address, check if one with same values already exist
                existing_instance = None
                if all(key in address for key in keys_to_check):
                    existing_instance = Address.objects.filter(
                        street=address['street'],
                        houseNumber=address['houseNumber'],
                        location=address['location'],
                        postcode=address['postcode']
                    ).first()
                if existing_instance:
                    address_list.append(existing_instance)
                else:
                    address_serializer = AddressSerializer(data=address)
                    if address_serializer.is_valid(raise_exception=True):
                        address = address_serializer.save()
                        address_list.append(address)
        return address_list

    def get_opening_hours_list_or_error(openingHours_data, store_id):
        opening_hours_list = []
        keys_to_check = ['dayOfWeek', 'openingTime', 'closingTime'
                    'isClosed', 'isSpecialTime']
        for opening_hours in openingHours_data:
            opening_hours_id = opening_hours.pop('id', None)
            if opening_hours_id is not None:
                openingHours_instance = GeneralFuntions.get_instance_or_error(
                    OpeningHours, opening_hours_id, "Invalid openingHoursId: ")
                if isinstance(openingHours_instance, Response):
                    return openingHours_instance

                # check for changes
                if any(key in opening_hours for key in keys_to_check):
                    key_value_pairs = [(key, opening_hours.get(key), getattr(
                        openingHours_instance, key)) for key in keys_to_check if key in opening_hours]
                    # check if the values for the keys that are present in both address and address_instance match
                    if all(old_value == new_value for _, old_value, new_value in key_value_pairs):
                        opening_hours_list.append(openingHours_instance)
                    else:
                        # check if there is an other opening hour using the same address
                        existing_store = Store.objects.filter(
                            openingHours__id=opening_hours_id).exclude(id=store_id).first()
                        if existing_store is not None:
                            return Response({'error': f"Opening Hour is already being used by '{existing_store.name}' store and can not be changed."}, status=status.HTTP_400_BAD_REQUEST)

                opening_hours_serializer = OpeningHoursSerializer(
                    openingHours_instance, data=opening_hours, partial=True)
                if opening_hours_serializer.is_valid(raise_exception=True):
                    opening_hours = opening_hours_serializer.save()
                    opening_hours_list .append(opening_hours)
            else:
                # if this is a new opening hour, check if one with same values already exist
                existing_instance = None
                keys_to_check = ['dayOfWeek', 'openingTime', 'closingTime']
                if all(key in opening_hours for key in keys_to_check):
                    try:
                        datetime.datetime.strptime(opening_hours['closingTime'], '%H:%M:%S').time()
                        datetime.datetime.strptime(opening_hours['openingTime'], '%H:%M:%S').time()
                        existing_instance = OpeningHours.objects.filter(
                            dayOfWeek=opening_hours['dayOfWeek'],
                            openingTime=opening_hours['openingTime'],
                            closingTime=opening_hours['closingTime'],
                            isClosed=opening_hours.get('isClosed', False),
                            isSpecialTime=opening_hours.get('isSpecialTime', False)
                        ).first()
                    except ValueError:
                         return Response({'error': "Closing Time or Opening Time having an invalid time."}, status=status.HTTP_400_BAD_REQUEST)
                if existing_instance:
                    opening_hours_list.append(existing_instance)
                else:
                    opening_hours_serializer = OpeningHoursSerializer(
                        data=opening_hours)
                    if opening_hours_serializer.is_valid(raise_exception=True):
                        opening_hours = opening_hours_serializer.save()
                        opening_hours_list .append(opening_hours)
        return opening_hours_list
