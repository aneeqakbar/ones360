from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()

class MobileLoginBackend(ModelBackend):
    def authenticate(self, request, mobile_number=None, password=None, **kwargs):
        # Check the mobile_number/password and return a user.
        if mobile_number is None:
            mobile_number = kwargs.get("mobile_nubmer")
        if mobile_number is None or password is None:
            return
        try:
            user = UserModel.objects.get(mobile_number=mobile_number)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
