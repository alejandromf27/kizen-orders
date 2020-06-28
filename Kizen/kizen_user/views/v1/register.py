from rest_framework.response import Response
from rest_framework.views import APIView
from kizen_user.serializers.profile_serializer import UserProfileSerializer
from rest_framework import status
from Kizen.response_data import json_data


class RegisterAPIView(APIView):
    """
    class to register the user
    """

    @staticmethod
    def post(request):
        """
        Create user
        :param request: http petition
        :return: user serialized data
        """
        try:
            serializer = UserProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(json_data(
                    data=serializer.data
                ), status=status.HTTP_201_CREATED)
            return Response(json_data(
                message=serializer.errors,
                status='danger'
            ), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(json_data(
                message=str(e),
                status='danger'
            ), status=status.HTTP_400_BAD_REQUEST)
