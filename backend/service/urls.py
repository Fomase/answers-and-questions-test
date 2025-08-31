from django.contrib import admin
from django.urls import path, include

from  main.urls import router as main_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(main_router.urls))
]
