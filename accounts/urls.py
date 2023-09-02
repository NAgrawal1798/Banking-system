from django.urls import path

from accounts.views.account import AccountListView, AccountRetrieveView
from accounts.views.transaction import TransactionListView, TransactionRetrieveView

urlpatterns = [
    path("accounts/", AccountListView.as_view(), name="account-list"),
    path("accounts/<int:id>/", AccountRetrieveView.as_view(), name="account-detail"),
    path("transactions/", TransactionListView.as_view(), name="transaction-list"),
    path(
        "transactions/<int:id>/",
        TransactionRetrieveView.as_view(),
        name="transaction-detail",
    ),
]
