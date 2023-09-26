from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import OrderSerializer
from utils.service import OrderService


class CreateOrder(APIView):
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data.get("email")
        robot_serial = serializer.validated_data.get("robot_serial")
        service = OrderService(email, robot_serial)
        message = service.process_order()

        return Response({"message": message}, status=status.HTTP_200_OK)
