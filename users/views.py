import datetime
import jwt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializers


class Register(APIView):
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        if user.is_admin:
            # Admin login
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow(),
                'admin': True
            }
        else:
            # Regular user login
            if not user.is_approved:
                raise AuthenticationFailed('User registration request not approved')

            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow(),
                'admin': False
            }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializers(user)

        return Response(serializer.data)


class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout successful'
        }
        return response


class AdminView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        if not payload.get('admin'):
            raise AuthenticationFailed('Unauthorized')

        # Admin-specific logic goes here
        # You can control other APIs or perform additional actions

        return Response({'message': 'Admin API'})


class ApproveUser(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        admin = User.objects.filter(id=payload['id']).first()

        if not admin.is_admin:
            raise AuthenticationFailed('Unauthorized')

        user_id = request.data.get('user_id')
        user = User.objects.filter(id=user_id).first()

        if not user:
            raise AuthenticationFailed('User not found')

        user.is_approved = True
        user.save()

        return Response({'message': 'User approved'})


class UserApprovalRequests(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        admin = User.objects.filter(id=payload['id']).first()

        if not admin.is_admin:
            raise AuthenticationFailed('Unauthorized')

        users = User.objects.filter(is_approved=False)
        serializer = UserSerializers(users, many=True)

        return Response(serializer.data)


class DeleteUser(APIView):
    def delete(self, request, user_id):
        token = request.COOKIES.get('jwt')

        if not token:
            return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(id=payload['id']).first()

        if not user:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_admin or user.id == user_id:
            user_to_delete = User.objects.filter(id=user_id).first()

            if not user_to_delete:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            user_to_delete.delete()

            return Response({'message': 'User deleted'})

        return Response({'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)


class PromoteDemoteUser(APIView):
    def post(self, request, user_id):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        admin = User.objects.filter(id=payload['id']).first()

        if not admin:
            raise AuthenticationFailed('Admin not found')

        if not admin.is_admin:
            raise AuthenticationFailed('Unauthorized')

        user = User.objects.filter(id=user_id).first()

        if not user:
            raise AuthenticationFailed('User not found')

        action = request.data.get('action')

        if action == 'promote':
            if user.is_admin:
                raise AuthenticationFailed('User is already an admin')

            user.is_admin = True
            message = 'User promoted to admin'
        elif action == 'demote':
            if not user.is_admin:
                raise AuthenticationFailed('User is not an admin')

            user.is_admin = False
            message = 'Admin demoted to user'
        else:
            raise AuthenticationFailed('Invalid action')

        user.save()

        return Response({'message': message})


class TotalUsers(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        if not payload.get('admin'):
            raise AuthenticationFailed('Unauthorized')

        users = User.objects.all()
        serializer = UserSerializers(users, many=True)

        return Response(serializer.data)
