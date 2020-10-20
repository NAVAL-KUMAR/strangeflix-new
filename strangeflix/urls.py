
from products.views import HomeView, VideoView,FavouriteVideo,HistoryVideo,SearchView
from django.contrib import admin
from django.urls import path
from products import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomeView.as_view()),
    path('new_video', views.new_video,name='new_video'),
    path('favourite_video', FavouriteVideo.as_view()),
    path('history_video', HistoryVideo.as_view()),
    path('video/<int:id>', VideoView.as_view()),
    path('search/', SearchView.as_view(),name='search'),
    path('add_tag',views.add_tag,name='add_tag'),
    path('ignore_goto_video',views.ignore_goto_video),
    path('ignore_v', views.ignore_v),
    path('comment',views.comment),
    path('flag',views.flag,name='flag'),
    path('notification',views.notification,name='notification'),
    path('delete_video',views.delete_video,name='delete_video'),
    path('delete_comment',views.delete_comment),
    path('edit_comment',views.edit_comment),
    path('comment_list',views.comment_list),
    path('liked', views.liked),
    path('add_comment_flag',views.add_comment_flag),
    path('delete_comm',views.delete_comm),
    path('disliked', views.disliked),
    path('save_video_time', views.save_video_time),
    path('favourite', views.favourite),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),

    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    path('logout', views.logout, name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="products/password_reset.html"),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="products/password_reset_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="products/password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="products/password_reset_done.html"),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)