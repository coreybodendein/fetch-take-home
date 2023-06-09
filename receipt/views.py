from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Receipt
from .serializers import ReceiptSerializer, ReceiptModelCreateSerialzier, ReceiptModelRetrieveSerialzier


class ReceiptProcessorGetView(APIView):
    """Gets a stored Receipt and returns the calculated number of points"""
    def get(self, request, _id):
        try:
            receipt = Receipt.objects.get(id=_id)
            return Response(ReceiptModelRetrieveSerialzier(instance=receipt).data)
        except Receipt.DoesNotExist:
            return Response('No receipt found for that id', status=404)


class ReceiptProcessorPostView(APIView):
    """Creates and validates a given Receipt and returns the generated UUID"""
    def post(self, request):
        serializer = ReceiptSerializer(data=request.data)
        if serializer.is_valid():
            receipt = serializer.save()
            return Response(ReceiptModelCreateSerialzier(receipt).data)
        else:
            return Response('The receipt is invalid', status=400)
