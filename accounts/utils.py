from django.contrib.auth.models import User
from django.utils import timezone


def get_user_and_staff_info(user_id):
    try:
        user = User.objects.get(id=user_id)
        is_staff = user.is_staff
    except User.DoesNotExist:
        user = None
        is_staff = False
    return user, is_staff


def get_pagination_urls(
    page_number,
    page_size,
    total_count,
    url,
    page_name,
    user_id,
    start_timestamp=None,
    end_timestamp=None,
    account_id=None,
    category=None,
):
    next_page_number = page_number + 1
    previous_page_number = page_number - 1 if page_number > 1 else None

    query_params = f"userId={user_id}"
    if start_timestamp:
        query_params += f"&start_timestamp={start_timestamp}"
    if end_timestamp:
        query_params += f"&end_timestamp={end_timestamp}"
    if account_id:
        query_params += f"&account_id={account_id}"
    if category:
        query_params += f"&category={category}"

    next_page_url = (
        f"{url}?{query_params}&{page_name}={next_page_number}"
        if next_page_number <= total_count // page_size + 1
        else None
    )
    previous_page_url = (
        f"{url}?{query_params}&{page_name}={previous_page_number}"
        if previous_page_number
        else None
    )
    return next_page_url, previous_page_url


def calculate_transaction_count_last_thirty_days(transactions):
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    return transactions.filter(timestamp__gte=thirty_days_ago).count()


def calculate_balance_change_last_thirty_days(transactions):
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    transactions = transactions.filter(timestamp__gte=thirty_days_ago)
    return sum(transaction.amount for transaction in transactions)
