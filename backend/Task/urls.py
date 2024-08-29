from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from Task import views

router=routers.DefaultRouter()


urlpatterns=[

    path("api/v1/users/", include(router.urls)),
    path("docs/",include_docs_urls(title="Task API")),
    re_path('api/v1/iniciarSesion', views.iniciarSesion),
    re_path('api/v1/registro', views.registro),
    re_path('api/v1/perfil', views.perfil)
]
#genera
#GET,POST,PUT.DELETE para entidad