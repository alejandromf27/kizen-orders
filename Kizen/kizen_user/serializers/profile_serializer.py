from rest_framework import serializers
from kizen_user.models.user import UserProfile
from kizen_user.serializers.user_serializer import UserSimpleSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    """ serialize to json UserProfile object"""

    user = UserSimpleSerializer(required=True)
    birth_date = serializers.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = UserProfile
        fields = ('user', 'birth_date')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of profile
        :return: returns a successfully created profile record
        """
        user_data = validated_data.pop('user')
        user = UserSimpleSerializer.create(UserSimpleSerializer(), validated_data=user_data)
        profile, created = UserProfile.objects.update_or_create(
            user=user,
            birth_date=validated_data.pop('birth_date')
        )
        return profile

