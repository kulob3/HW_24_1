import django_filters
from users.models import Payment

class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'date': ['exact'],
            'course': ['exact'],
            'lesson': ['exact'],
            'payment_method': ['exact'],
        }