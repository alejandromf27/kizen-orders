from django.contrib import admin
from kizen_user.models.user import UserProfile
# from django.contrib.auth.models import User

#
# class EmailBackend(object):
#
#     @staticmethod
#     def authenticate(username=None, password=None):
#         # for Admin panel value will be come in username and for APIs value will be come in email
#         print(username, password)
#         try:
#             user = User.objects.get(email=username)
#         except User.MultipleObjectsReturned:
#             user = User.objects.filter(email=username).order_by('id').first()
#         except User.DoesNotExist:
#             return None
#         if user.check_password(password):
#             return user
#         return None
#
#     @staticmethod
#     def get_user(user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None


admin.site.register(UserProfile)
