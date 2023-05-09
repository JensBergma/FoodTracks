from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from StoreAPI.models import OpeningHours
from StoreAPI.serializer import OpeningHoursSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OpeningHoursListCreateView(generics.ListCreateAPIView):
    queryset = OpeningHours.objects.all()
    serializer_class = OpeningHoursSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['dayOfWeek', 'openingTime',
                     'closingTime', 'isClosed', 'isSpecialTime', 'id']
    ordering_fields = ['dayOfWeek', 'openingTime',
                       'closingTime', 'isClosed', 'isSpecialTime', 'id']
    filterset_fields = ['dayOfWeek', 'openingTime',
                        'closingTime', 'isClosed', 'isSpecialTime', 'id']

    @swagger_auto_schema(
        operation_summary="Get a list of opening hours records",
        operation_description="Retrieve a list of opening hours records with optional search, ordering, and filtering.",
        responses={
            200: "List of opening hours records retrieved successfully",
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create an opening hours record",
        operation_description="Create a new opening hours record.",
        responses={
            201: "Opening hours record created successfully",
            400: "Bad request - Invalid input",
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OpeningHoursRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OpeningHours.objects.all()
    serializer_class = OpeningHoursSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get opening hours details",
        operation_description="Retrieve details of a specific opening hours record.",
        responses={
            200: "Opening hours details retrieved successfully",
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.',
            404: "Opening hours record not found"
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update opening hours",
        operation_description="Update an existing opening hours record.",
        request_body=OpeningHoursSerializer,
        responses={
            200: "Opening hours record updated successfully",
            400: "Invalid data provided",
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.',
            404: "Opening hours record not found"
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete opening hours",
        operation_description="Delete an existing opening hours record.",
        responses={
            204: "Opening hours record deleted successfully",
            401: 'Unauthorized - Authentication credentials were not provided or were invalid.',
            404: "Opening hours record not found"
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
