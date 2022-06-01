from rest_framework import serializers
from .models import * 
from django.contrib.auth.models import User

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model= Currency 
        fields= ['id', 'code', 'name']


class WriteCategorySerializer(serializers.ModelSerializer):
    user= serializers.HiddenField(default= serializers.CurrentUserDefault())
    class Meta:
        model= Category
        fields= ['user', 'id', 'name', ]


class ReadCategorySerializer(serializers.ModelSerializer):
    user= serializers.SlugRelatedField(slug_field= 'username', queryset= User.objects.all())
    class Meta:
        model= Category
        fields= ['id', 'name', 'user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= [
            'id',
            'username'
        ]
    

class WriteTransactionSerializer(serializers.ModelSerializer):
    user= serializers.HiddenField(default= serializers.CurrentUserDefault())
    currency= serializers.SlugRelatedField(slug_field= 'code', queryset= Currency.objects.all())
    category= serializers.SlugRelatedField(slug_field= 'name', queryset= Category.objects.all())
    class Meta:
        model= Transaction
        fields= [
            'user',
            'amount',
            'currency',
            'description',
            'category'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user= self.context['request'].user
        self.fields['category'].queryset= user.categories.all()

class ReadTransactionSerializer(serializers.ModelSerializer):
    currency= CurrencySerializer()
    category= ReadCategorySerializer()
    user= serializers.SlugRelatedField(slug_field= 'username', queryset= User.objects.all())

    class Meta:
        model= Transaction
        fields= [
            'user',
            'id',
            'amount',
            'currency',
            'date',
            'description',
            'category'
        ]

        read_only_fields= fields