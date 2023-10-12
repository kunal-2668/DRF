from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login,logout
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
# Create your views here.

class RegisterUser(APIView):
    def post(self,request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'Message':"User Created",                   
                }
            )
        else:
            return Response(serializer.errors)


class LoginUser(APIView):
    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data = data)

        if serializer.is_valid():
            user = authenticate(username = serializer.data['username'],password = serializer.data['password'])
            if user:
                token , _ = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        'Message':"User Login Success",
                        'token' : str(token)                     
                    }
                )
            else:
                return Response({
                    'Message':"Invalid Username/Password",                   
                })
        else:
            return Response(serializer.errors)


@api_view(['GET','POST'])
def index(request):
    if request.method == 'GET':

        data = Person.objects.all()

        serializer = PersonSerializer(data,many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    http_method_names = ['get','post']

    def list(self,request):
        print(request.user)
        search = request.GET.get('search')
        queryset = self.queryset

        if search:
            queryset = queryset.filter(name__startswith = search)

        page = request.GET.get('page',1)
        page_size = 2

        try:
            paginator = Paginator(queryset,page_size)
            serializer = PersonSerializer(paginator.page(page),many=True)
            return Response({'data':serializer.data})

        except Exception as e:
            return Response({
                'Message' : "No page Found"
            })
        