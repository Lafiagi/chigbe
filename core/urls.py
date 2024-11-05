from django.urls import path
from .views import BulkUploadViewSet, DrugViewSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register(r"upload/single", DrugViewSet, basename="upload")
urlpatterns = [
    path(
        "upload/bulk/",
        BulkUploadViewSet.as_view({"post": "create"}),
        name="bulk-upload-drugs",
    ),
]
urlpatterns += router.urls
