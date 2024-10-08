
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Items
from .seriliser import ItemsSerilizer,RegistrationSerializer,LoginSeriliser
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache

# Create your views here.


@api_view(['POST'])
def registration_view(request):
    data=request.data
    seriliser=RegistrationSerializer(data=data)
    if not seriliser.is_valid():
        return Response(seriliser.errors,status=status.HTTP_400_BAD_REQUEST)
    seriliser.save()
    return Response({'Message':"USER CREATED"},status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_view(request):
    data=request.data
    seriliser=LoginSeriliser(data=data)
    
    if not seriliser.is_valid():
        return Response(seriliser.errors,status=status.HTTP_400_BAD_REQUEST)

    username=seriliser.data['username']
    password=seriliser.data['password']
   
    user=authenticate(username=username,password=password)
 
    if user is None:
        return Response({"Error":"Incoorect Password"},status=status.HTTP_400_BAD_REQUEST)
    
    refresh = RefreshToken.for_user(user)

    return Response ({ 'refresh': str(refresh), 'access': str(refresh.access_token),
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    data=request.data
    seriliser=ItemsSerilizer(data=data)
    if not seriliser.is_valid():
        return Response(seriliser.errors,status=status.HTTP_400_BAD_REQUEST)
    
    seriliser.save()
    return Response(seriliser.data,status=status.HTTP_201_CREATED)


class Ineventry_ops_APIView(APIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]

    def get(self,request,pk):
       
        if cache.get(pk):
            obj=cache.get(pk)
            print("Cache Hit ")
            return Response(obj)
        else:
            try:
                obj=Items.objects.filter(id=pk)
                if obj.exists():
                    seriliser=ItemsSerilizer(obj,many=True)
                    cache.set(pk, seriliser.data)
                    print("DB Hit ")
                    return Response(seriliser.data)
            except Exception as error:
                return Response(f'{error}',status=status.HTTP_404_NOT_FOUND)
            
        return Response('Item not found',status=status.HTTP_404_NOT_FOUND)

    def put(self,request,pk):

        data=request.data
        try:
            obj=Items.objects.get(id=pk)
            seriliser=ItemsSerilizer(obj,data=data)

            if seriliser.is_valid():
                seriliser.save()
                return Response(seriliser.data)
        except Exception as e:
            return Response('Item not found',status=status.HTTP_404_NOT_FOUND)
        return Response(seriliser.errors)
      
    def delete(self,request,pk):

        obj=Items.objects.filter(id=pk)
        if not obj.exists():
            return Response('Item not found',status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response({"Msg": "Deletion Successful"},status=status.HTTP_200_OK)


