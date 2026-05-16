from django.urls import path
from .views import RegisterView, WalletBalanceView, CreditMoneyView, DebitMoneyView, TransactionHistoryView, CreateWalletView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # register
    path('register/', RegisterView.as_view()),

    # login
    path('login/', TokenObtainPairView.as_view()),

    # refresh token
    path('refresh/', TokenRefreshView.as_view()),

    # create wallet
    path('create/',CreateWalletView.as_view()),

    # check balance
    path('<int:wallet_id>/balance/', WalletBalanceView.as_view()),

    # credit money
    path('<int:wallet_id>/credit/', CreditMoneyView.as_view()),

    # debit money
    path('<int:wallet_id>/debit/', DebitMoneyView.as_view()),

    # transaction history
    path('<int:wallet_id>/transactions/', TransactionHistoryView.as_view())

]