from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from blog.models import UserProfile
from property.models import PropertyListing
from property.api.serializers import PropertyListingSerializer
from django.contrib.auth.models import User


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_view(request, slug):

    try:
        property_listing = PropertyListing.objects.get(slug=slug)

    except PropertyListing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PropertyListingSerializer(property_listing)

    return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_property_view(request, slug):

    try:
        property_listing = PropertyListing.objects.get(slug=slug)

    except PropertyListing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if PropertyListing.owner != user:
        return Response({'response': "You dont have enough permissions for that"})

    serializer = PropertyListingSerializer(property_listing, data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["success"] = "updated success"
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST', ])
# @permission_classes((IsAuthenticated,))
# def api_delete_property_view(request, slug):
#
#     try:
#         property_listing = PropertyListing.objects.get(slug=slug)
#
#     except PropertyListing.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     user = request.user
#     if PropertyListing.owner != user:
#         return Response({'response': "You dont have enough permissions for that"})
#
#     operation = property_listing.delete()
#     data = {}
#     if operation:
#         data["success"] = "deleted success"
#     else:
#         data["faliure"] = "failed"
#     return Response(data=data)


# @api_view(['POST', ])
# @permission_classes((IsAuthenticated,))
# def api_create_property_view(request):
#
#     account = request.user
#     property_listing = PropertyListing(owner=account)
#
#     serializer = PropertyListingSerializer(property_listing, data=request.data)
#     deta = {}
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPropertyListView(ListAPIView):
    queryset = PropertyListing.objects.filter(Verify='N')
    serializer_class = PropertyListingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'city', 'zipcode',
                     'price', 'sqft', 'owner__username')


class followview(APIView):

    def post(self,request):

        for each in request.data:

            p1 = request.data[each]['title']
            status1 = request.data[each]['status']

            prop = PropertyListing.objects.get(title=p1)

            if status1=='Accepted':

                prop.Verify='V'
                prop.save()

            else:

                prop.Verify='R'
                prop.save()
                return Response("fknlenl")
