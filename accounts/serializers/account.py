from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    transaction_count_last_thirty_days = serializers.IntegerField(read_only=True)
    balance_change_last_thirty_days = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )

    class Meta:
        model = Account
        fields = [
            "id",
            "user",
            "name",
            "transaction_count_last_thirty_days",
            "balance_change_last_thirty_days",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data[
            "transaction_count_last_thirty_days"
        ] = instance.calculate_transaction_count_last_thirty_days()
        data[
            "balance_change_last_thirty_days"
        ] = instance.calculate_balance_change_last_thirty_days()
        return data
