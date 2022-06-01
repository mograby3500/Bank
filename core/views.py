from rest_framework import generics, viewsets
from .models import *
from .serializers import *
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

class CurrencyListAPIView(generics.ListAPIView):
    queryset= Currency.objects.all()
    serializer_class= CurrencySerializer

    pagination_class= None


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadCategorySerializer
        
        return WriteCategorySerializer

    def get_queryset(self):
        return self.request.user.categories.all()

    
        

class TransactionModelViewSet(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    filter_backends= [SearchFilter, OrderingFilter, DjangoFilterBackend, ]
    search_fields= ["description"]
    ordering_fields= ["amount", "date", "id"]
    filterset_fields= ["currency__code"]
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadTransactionSerializer

        return WriteTransactionSerializer  
    
    def get_queryset(self):
        user= self.request.user 
        return Transaction.objects.filter(user= user).select_related("category", "currency", "user")

    def perform_create(self, serializer):
        serializer.save(date= datetime.now())
    