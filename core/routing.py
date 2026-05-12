from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"graphql/", consumers.GraphQLWSConsumer.as_asgi()),
]