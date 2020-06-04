from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Test API Endpoint
class PingPong(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(request)
        content = {'message': 'pong!'}
        return Response(content)
