from django.db import models
from django.core.files.base import ContentFile
from datetime import datetime
from io import BytesIO
from PIL import Image

class Realtor(models.Model):
  name = models.CharField(max_length=50)
  photo = models.ImageField(upload_to='realtors/%Y/%m/%d/', default='images/no_image.png')
  phone = models.CharField(max_length=20)
  email = models.CharField(max_length=100)
  date_hired = models.DateTimeField(default=datetime.now, blank=True)
  top_seller = models.BooleanField(default=False)

  # override the save method and 
  # use the Image class of the PIL package 
  # to convert it to JPEG
  def save(self, *args, **kwargs):
    if self.photo:
      filename = "%s.jpg" % self.photo.name.split('.')[0]
      
      photo = Image.open(self.photo)
      # for PNG images discard the alpha channel and fill it with some color
      if photo.mode in ('RGBA', 'LA'):
        background = Image.new(photo.mode[:-1], photo.size, '#fff')
        background.paste(photo, photo.split()[-1])
        photo = background
        photo_io = BytesIO()
        photo.save(photo_io, format='JPEG', quality=100)
                
        # change the photo field value to be the newly modified photo value
        self.photo.save(filename, ContentFile(photo_io.getvalue()), save=False)
    super(Realtor, self).save(*args, **kwargs)
  
  def __str__(self):
    return self.name
