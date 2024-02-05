from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about-us', views.about),
    path('contact-us', views.contact),
    path('search', views.search_product),
    path('category/<int:pk>', views.get_full_category),
    path('product/<int:pk>', views.get_full_product),
    path('product-not-found', views.pr_not_found),
    path('cart', views.get_user_cart),
    path('del-item/<int:pk>', views.del_from_cart),
    path('add-to-cart/<int:pk>', views.add_to_cart),
    path('register', views.Register.as_view()),
    path('accounts/logout/', views.logout_view)
  ]
