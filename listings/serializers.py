from rest_framework import serializers
from .models import Listing

# data that will be available for all users
class ListingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Listing
    fields = ('sale_type', 'home_type', 'price', 'title', 'slug', 'description', 'address', 'city', 'zipcode', 'beds', 'baths', 'size_square_metres', 'photo_main')


# all data will be available only for the authenticated users
class ListingDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Listing
    fields = '__all__'
    lookup_field = 'slug'
