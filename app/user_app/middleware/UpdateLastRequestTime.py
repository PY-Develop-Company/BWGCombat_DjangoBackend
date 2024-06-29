from django.utils.timezone import now
from user_app.models import UserData  # Ensure you import the model
from rest_framework_simplejwt.authentication import JWTAuthentication


class UpdateLastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_authenticator = JWTAuthentication()
        try:
            user, _ = jwt_authenticator.authenticate(request)

            if user and user.is_authenticated:
                user_activity = UserData.objects.get(user_id=user.tg_id)
                last_activity = user_activity.last_visited

                delta = last_activity.day - now().day
                if delta >= 1:
                    user_activity.gold_balance += delta * user_activity.passive_income

                user_activity.last_visited = now()
                user_activity.save()

        except:
            pass  # Do nothing if the token is invalid
        response = self.get_response(request)
        return response
