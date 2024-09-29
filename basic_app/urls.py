from django.urls import path, include
from basic_app import views

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('create_role/', views.OrganisationSignup.as_view()),
    path('user_login/',views.Login.as_view()),
    path('products/', include([
                              path('add_product/', views.AddProductDetails.as_view()),
                              path('view_product/<int:product_id>', views.FetchProductDetails.as_view()),
                              path('update_product/', views.UpdateProductDetails.as_view()),
                              path('delete_product/<int:product_id>', views.DeleteProductDetails.as_view()), ])),

]
