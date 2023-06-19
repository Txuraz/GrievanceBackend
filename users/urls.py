from django.contrib import admin
from django.urls import path
from .views import Register, Login, UserView, Logout, AdminView, ApproveUser, UserApprovalRequests, DeleteUser, \
    PromoteDemoteUser, TotalUsers, ForgotPassword, ResetPassword

urlpatterns = [
    path('register', Register.as_view()),
    path('login', Login.as_view()),
    path('user', UserView.as_view()),
    path('logout', Logout.as_view()),
    path('admin/', AdminView.as_view(), name='admin'),
    path('approval-requests/', UserApprovalRequests.as_view(), name='approval-requests'),
    path('approve-user/', ApproveUser.as_view(), name='approve-user'),
    path('user/delete/<int:user_id>/', DeleteUser.as_view(), name='delete-user'),
    path('user/<int:user_id>/promote-demote/', PromoteDemoteUser.as_view(), name='promote-demote-user'),
    path('total-user/', TotalUsers.as_view(), name='approved_users_and_admins'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot_password'),
    path('reset-password/', ResetPassword.as_view(), name='reset_password'),
]