import random
import string

from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd

from core.models import Drug
from core.serializers import DrugSerializer
from services.utlis import generate_unique_code


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    http_method_names = ["get", "post"]

    @transaction.atomic
    def perform_create(self, serializer):
        unique_code = generate_unique_code(random.randrange(10, 100_000_000))
        serializer.save(owner=self.request.user, unique_code=unique_code)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class BulkUploadViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    @transaction.atomic
    def create(self, request):
        file_obj = request.FILES.get("file")
        if file_obj and not file_obj.name.endswith(".csv"):
            return Response(
                {"error": "File is not CSV type"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = pd.read_csv(file_obj)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        for _, row in df.iterrows():
            unique_code = generate_unique_code(random.randrange(10, 100_000_000))
            drug_data = {
                "name": row["name"],
                "dosage": row["dosage"],
                "batch_number": row["batch_number"],
                "manufacture_date": row["manufacture_date"],
                "expiry_date": row["expiry_date"],
                "manufacturer": row["manufacturer"],
                "unique_code": unique_code,
            }
            serializer = DrugSerializer(data=drug_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(
                    {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {"message": "Drugs added successfully!"}, status=status.HTTP_201_CREATED
        )
