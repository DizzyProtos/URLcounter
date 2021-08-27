from django.urls import path
from urlcounter.views import add_url, update_url, get_result


urlpatterns = [
    path('add', add_url, name='add'),
    path('update/<int:url_id>', update_url, name='update'),
    path('get/<int:url_id>', get_result, name='get'),
]
