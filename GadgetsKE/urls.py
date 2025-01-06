from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    path("", views.home),
    path("about/", views.about,name="about"),
    path("contact/", views.contact, name="contact"),
    path("category/<slug:val>", views.CategoryView.as_view(), name='category'),
    path("product-detail/<int:pk>", views.productDetail.as_view(),name="category-title"),
    path("product-details/<int:pk>", views.productDetail.as_view(), name="product-detail"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name="address"),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(),name='updateAddress'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.show_cart, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    #auth
    path("registration/", views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('account/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('passwordChange/', auth_view.PasswordResetView.as_view(template_name='app/changePassword.html', form_class=MyPasswordChangeForm, success_url='/passwordChangedone'), name='passwordChange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordChangedone.html')),
    path("logout/",auth_view.LogoutView.as_view(next_page='login'), 
    name='logout'),

    #password reset
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 