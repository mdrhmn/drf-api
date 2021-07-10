from rest_framework import serializers
from django.contrib.auth.models import User, Group

from .models import *

"""
There are 2 main types of serializers:

1. HyperlinkedModelSerializer. 
he HyperlinkedModelSerializer class is similar to the ModelSerializer class except that it uses hyperlinks 
to represent relationships, rather than primary keys.
"""


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # Shortcut for getting all fields
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


"""
2. ModelSerializer
The ModelSerializer class provides a shortcut that lets you automatically create a Serializer class with 
fields that correspond to the Model fields.
"""


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        # fields = ('id', 'title', 'description', 'completed')
        # Shortcut for getting all fields
        fields = '__all__'
