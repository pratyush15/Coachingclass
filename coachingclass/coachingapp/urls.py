from django.urls import path      
from . import views   
from django.conf import settings 
from django.conf.urls.static import static    
from django.contrib.auth import views as auth_view 
from .forms import LoginForm
urlpatterns = [ 
    path("home/",views.home,name="home"), 
    path("",views.home,name="home"), 
    path("contact/",views.contact,name="contact"), 
    path("services/",views.services,name="services"), 
    path("about/",views.about,name="about"), 
    path('gallery/',views.gallery,name="gallery"),    
    path('category/<int:cid>/',views.show_category_page),  
    #path("profile/",views.ProfileView.as_view(),name="profile"), 
    path("profile/",views.ProfileView.as_view(),name="profile"), 
    path("data/",views.data,name="data"), 
    path("updateData/<int:pk>",views.updateData.as_view(),name="updateData"),
    #Authentication-Section  
    path("customerregistration/",views.CustomerRegistrationView.as_view(),name="customerregistration"),       
    path("accounts/login/", auth_view.LoginView.as_view(template_name='login.html',       
    authentication_form=LoginForm), name='login'),   
    path("logout/",auth_view.LogoutView.as_view(next_page='login'),name='logout'),  
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
  