
from users.models import Payment
from rest_framework.serializers import ModelSerializer
from users.models import User

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"