from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema

from .views_helper import GeneralFuntions
from .models import Store
from .serializer import StoreSerializer

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class StoreListCreateView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'address__street', 'address__location', 'address__postcode', 'openingHours__dayOfWeek', 'address__id', 'openingHours__id', 'id']
    ordering_fields = ['name', 'address__street', 'address__location', 'address__postcode', 'openingHours__dayOfWeek', 'address__id', 'openingHours__id', 'id']
    filterset_fields = ['name', 'address__street', 'address__location', 'address__postcode', 'openingHours__dayOfWeek', 'address__id', 'openingHours__id', 'id']

    def create(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            store = serializer.save()
            address_data = request.data.pop('address', None)
            if address_data is not None:
                address_list = GeneralFuntions.get_address_list_or_error(address_data)
                if isinstance(address_list, Response):
                    return address_list
                store.address.set(address_list)

            opening_hours_data = request.data.pop('openingHours', None)
            if opening_hours_data is not None:
                opening_hours_list = GeneralFuntions.get_opening_hours_list_or_error(opening_hours_data, store.id)
                if isinstance(opening_hours_list, Response):
                    return opening_hours_list
            store.openingHours.set(opening_hours_list)

            serialized_data = self.get_serializer(store).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Get list of stores',
        operation_description='Get a paginated list of all stores. You can filter the results by using the search and filter parameters.',
        responses={
            200: 'OK - Returns a paginated list of stores.',
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Create new stores',
        operation_description='Create a new stores. It also can create a Address or a Opening Hour',
        request_body=StoreSerializer,
        responses={
            201: 'Created - The stores was created successfully.',
            400: 'Bad Request - The request was invalid or cannot be served.',
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class StoreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            store = serializer.save()
            address_data = request.data.pop('address', None)
            if address_data is not None:
                address_list = GeneralFuntions.get_address_list_or_error(address_data)
                if isinstance(address_list, Response):
                    return address_list
                store.address.set(address_list)

            opening_hours_data = request.data.pop('openingHours', None)
            if opening_hours_data is not None:
                opening_hours_list = GeneralFuntions.get_opening_hours_list_or_error(opening_hours_data, store.id)
                if isinstance(opening_hours_list, Response):
                    return opening_hours_list
                store.openingHours.set(opening_hours_list)

            return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Get store details",
        operation_description="Retrieve details of a specific store record.",
        responses={
            200: "Store details retrieved successfully",
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.',
            404: "Store record not found"
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update store",
        operation_description="Update an existing store record. Can also update a Address or Opening Hour",
        request_body=StoreSerializer,
        responses={
            200: "Store record updated successfully",
            400: "Invalid data provided",
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.',
            404: "Store record not found"
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete store",
        operation_description="Delete an existing store record.",
        responses={
            204: "Store record deleted successfully",
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.',
            404: "Store record not found"
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

