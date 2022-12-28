from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import get_user_model
User = get_user_model()

class SignupView(APIView):
  permission_classes = (permissions.AllowAny, )

  def post(self, request, format=None):
    data = self.request.data 
    
    name = data['name']
    email = data['email']
    password = data['password']
    password2 = data['password2']
    
    if password == password2:
      if User.objects.filter(email=email).exists():
        return Response({'error': 'The email address you have provided is already in use. Please use a different email address.'})
      else:
        if len(password) < 8:
          return Response({'error': 'Your password must be at least 8 characters long.'})
        else:
          user = User.objects.create_user(email=email, password=password, name=name)
          user.save()
          return Response({'success': 'Your user account has been created successfully.'})
    else:
      return Response({'error': 'Those passwords did not match. Try again.'})
