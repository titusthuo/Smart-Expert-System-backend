from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


class UploadProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if 'profile_picture' not in request.FILES:
            return Response({"error": "No image provided"}, status=400)

        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()

        photo_url = request.build_absolute_uri(user.profile_picture.url)

        return Response({
            "success": True,
            "profile_picture_url": photo_url
        })


class GetProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if user.profile_picture:
                return Response({"profile_picture_url": request.build_absolute_uri(user.profile_picture.url)})
            return Response({"profile_picture_url": None})
        except Exception:
            return Response({"profile_picture_url": None})