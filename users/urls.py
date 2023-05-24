from django.contrib import admin
from django.urls import path
from .views import Register, Login, UserView, Logout, AdminView, ApproveUser, UserApprovalRequests

urlpatterns = [
    path('register', Register.as_view()),
    path('login', Login.as_view()),
    path('user', UserView.as_view()),
    path('logout', Logout.as_view()),
    path('admin/', AdminView.as_view(), name='admin'),
    path('approval-requests/', UserApprovalRequests.as_view(), name='approval-requests'),
    path('approve-user/', ApproveUser.as_view(), name='approve-user'),
]