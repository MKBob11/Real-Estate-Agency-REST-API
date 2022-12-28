from datetime import datetime, timezone, timedelta
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Listing
from .serializers import ListingSerializer, ListingDetailSerializer


class ListingsView(ListAPIView):
  permission_classes = (permissions.AllowAny, )
  queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
  serializer_class = ListingSerializer
  lookup_field = 'slug'

class ListingView(RetrieveAPIView):
  permission_classes = (permissions.IsAuthenticated, )
  queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
  serializer_class = ListingDetailSerializer
  lookup_field = 'slug'

class SearchView(APIView):
  permission_classes = (permissions.AllowAny, )
  serializer_class = ListingSerializer

  def post(self, request, format=None):
    queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
    data = self.request.data 

    sale_type = data['sale_type']
    queryset = queryset.filter(sale_type__iexact=sale_type)

    price = data['price']
    if price == '€0+':
      price = 0
    elif price == '€200,000+':
      price = 200000
    elif price == '€400,000+':
      price = 400000
    elif price == '€600,000+':
      price = 600000
    elif price == '€800,000+':
      price = 800000
    elif price == '€1,000,000+':
      price = 1000000
    elif price == '€1,200,000+':
      price = 1200000
    elif price == '€1,500,000+':
      price = 1500000
    elif price == 'Any':
      price = -1
      
    if price != -1:
      queryset = queryset.filter(price__gte=price)

    beds = data['beds']
    if beds == '0+':
      beds = 0
    elif beds == '1+':
      beds = 1
    elif beds == '2+':
      beds = 2
    elif beds == '3+':
      beds = 3
    elif beds == '4+':
      beds = 4
    elif beds == '5+':
      beds = 5

    queryset = queryset.filter(beds__gte=beds)

    home_type = data['home_type']
    queryset = queryset.filter(home_type__iexact=home_type)
    
    baths = data['baths']
    if baths == '0+':
      baths = 0.0
    elif baths == '1+':
      baths = 1.0
    elif baths == '2+':
      baths = 2.0
    elif baths == '3+':
      baths = 3.0
    elif baths == '4+':
      baths = 4.0

    queryset = queryset.filter(baths__gte=baths)
    
    size_square_metres = data['size_square_metres']
    if size_square_metres == '50+':
      size_square_metres = 50
    elif size_square_metres == '100+':
      size_square_metres = 100
    elif size_square_metres == '200+':
      size_square_metres = 200
    elif size_square_metres == '500+':
      size_square_metres = 500
    elif size_square_metres == '1000+':
      size_square_metres = 1000
    elif size_square_metres == 'Any':
      size_square_metres = 0

    if size_square_metres != 0:
      queryset = queryset.filter(size_square_metres__gte=size_square_metres)
      
    days_passed = data['days_listed']
    if days_passed == '1 or less':
      days_passed = 1
    elif days_passed == '2 or less':
      days_passed = 2
    elif days_passed == '5 or less':
      days_passed = 5
    elif days_passed == '10 or less':
      days_passed = 10
    elif days_passed == '20 or less':
      days_passed = 20
    elif days_passed == 'Any':
      days_passed = 0

    for query in queryset:
      num_days = (datetime.now(timezone.utc) - query.list_date).days
      
      if days_passed != 0:
        if num_days > days_passed:
          slug = query.slug
          queryset = queryset.exclude(slug__iexact=slug)

    has_photos = data['has_photos']
    if has_photos == '1+':
      has_photos = 1
    elif has_photos == '3+':
      has_photos = 3
      
    for query in queryset:
      count = 0
      if query.photo_1: # if photo_1 exists etc.
        count += 1
      if query.photo_2:
        count += 1
        
      if count < has_photos:
        slug = query.slug
        queryset = queryset.exclude(slug__iexact=slug)

    open_house = data['open_house']
    queryset = queryset.filter(open_house__iexact=open_house)

    keywords = data['keywords']
    queryset = queryset.filter(description__icontains=keywords)

    serializer = ListingSerializer(queryset, many=True)

    return Response(serializer.data)
