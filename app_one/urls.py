from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index),
	path('register',views.create_user),
	path('user_login', views.user_login),
	path('user_success', views.user_welcome),
	path('create_message', views.create_content),
	path('user/<int:user_id>',views.user_profile),
	path('create_comment/<int:message_id>', views.create_comment),
	path('delete_message/<int:message_id>',views.delete_message),
	path('logout', views.user_logout),
]