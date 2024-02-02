from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin
from .models import Product,Category,User,Buyer,Seller
from .serializers import ProductSerializer,CategorySerializer,UsersSerializer,BuyerSerializer,SellerSerializer,LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
import jwt
from datetime import datetime, timedelta
from django.core.cache import cache


class IsSeller(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     user = request.user
    #     seller = Seller.objects.filter(user_id = user.id).first()
    #     if seller and seller.id == obj.id:
    #         return True
    #     return False
    
    
    def has_permission(self, request, view):
        user = request.user
        return Seller.objects.filter(user_id=user.id).exists()
    

# Create your views here.
class ProductDetailView(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSeller]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  
    
    # The serializer is responsible for converting complex data types, such as Django models, into Python data types that can be easily rendered into JSON and vice versa.
    
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        self.destroy(request,*args,**kwargs)
        return Response({"Message":"Product Deleted Successfully"})
    
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
    
class CategoryDetailView(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def put(self,request,*args,**kwargs):
        self.update(request,*args,**kwargs)
        return Response({"Message":"Category Updated Successfully"})
    
    def delete(self,request,*args,**kwargs):
        self.destroy(request,*args,**kwargs)
        return Response({"Message":"Category Deleted Successfully"})
    
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
# ========================================================================================================================== 



    
    


    
    
class CategoryCreateView(GenericAPIView,CreateModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
    
class ProductCreateView(GenericAPIView,CreateModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSeller]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
    
# ==========================================================================================================================   


class ProductListView(GenericAPIView,ListModelMixin):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = '__all__'
    
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
class CategoryListView(GenericAPIView,ListModelMixin):
    

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = '__all__'
    
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
    
# ========================================================================================================================== 



class UsersCreateView(GenericAPIView,CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class BuyerCreateView(GenericAPIView,CreateModelMixin):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class SellerCreateView(GenericAPIView,CreateModelMixin):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
    
    


    
    
    
    
    
def authenticate_user(serializer):
    user = User.objects.get(email= serializer.validated_data['email'])
    if user is None:
        raise ValidationError("Invalid username/password. Please try again!")
    return user

class LoginAPIView(APIView):
    
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate_user(serializer)
            # user = User.objects.get(email = serializer.validated_data['email'])
            
            refresh = RefreshToken.for_user(user)
            
            return Response({"message":"User Logged In Successfully",
                             "payload":serializer.validated_data,
                             'refresh': str(refresh),
                             'access': str(refresh.access_token),})
            
            
class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =[IsAuthenticated]
    
    def post(self, request, format=None):
        if request.user.is_authenticated:
            print(request)
            authorization_header = request.headers.get('Authorization')
            if authorization_header and authorization_header.startswith('Bearer '):
                bearer_token = authorization_header.split(' ')[1]
                try:
                    token = RefreshToken(str(bearer_token))
                    token.blacklist()

                
                except Exception as e:
                    # return Response({'detail': 'Invalid token or token has expired.'}, status=400)
                    pass
            
            logout(request)
            return Response({"detail": "Logout successful."})
        else:
            return Response({"detail": "User not authenticated."})
        
        
        

    
    
    
    
    

