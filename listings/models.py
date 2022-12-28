from django.db import models
from django.utils.timezone import now
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
from realtors.models import Realtor


class Listing(models.Model):
  class SaleType(models.TextChoices):
    FOR_RENT = 'For Rent'
    FOR_SALE = 'For Sale'
        
  class HomeType(models.TextChoices):
    APARTMENT = 'Apartment'
    STUDIO_APARTMENT = 'Studio Apartment'
    HOUSE = 'House'
    DETACHED_HOUSE = 'Detached House'
    SEMI_DETACHED_HOUSE = 'Semi-Detached House'
    TERRACED_HOUSE = 'Terraced House'
    TOWNHOUSE = 'Townhouse'
    DUPLEX = 'Duplex'
    SITE = 'Site'

  realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
  sale_type = models.CharField(max_length=50, choices=SaleType.choices, default=SaleType.FOR_SALE)
  home_type = models.CharField(max_length=50, choices=HomeType.choices, default=HomeType.APARTMENT)
  price = models.IntegerField()
  title = models.CharField(max_length=150)
  slug = models.CharField(max_length=200, unique=True)
  description = models.TextField(blank=True)
  address = models.CharField(max_length=150)
  city = models.CharField(max_length=100)
  zipcode = models.CharField(max_length=15)
  beds = models.IntegerField()
  baths = models.DecimalField(max_digits=2, decimal_places=1)
  size_square_metres = models.IntegerField()
  open_house = models.BooleanField(default=False)
  photo_main = models.ImageField(upload_to='listings/%Y/%m/%d/', default='images/no_image.png')
  photo_1 = models.ImageField(upload_to='listings/%Y/%m/%d/', blank=True)
  photo_2 = models.ImageField(upload_to='listings/%Y/%m/%d/', blank=True)
  is_published = models.BooleanField(default=True)
  list_date = models.DateTimeField(default=now, blank=True)

  # override the save method and 
  # use the Image class of the PIL package 
  # to convert it to JPEG
  def save(self, *args, **kwargs):
    if self.photo_main:
      filename = "%s.jpg" % self.photo_main.name.split('.')[0]
      
      photo_main = Image.open(self.photo_main)
      # for PNG images discard the alpha channel and fill it with some color
      if photo_main.mode in ('RGBA', 'LA'):
        background = Image.new(photo_main.mode[:-1], photo_main.size, '#fff')
        background.paste(photo_main, photo_main.split()[-1])
        photo_main = background
        photo_io = BytesIO()
        photo_main.save(photo_io, format='JPEG', quality=100)
                
        # change the photo field value to be the newly modified photo value
        self.photo_main.save(filename, ContentFile(photo_io.getvalue()), save=False)
    super(Listing, self).save(*args, **kwargs)

  def __str__(self):
    return self.title
