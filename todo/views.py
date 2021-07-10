from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import generics, permissions, viewsets, status
from django.contrib.auth.models import User, Group

"""
Method 1: Generics
REST framework provides a set of already mixed-in generic class-based views that we can use to trim down our views.py module even more.
GenericViewSet inherits from GenericAPIView but does not provide any implementations of basic actions. Just only get_object, get_queryset.

To create CRUD, Generics needs two classes(ListCreateAPIView and RetrieveUpdateDestroyAPIView.
"""

"""
8 types of permission classes:
1. AllowAny
The AllowAny permission class will allow unrestricted access, regardless of if the request was authenticated or unauthenticated.
This permission is not strictly required, since you can achieve the same result by using an empty list or tuple for the permissions setting, 
but you may find it useful to specify this class because it makes the intention explicit.

2. IsAuthenticated
The IsAuthenticated permission class will deny permission to any unauthenticated user, and allow permission otherwise.
This permission is suitable if you want your API to only be accessible to registered users.

3. IsAdminUser
The IsAdminUser permission class will deny permission to any user, unless user.is_staff is True in which case permission will be allowed.
This permission is suitable is you want your API to only be accessible to a subset of trusted administrators.

4. IsAuthenticatedOrReadOnly
The IsAuthenticatedOrReadOnly will allow authenticated users to perform any request. Requests for unauthorised users will only be permitted 
if the request method is one of the "safe" methods; GET, HEAD or OPTIONS.
This permission is suitable if you want to your API to allow read permissions to anonymous users, and only allow write permissions to authenticated users.

5. DjangoModelPermissions
This permission class ties into Django's standard django.contrib.auth model permissions. This permission must only be applied to views that has a .queryset property set. 
Authorization will only be granted if the user is authenticated and has the relevant model permissions assigned.

6. DjangoModelPermissionsOrAnonReadOnly
Similar to DjangoModelPermissions, but also allows unauthenticated users to have read-only access to the API.

7. DjangoObjectPermissions
This permission class ties into Django's standard object permissions framework that allows per-object permissions on models. In order to use this permission class, 
you'll also need to add a permission backend that supports object-level permissions, such as django-guardian.
As with DjangoModelPermissions, this permission must only be applied to views that have a .queryset property. Authorization will only be granted if the user is authenticated 
and has the relevant per-object permissions and relevant model permissions assigned.

8. TokenHasReadWriteScope
This permission class is intended for use with either of the OAuthAuthentication and OAuth2Authentication classes, and ties into the scoping that their backends provide.
"""

class TodoList(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    # View-level permissions
    # IsAuthenticatedOrReadOnly, which will ensure that authenticated requests get read-write access,
    # and unauthenticated requests get read-only access.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TodoSerializer


class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    # View-level permissions
    # IsAuthenticatedOrReadOnly, which will ensure that authenticated requests get read-write access,
    # and unauthenticated requests get read-only access.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TodoSerializer


"""
Method 2: APIView
We can also write our API views using class-based views, rather than function based views. As we'll see this is a powerful pattern that allows us to reuse common functionality, 
and helps us keep our code DRY.
"""

# class TodoList(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     """
#     List all todos, or create a new todo.
#     """
#     def get(self, request, format=None):
#         todos = Todo.objects.all()
#         serializer = TodoSerializer(todos, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = TodoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TodoDetail(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     """
#     Retrieve, update or delete a todo instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Todo.objects.get(pk=pk)
#         except Todo.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         todo = self.get_object(pk)
#         serializer = TodoSerializer(todo)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         todo = self.get_object(pk)
#         serializer = TodoSerializer(todo, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         todo = self.get_object(pk)
#         todo.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""
Method 3: Function-based views
"""

# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import *
# from .serializers import *

# # FBV for list of all Todo objects
# @api_view(['GET', 'POST'])
# def todo_list(request):
#     """
#     List all code todos, or create a new todo.
#     """
#     if request.method == 'GET':
#         todos = Todo.objects.all()
#         serializer = TodoSerializer(todos, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = TodoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def todo_detail(request, pk):
#     """
#     Retrieve, update or delete a code todo.
#     """
#     try:
#         todo = Todo.objects.get(pk=pk)
#     except todo.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = TodoSerializer(todo)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = TodoSerializer(todo, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         todo.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""
Method 4: Viewsets

ModelViewSet inherits from GenericAPIView and includes implementations for various actions. 
In other words you don't need implement basic actions as list, retrieve, create, update or destroy. 
Of course you can override them and implement your own list or your own create methods.

ModelViewSet support creating url pattern automatically with DRF router. But Generics don't. you do yourself.
To create CRUD, Generics needs two classes(ListCreateAPIView and RetrieveUpdateDestroyAPIView). 
But ModelViewSet needs only one class(ModelViewSet)
"""

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]