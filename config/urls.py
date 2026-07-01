from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/books/', include('apps.books.urls')),
    path('api/auth/', include('apps.users.urls')),
    path('api/shelves/', include('apps.shelves.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
]
