from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Category, Customization, MenuItem
from .serializers import CategorySerializer, CustomizationSerializer, MenuItemSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomizationViewSet(viewsets.ModelViewSet):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminUser]