from rest_framework import serializers
from .models import Product,Category,User,Buyer,Seller
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, data):
        category_data = data.pop('category')
        print(category_data.get('name'))
        
        try:
            category = Category.objects.get(name=category_data.get('name'))
            print(category)
            product_instance = Product.objects.create(category=category, **data)
            return product_instance
        
        except:
            raise ValidationError({"message":"Category not found"})
        
        
        # category_instance = Category.objects.create(**category_data)
        
        
    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        
        try:
            category = Category.objects.get(name=category_data.get('name'))
            print(category)
            instance.product_name = validated_data.get('product_name', instance.product_name)
            instance.product_quantity = validated_data.get('product_quantity', instance.product_quantity)
            instance.category = validated_data.get('category',instance.category)
            instance.save()
            return instance  
            
            
        except:
            raise ValidationError({"message":"Category not found"})
        
        
        
        # Add more fields as needed

        

        



class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, data):
        
        
        phone_number = data.get('phone_number', None)
        email = data.get('email')
        
        if not email:
            raise ValidationError("The Email field must be set")

        if phone_number and len(phone_number) != 10:
            raise ValidationError("Phone number should be of 10 digits")

        if len(data['password']) < 8:
            raise ValidationError("Password should be of at least 8 characters")

        password = data.pop('password')
        user = User(**data)            # The **data syntax is used for unpacking the dictionary into keyword arguments.
        user.set_password(password)  
        user.save()
        
        # user = User.objects.get(email = data.get('email'))
        # serializer = UsersSerializer(user)
        # print(serializer.data)
        # print(type(serializer.data))
        # refresh = RefreshToken.for_user(user)
        # response = serializer.data
        # response.access_token= str(refresh.access_token)
        
        
        print(type(user))
        print(user)

        # return Response({"message":"User Logged In Successfully",
        #                 "payload":user,
        #                 #'refresh': str(refresh),
        #                 'access': str(refresh.access_token),})
        
        return user


class SellerSerializer(serializers.ModelSerializer):
    user_id = UsersSerializer()
    class Meta:
        model = Buyer
        fields = '__all__'


    
    def create(self, data):
        user_data = data.pop('user_id')
        user_instance = User.objects.create(**user_data)
        seller_instance = Seller.objects.create(user_id=user_instance, **data)
        
        return seller_instance


class BuyerSerializer(serializers.ModelSerializer):
    user_id = UsersSerializer()
    
    class Meta:
        model = Buyer
        fields = '__all__'


    
    def create(self, data):
        user_data = data.pop('user_id')
        user_instance = User.objects.create(**user_data)
        buyer_instance = Buyer.objects.create(user_id=user_instance, **data)
        
        return buyer_instance
    
    
    
class LoginSerializer(serializers.Serializer):
        email = serializers.CharField(max_length=300, required=True)
        password = serializers.CharField(required=True, write_only=True)
     