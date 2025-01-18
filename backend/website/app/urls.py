from django.urls import path, include
from .views import get_all_routes, manage_user, manage_users, manage_task, manage_tasks, login, auth, contact, change_password, create_task
from .views import GetAllRoutesView, LoginView, AuthView, ChangePasswordView, ManageUserView, ManageUsersView, ManageTasksView, ManageTaskView, CreateTaskView, UserView

urlpatterns = [
    path('routes/', get_all_routes, name='show-routes'),
    path('login/', login, name='login'),
    path('auth/', auth, name='auth'),
    path('contact/', contact, name='contact'),
    path('change-password/', change_password, name='change-password'),
    path('user/', manage_user, name='manage-user'),
    path('users/', manage_users, name='manage-users'),
    path('task/<int:id>', manage_task, name='manage-task'),
    path('tasks/', manage_tasks, name='manage-tasks'),
    path('task/', create_task, name='create-task'),

    # Other Examples (class based views)
    path('class/routes/', GetAllRoutesView.as_view(), name='class-show-routes'),
    path('class/login/', LoginView.as_view(), name='class-login'),
    path('class/auth/', AuthView.as_view(), name='class-auth'),
    path('class/change-password/', ChangePasswordView.as_view(),
         name='class-change-password'),
    path('class/user/', ManageUserView.as_view(), name='class-manage-user'),
    path('class/users/', ManageUsersView.as_view(), name='class-manage-users'),
    path('class/task/<int:id>', ManageTaskView.as_view(), name='class-manage-task'),
    path('class/tasks/', ManageTasksView.as_view(), name='class-manage-tasks'),
    path('class/task/', CreateTaskView.as_view(), name='class-create-task'),

    # Generics (no auth needed)
    path('class/generics/users/', UserView.as_view(), name='class-show-users'),
]

urlpatterns += [
    path('auth_rest/', include('rest_framework.urls')),
]
