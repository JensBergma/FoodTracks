from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema

from StoreAPI.models import Address
from StoreAPI.serializer import AddressSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['street', 'location', 'postcode', 'houseNumber', 'id']
    ordering_fields = ['street', 'location', 'postcode', 'houseNumber', 'id']
    filterset_fields = ['street', 'location', 'postcode', 'houseNumber', 'id']

    @swagger_auto_schema(
        operation_summary='Get list of addresses',
        operation_description='Get a paginated list of all addresses. You can filter the results by using the search and filter parameters.',
        responses={
            200: 'OK - Returns a paginated list of addresses.',
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Create new address',
        operation_description='Create a new address.',
        request_body=AddressSerializer,
        responses={
            201: 'Created - The address was created successfully.',
            400: 'Bad Request - The request was invalid or cannot be served.',
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.'
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get address details",
        operation_description="Retrieve details of a specific address record.",
        responses={
            200: "Address details retrieved successfully",
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.',
            404: "Address record not found"
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update address",
        operation_description="Update an existing address record.",
        request_body=AddressSerializer,
        responses={
            200: "Address record updated successfully",
            400: "Invalid data provided",
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.',
            404: "Address record not found"

        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete address",
        operation_description="Delete an existing address record.",
        responses={
            204: "Address record deleted successfully",
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.',
            404: "Address record not found"
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
