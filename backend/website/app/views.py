from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status, generics

from .permissions import IsOwnerOrReadOnly
from .models import Task
from django.contrib.auth.models import User

from .serializers import UserSerializer, TaskSerializer, PasswordChangeSerializer, PaginationSerializer, UserTypeSerializer, UserTasksSerializer, SortBySerializer, ContactSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotAuthenticated
from rest_framework.request import HttpRequest


# Create your views here.
@api_view(['GET'])
def get_all_routes(req: HttpRequest):
    try:
        routes = {reverse('show-routes'): {'GET': 'Shows all routes'},
                  reverse('login'): {'POST': 'Login'},
                  reverse('auth'): {'POST': 'Authenticate'},
                  reverse('change-password'): {'PUT': 'Change password'},
                  reverse('manage-user'): {'GET': 'Get user details', 'POST': 'Create user'},
                  reverse('manage-users'): {'POST': 'Manage users'},
                  reverse('manage-task', args=[1])+'<int:id>': {'GET': 'Get task details', 'PUT': 'Update task', 'DELETE': 'Delete task'},
                  reverse('manage-tasks'): {'POST': 'Manage tasks'},
                  reverse('create-task'): {'POST': 'Create task'},
                  # Class based views
                  reverse('class-show-routes'): {'GET': 'Shows all routes (CLASS-BASED)'},
                  reverse('class-login'): {'POST': 'Login (CLASS-BASED)'},
                  reverse('class-auth'): {'POST': 'Authenticate (CLASS-BASED)'},
                  reverse('class-change-password'): {'PUT': 'Change password (CLASS-BASED)'},
                  reverse('class-manage-user'): {'GET': 'Get user details', 'POST': 'Create user (CLASS-BASED)'},
                  reverse('class-manage-users'): {'POST': 'Manage users (CLASS-BASED)'},
                  reverse('class-manage-task', args=[1])+'<int:id>': {'GET': 'Get task details', 'PUT': 'Update task', 'DELETE': 'Delete task (CLASS-BASED)'},
                  reverse('class-manage-tasks'): {'POST': 'Manage tasks (CLASS-BASED)'},
                  reverse('class-create-task'): {'POST': 'Create task (CLASS-BASED)'},
                  reverse('class-show-users'): {'GET': 'Shows all users (generics) (CLASS-BASED)'},
                  }
        return Response(routes)
    except Exception as e:
        print(e)
        return Response({"detail": "There was an unknown error"})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def login(req: HttpRequest):
    user = authenticate(
        username=req.data['username'], password=req.data['password'])
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=401)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([JWTAuthentication])
def auth(req: HttpRequest):
    if req.user.is_authenticated != True:
        raise NotAuthenticated()
    return Response('success')


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def contact(req):
    contact_serializer = ContactSerializer(data=req.data)
    if contact_serializer.is_valid():
        name = contact_serializer.data.get('name')
        email = contact_serializer.data.get('email')
        subject = contact_serializer.data.get('subject')
        message = contact_serializer.data.get('message')
        try:
            send_mail(
                subject=f"Contact Form: {subject}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=email,
                # Replace with your Mailhog email address
                recipient_list=['your-email@example.com'],
            )
            return Response({'detail': 'Email sent successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({'detail': 'Could not connect to the email server.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def change_password(req: HttpRequest):
    serializer = PasswordChangeSerializer(
        data=req.data, context={'request': req})
    if serializer.is_valid():
        user = req.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@authentication_classes([JWTAuthentication])
def manage_user(req: HttpRequest):
    try:
        if req.method == 'GET':
            if req.user.is_authenticated != True:
                raise NotAuthenticated()
            queryset = User.objects.get(id=req.user.id)
            serializer = UserSerializer(queryset)
            return Response(serializer.data)

        elif req.method == 'POST':
            if not ('application/x-www-form-urlencoded' in req.content_type or 'multipart/form-data' in req.content_type):
                return Response({'detail': 'Unsupported media type. Only form data is accepted.'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            serializer = UserSerializer(data=req.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except NotAuthenticated as e:
        raise NotAuthenticated()
    except Exception as e:
        print(e)
        return Response({"detail": "There was an unknown error"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def manage_users(req: HttpRequest):
    try:
        user_type_serializer = UserTypeSerializer(data=req.data)
        if user_type_serializer.is_valid():
            if user_type_serializer.data.get('type') == 'default':
                if req.user.is_authenticated != True:
                    raise NotAuthenticated()
                queryset = User.objects.all()
                serializer = UserSerializer(queryset, many=True)
                return Response(serializer.data)
            elif user_type_serializer.data.get('type') == 'user_tasks':
                if req.user.is_authenticated != True:
                    raise NotAuthenticated()
                queryset = User.objects.all()
                serializer = UserTasksSerializer(queryset, many=True)
                return Response(serializer.data)

        return Response(user_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except NotAuthenticated as e:
        raise NotAuthenticated()
    except Exception as e:
        print(e)
        return Response({"detail": "There was an unknown error"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def manage_tasks(req: HttpRequest):
    try:
        pagination_serializer = PaginationSerializer(data=req.data)
        sort_by_serializer = SortBySerializer(data=req.data)
        if pagination_serializer.is_valid() and sort_by_serializer.is_valid():
            page = pagination_serializer.data.get('page')
            page_size = pagination_serializer.data.get('page_size')
            sort_by = sort_by_serializer.validated_data.get(
                'sort_by', 'id')
            sort_type = sort_by_serializer.validated_data.get(
                'sort_type', 'asc')
            if sort_type == 'desc':
                sort_by = f'-{sort_by}'

            start = (page - 1) * page_size
            end = start + page_size
            total_tasks = Task.objects.filter(owner_id=req.user.id).count()
            queryset = Task.objects.filter(
                owner_id=req.user.id).order_by(sort_by)[start:end]
            serializer = TaskSerializer(queryset, many=True)
            return Response({
                'total_tasks': total_tasks,
                'tasks': serializer.data
            }, status=status.HTTP_200_OK)
        errors = {**pagination_serializer.errors, **sort_by_serializer.errors}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"detail": "There was an unknown error"})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def manage_task(req: HttpRequest, id: int):
    try:
        if req.method == 'GET':
            try:
                task = Task.objects.get(id=id, owner_id=req.user.id)
                serializer = TaskSerializer(task)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response({'detail': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        elif req.method == 'PUT':
            try:
                task = Task.objects.get(id=id, owner_id=req.user.id)
                serializer = TaskSerializer(task, data=req.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response('Successfully updated task', status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Task.DoesNotExist:
                return Response({'detail': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        elif req.method == 'DELETE':
            try:
                task = Task.objects.get(id=id, owner_id=req.user.id)
                task.delete()
                return Response('Successfully deleted task', status=status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response({'detail': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"detail": "There was an unknown error"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_task(req: HttpRequest):
    try:
        data = req.data.copy()
        data['owner_id'] = req.user.id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response('Successfully created task', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"detail": "There was an unknown error"})


## Other Examples (class based views)##

class GetAllRoutesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: HttpRequest):
        try:
            routes = {reverse('show-routes'): {'GET': 'Shows all routes'},
                      reverse('login'): {'POST': 'Login'},
                      reverse('auth'): {'POST': 'Authenticate'},
                      reverse('change-password'): {'PUT': 'Change password'},
                      reverse('manage-user'): {'GET': 'Get user details', 'POST': 'Create user'},
                      reverse('manage-users'): {'POST': 'Manage users'},
                      reverse('manage-task', args=[1])+'<int:id>': {'GET': 'Get task details', 'PUT': 'Update task', 'DELETE': 'Delete task'},
                      reverse('manage-tasks'): {'POST': 'Manage tasks'},
                      reverse('create-task'): {'POST': 'Create task'},
                      # Class based views
                      reverse('class-show-routes'): {'GET': 'Shows all routes (CLASS-BASED)'},
                      reverse('class-login'): {'POST': 'Login (CLASS-BASED)'},
                      reverse('class-auth'): {'POST': 'Authenticate (CLASS-BASED)'},
                      reverse('class-change-password'): {'PUT': 'Change password (CLASS-BASED)'},
                      reverse('class-manage-user'): {'GET': 'Get user details', 'POST': 'Create user (CLASS-BASED)'},
                      reverse('class-manage-users'): {'POST': 'Manage users (CLASS-BASED)'},
                      reverse('class-manage-task', args=[1])+'<int:id>': {'GET': 'Get task details', 'PUT': 'Update task', 'DELETE': 'Delete task (CLASS-BASED)'},
                      reverse('class-manage-tasks'): {'POST': 'Manage tasks (CLASS-BASED)'},
                      reverse('class-create-task'): {'POST': 'Create task (CLASS-BASED)'},
                      reverse('class-show-users'): {'GET': 'Shows all users (generics) (CLASS-BASED)'},
                      }
            return Response(routes)
        except Exception as e:
            print(e)
            return Response({"detail": "There was an unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest):
        user = authenticate(
            username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class AuthView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request: HttpRequest):
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        return Response('success')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request: HttpRequest):
        serializer = PasswordChangeSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageUserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request: HttpRequest):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            queryset = User.objects.get(id=request.user.id)
            serializer = UserSerializer(queryset)
            return Response(serializer.data)
        except NotAuthenticated as e:
            raise NotAuthenticated()
        except Exception as e:
            print(e)
            return Response({"detail": "There was an unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: HttpRequest):
        try:
            if not ('application/x-www-form-urlencoded' in request.content_type or 'multipart/form-data' in request.content_type):
                return Response({'detail': 'Unsupported media type. Only form data is accepted.'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"detail": "There was an unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ManageUsersView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: HttpRequest):
        try:
            user_type_serializer = UserTypeSerializer(data=request.data)
            if user_type_serializer.is_valid():
                user_type = user_type_serializer.validated_data.get('type')
                if user_type == 'default':
                    if not request.user.is_authenticated:
                        raise NotAuthenticated()
                    queryset = User.objects.all()
                    serializer = UserSerializer(queryset, many=True)
                    return Response(serializer.data)
                elif user_type == 'user_tasks':
                    if not request.user.is_authenticated:
                        raise NotAuthenticated()
                    queryset = User.objects.all()
                    serializer = UserTasksSerializer(queryset, many=True)
                    return Response(serializer.data)

                return Response(user_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except NotAuthenticated as e:
            raise NotAuthenticated()
        except Exception as e:
            print(e)
            return Response({"detail": "There was an unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ManageTasksView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: HttpRequest):
        try:
            pagination_serializer = PaginationSerializer(data=request.data)
            sort_by_serializer = SortBySerializer(data=request.data)
            if pagination_serializer.is_valid() and sort_by_serializer.is_valid():
                page = pagination_serializer.validated_data.get('page')
                page_size = pagination_serializer.validated_data.get(
                    'page_size')
                sort_by = sort_by_serializer.validated_data.get(
                    'sort_by', 'id')
                sort_type = sort_by_serializer.validated_data.get(
                    'sort_type', 'asc')
                if sort_type == 'desc':
                    sort_by = f'-{sort_by}'

                start = (page - 1) * page_size
                end = start + page_size
                total_tasks = Task.objects.filter(
                    owner_id=request.user.id).count()
                queryset = Task.objects.filter(
                    owner_id=request.user.id).order_by(sort_by)[start:end]
                serializer = TaskSerializer(queryset, many=True)
                return Response({
                    'total_tasks': total_tasks,
                    'tasks': serializer.data
                }, status=status.HTTP_200_OK)
            errors = {**pagination_serializer.errors,
                      **sort_by_serializer.errors}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"detail": "There was an unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ManageTaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request: HttpRequest, id: int):
        try:
            task = Task.objects.get(id=id, owner_id=request.user.id)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'detail': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "There was an unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: HttpRequest, id: int):
        try:
            task = Task.objects.get(id=id, owner_id=request.user.id)
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response('Successfully updated task', status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({'detail': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "There was an unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: HttpRequest, id: int):
        try:
            task = Task.objects.get(id=id, owner_id=request.user.id)
            task.delete()
            return Response('Successfully deleted task', status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'detail': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "There was an unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateTaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: HttpRequest):
        try:
            data = request.data.copy()
            data['owner_id'] = request.user.id
            serializer = TaskSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response('Successfully created task', status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"detail": "There was an unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Class-based view for users with query parameter filtering (using generics)
class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get('username')
        if username:
            queryset = queryset.filter(username=username)
        return queryset
