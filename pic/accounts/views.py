from rest_framework import views
from rest_framework.response import Response


class ExampleView(views.APIView):
    def get(self, request):
        return Response({"message_from_view": "Hello, World!"})
