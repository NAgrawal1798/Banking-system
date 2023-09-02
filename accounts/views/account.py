from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountSerializer
from accounts.utils import get_pagination_urls, get_user_and_staff_info


class AccountListView(APIView):
    def get(self, request):
        user_id = request.GET.get("userId")
        cursor = request.GET.get("cursor")
        page_number = int(request.GET.get("page", 1))
        page_size = 10

        user, is_staff = get_user_and_staff_info(user_id)

        if is_staff:
            # For admin user
            accounts = Account.objects.all()
        else:
            # For normal user
            accounts = Account.objects.filter(user=user_id)

        if cursor:
            accounts = accounts.filter(id__gt=cursor)

        total_count = accounts.count()
        offset = (page_number - 1) * page_size
        page_accounts = accounts[offset : offset + page_size]

        serializer = AccountSerializer(page_accounts, many=True)

        next_page_url, previous_page_url = get_pagination_urls(
            page_number, page_size, total_count, "/accounts/", "page"
        )

        return Response(
            {
                "results": serializer.data,
                "next": next_page_url,
                "previous": previous_page_url,
                "count": total_count,
            },
            status=status.HTTP_200_OK,
        )


class AccountRetrieveView(APIView):
    def get(self, request, id):
        user_id = request.GET.get("userId")
        user, is_staff = get_user_and_staff_info(user_id)

        try:
            if is_staff:
                account = Account.objects.get(id=id)
            else:
                account = Account.objects.get(id=id, user=user_id)
        except Account.DoesNotExist:
            return Response(status=404)

        serializer = AccountSerializer(account)
        return Response(serializer.data)
