"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from ec import views
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', TemplateView.as_view(template_name='hello.html')),
    path('list/', views.ProductListView.as_view(), name='list'), # 商品一覧ページ
    path('detail/<int:pk>/', views.ProductDetailView.as_view(), name='detail'), # 詳細ページ
    path('cart/add/detail/', views.DetailAddCartView.as_view(),), # カート追加
    path('cart/', views.CartListView.as_view()), # カートページ
    path('cart/add/list/', views.ListAddCartView.as_view()), # カート追加
    path('cart/remove/<str:pk>/', views.remove_from_cart), # カート削除
    path('', views.ProductListView.as_view()),# herokuにデプロイする際のpath
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
