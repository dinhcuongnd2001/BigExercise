from django.urls import path
from .import views

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.store, name = 'store'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('product_detail/', views.product_detail, name = 'product_detail'),
    path('submit_review/<int:product_id>', views.submit_review, name = 'submit_review'),
    path('update_item/', views.updateItem, name = 'update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('register/', views.register, name='register'),
    path('profile/',views.profile, name='profile'),
    path('profile/update', views.profile_update, name = 'profile_update'),
    path('login/',auth_views.LoginView.as_view(template_name="store/login.html"), name="login"),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)