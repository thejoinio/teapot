# helper/urls.py
from django.urls import path
from .views import SubmitEmailView, VerifyTelegramView, VerifyDiscordView, VerifyJoindaAccountView

urlpatterns = [
    path('submit-email/', SubmitEmailView.as_view(), name='submit_email'),
    path('verify-telegram/', VerifyTelegramView.as_view(), name='verify_telegram'),
    path('verify-discord/', VerifyDiscordView.as_view(), name='verify_discord'),
    path('verify-signup', VerifyJoindaAccountView.as_view(), name='verify_joinda_signup')
]
