from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, logout
from kizen_user.serializers.user_serializer import LoginUserSerializer
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from oauth2_provider.models import AccessToken
from Kizen.response_data import json_data


class LoginAPIView(APIView):
    """
    class to login the user
    """

    @staticmethod
    def post(request):
        """
        Method to login users
        :param request: petition
        :return: data of the user access in the http response
        """
        data = request.data
        username = data.get("username", False)
        password = data.get('password', False)
        # check the authentication by username and password
        user = authenticate(username=username, password=password)
        if user:  # return the user access data
            data = LoginUserSerializer(user).data
            return Response(json_data(
                data=data
            ), status=status.HTTP_200_OK)
        else:  # return a validation message
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    """
    logout the users
    """
    permission_classes = [TokenHasReadWriteScope]

    @staticmethod
    def post(request):
        """
        Method to logout users
        :param request: http petition
        :return: empty http response
        """
        try:
            bearer = request.META.get('HTTP_AUTHORIZATION', False)
            if bearer:
                token = bearer.split(' ')[1]
                AccessToken.objects.filter(token=token).delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        logout(request)
        return Response({}, status=status.HTTP_200_OK)
