from rest_framework import serializers

from accounts.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "timestamp",
            "amount",
            "description",
            "transaction_category",
        ]
