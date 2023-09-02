from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account, Transaction
from accounts.serializers.transaction import TransactionSerializer
from accounts.utils import get_pagination_urls, get_user_and_staff_info


class TransactionListView(APIView):
    def get_queryset(self):
        user_id = self.request.GET.get("userId")
        user, is_staff = get_user_and_staff_info(user_id)

        if is_staff:
            # For admin user
            transactions = Transaction.objects.all()
        else:
            # For normal user
            user_accounts = Account.objects.filter(user=user_id)
            transactions = Transaction.objects.filter(account__in=user_accounts)

        return transactions

    def get(self, request):
        page_number = int(request.GET.get("page", 1))
        page_size = 10
        start_timestamp = request.GET.get("start_timestamp")
        end_timestamp = request.GET.get("end_timestamp")
        account_id = request.GET.get("account_id")
        category = request.GET.get("category")
        user_id = self.request.GET.get("userId")

        transactions = self.get_queryset()

        if start_timestamp:
            transactions = transactions.filter(timestamp__gte=start_timestamp)

        if end_timestamp:
            transactions = transactions.filter(timestamp__lte=end_timestamp)

        if account_id:
            transactions = transactions.filter(account_id=account_id)

        if category:
            transactions = transactions.filter(transaction_category=category)

        total_count = transactions.count()
        transactions = transactions.order_by("-timestamp")
        offset = (page_number - 1) * page_size
        page_transactions = transactions[offset : offset + page_size]

        serializer = TransactionSerializer(page_transactions, many=True)

        next_page_url, previous_page_url = get_pagination_urls(
            page_number,
            page_size,
            total_count,
            "/transactions/",
            "page",
            user_id,
            start_timestamp,
            end_timestamp,
            account_id,
            category,
        )

        return Response(
            {
                "count": total_count,
                "next": next_page_url,
                "previous": previous_page_url,
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class TransactionRetrieveView(APIView):
    def get_queryset(self):
        user_id = self.request.GET.get("userId")
        transaction_id = self.kwargs.get("id")
        user, is_staff = get_user_and_staff_info(user_id)

        try:
            if is_staff:
                # For admin user
                transaction = Transaction.objects.all(id=transaction_id)
            else:
                # For normal user
                transaction = Transaction.objects.filter(
                    id=transaction_id, user=user_id
                )
        except Transaction.DoesNotExist:
            transaction = None

        return transaction

    def get(self):
        transaction = self.get_queryset()

        if transaction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
