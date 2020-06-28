from rest_framework import serializers
from django.contrib.auth.models import User
from oauth2_provider.models import Application
from oauthlib.common import generate_token
from django.conf import settings
from datetime import timedelta
from django.utils.timezone import now
from oauth2_provider.models import AccessToken, RefreshToken


class TokeSerializer(serializers.ModelSerializer):
    """ serialize to json an AccessToken object"""

    expires_in = serializers.IntegerField(default=settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'])
    refresh_token = serializers.SerializerMethodField()

    class Meta:
        model = AccessToken
        fields = ('token', 'expires_in', 'refresh_token', 'scope')

    @staticmethod
    def get_refresh_token(obj):
        """
        Get the refresh token
        :param obj: Token obj
        :return: the token for refresh the session when expired
        """
        return obj.refresh_token.token


def get_access_token(user):
    """
    Function to generate a user access token
    :param user: user instance
    :return: the serialized token generated
    """
    # create the application for the user access
    app, created = Application.objects.get_or_create(user=user)
    # generate the token
    token = generate_token()
    # generate the refresh token
    refresh_token = generate_token()
    # calculate the token expiration time
    expires = now() + timedelta(seconds=settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'])
    # define scopes
    scope = "read write"
    # create and save the token
    access_token = AccessToken.objects.create(
        user=user,
        application=app,
        expires=expires,
        token=token,
        scope=scope
    )
    # create and save the refresh token
    RefreshToken.objects.create(
        user=user,
        application=app,
        token=refresh_token,
        access_token=access_token
    )
    return TokeSerializer(instance=access_token).data


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'].split('@')[0],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginUserSerializer(serializers.ModelSerializer):
    """
    Serialized to json of the user access data
    """
    info = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()
    application = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('info', 'token', 'application')

    @staticmethod
    def get_token(obj):
        """
        Method to generate the token
        :param obj: User obj
        :return: the generated token
        """
        return get_access_token(obj)

    @staticmethod
    def get_info(obj):
        """
        Get the user info
        :param obj: User obj
        :return: serialized user data
        """
        return UserSimpleSerializer(instance=obj).data

    @staticmethod
    def get_application(obj):
        """
        Get the data of user application
        :param obj: User obj
        :return: a json with client_id and secret client id
        """
        application = Application.objects.get(user=obj)
        return {
            'client_id': application.client_id,
            'client_secret': application.client_secret
        }
