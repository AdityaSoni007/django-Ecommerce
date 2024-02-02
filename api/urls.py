from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:pk>',views.ProductDetailView.as_view(),name='product-information'),
    path('category/<int:pk>',views.CategoryDetailView.as_view(),name='category-information'),
    
    
    path('create-product',views.ProductCreateView.as_view(),name='product-create'),
    path('create-category',views.CategoryCreateView.as_view(),name='category-create'),
    
    
    
    path('products',views.ProductListView.as_view(),name='product-info'),
    path('categorys',views.CategoryListView.as_view(),name='category-info'),
    
    
    
    path('register-admin',views.UsersCreateView().as_view()),
    path('register-seller',views.SellerCreateView().as_view()),
    path('register-buyer',views.BuyerCreateView().as_view()),
    
    
    path('login', views.LoginAPIView().as_view()),
    path('logout', views.LogoutAPIView().as_view()),
    
]