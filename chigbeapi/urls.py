from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
# from utils.CustomeSchemagenerator import CustomSchemaGenerator
from core.urls import urlpatterns as core_patterns
from authy.urls import urlpatterns as authy_patterns

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def home(request):
    """Handle default request."""
    return Response(data="Welcome to Chigbe")




schema_view = get_schema_view(
    openapi.Info(
        title="Chigbe API",
        default_version="v1",
        description="Api That connects the Chigbe frontend",
        terms_of_service="https://localhost:8000/terms",
        contact=openapi.Contact(email="minad@Chigbe.com.ng"),
    ),
    public=True,
    permission_classes=(AllowAny,),
    # generator_class=CustomSchemaGenerator,
)


urlpatterns = [
    path("re2@pe8!/", admin.site.urls),
    path("api/v1/core/", include(core_patterns)),
    path("auth/", include(authy_patterns)),
    path("", home)
]

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^apidocs/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            "apidocs.json",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
    ]


admin.site.site_header = "Chigbe Administraton"
admin.site.index_title = "Home page"
admin.site.site_title = "Entities page"
