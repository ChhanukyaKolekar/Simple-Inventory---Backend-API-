from django.urls import path,include
from inventory_app import views
urlpatterns = [
    path('items/',views.create_item),
    path('items/<int:pk>',views.Ineventry_ops_APIView.as_view()),
    path('reg_user/',views.registration_view),
    path('login_user/',views.login_view)
]