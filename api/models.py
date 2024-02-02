from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, password=None,is_staff=True, is_superuser=False, **extra_fields):
        # extra_fields is assumed to be a dictionary containing additional fields and their values. The double asterisks (**) in front of extra_fields perform dictionary unpacking, passing each key-value pair in extra_fields as a separate keyword argument to the user model's constructor.
        
        
        user = self.model(email=self.normalize_email(email), **extra_fields)  
        # Email address normalization involves converting an email address to a standardized, consistent format. 
        
        
        
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email=self.normalize_email(email),
                                is_active = True,
                                is_staff = True,
                                is_superuser = True,
                                **extra_fields)
        user.set_password(password)
        user.save()
        return user
        

class User(AbstractUser):
    
    username = None 
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)

    objects = UserManager()
    # This line assigns the custom manager UserManager() to the objects attribute of the User model. The UserManager is presumably a custom manager class that may include methods for creating users.

    USERNAME_FIELD = "email"
    # email field should be used as the unique identifier for authentication purposes. This is necessary because the default AbstractUser uses username for authentication.
    
    REQUIRED_FIELDS = []
    # List of fields required for user creation, other than the email and password, but in this case, it's an empty list ([]). If there were additional fields required during user creation, you would list them here.

    

    def __str__(self):
        return str(self.email)
    
    
    # def __str__(self):
    #     return f"email: {self.email}, password: {self.password}"

    
    
    
    
class Buyer(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10,blank=True)
    
    def __str__(self):
        return str(self.id)
    
   



class Seller(models.Model):
    
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10,blank=True)

    def __str__(self):
        return str(self.id)
    

    




class Category(models.Model):
    name = models.CharField(max_length=255)
    

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_quantity= models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    
    
    
    
