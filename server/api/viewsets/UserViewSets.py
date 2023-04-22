from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User

from ..serializers.UserSerializer import UserSerializer


# Get self user data, available for authenticated User
@api_view(["GET"])
def UserProfileView(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "You must be logged in to view this page."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# Returns True if username exists, else False
@api_view(["GET"])
def user_exists(request):
    username = request.query_params.get("username")
    if username:
        user = User.objects.filter(username=username)
        if user:
            return Response(True, status=status.HTTP_200_OK)
        else:
            return Response(False, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Returns True if email exists, else False
@api_view(["GET"])
def email_exists(request):
    email = request.query_params.get("email")
    if email:
        user = User.objects.filter(email=email)
        if user:
            return Response(True, status=status.HTTP_200_OK)
        else:
            return Response(False, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
