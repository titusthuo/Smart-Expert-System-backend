from graphene_file_upload.django import FileUploadGraphQLView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import jwt
from django.conf import settings
from core.models import User


@method_decorator(csrf_exempt, name='dispatch')
class CustomGraphQLView(FileUploadGraphQLView):
    def get_graphiql_template(self):
        from django.template.loader import get_template
        return get_template("graphql/modern_graphiql.html")

    def dispatch(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

            try:
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=['HS256']
                )

                username = payload.get('username')
                if username:
                    try:
                        user = User.objects.get(username=username)
                        request.user = user
                    except User.DoesNotExist:
                        try:
                            user = User.objects.get(email=username)
                            request.user = user
                        except User.DoesNotExist:
                            pass

            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                pass

        return super().dispatch(request, *args, **kwargs)