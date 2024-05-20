from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Wallet, Transaction
from serializers.serializers import WalletSerializer, TransactionSerializer
from prometheus_client import Counter
from queries import create_new_wallet, get_wallet_balance_by_key, transfer_wallet
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from .authoriztion_middleware import authorization
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
import uuid


api_request_counter = Counter('api_requests_total', 'Total number of API requests')



@api_view(['POST'])
@method_decorator(authorization, name='dispatch')
def create_wallet_view(request):
    wallet_key = str(uuid.uuid4())
    new_wallet = Wallet.objects.create(key=wallet_key)
    wallet_serializer = WalletSerializer(new_wallet)
    create_new_wallet(id=wallet_key)
    return create_new_wallet(id=wallet_key), Response(wallet_serializer.data)


@permission_classes([IsAuthenticated])
class ViewWalletView(APIView):
    def get(self, request, key_wallet):
        balance = get_wallet_balance_by_key(key_wallet)

        if balance is not None:
            cost = request.query_params.get('cost', 0)

            transaction_data = {
                'cost': cost,
                'from_wallet': None,
                'to_wallet': key_wallet
            }

            transaction_serializer = TransactionSerializer(data=transaction_data)
            if transaction_serializer.is_valid():
                return Response({'status': 'успешно', 'balance': balance}, status=status.HTTP_OK)
            else:
                return Response({'status': 'неуспешно', 'message': 'Параметры некорректны'}, status=status.HTTP_BAD_REQUEST)
        else:
            return Response({'status': 'неуспешно', 'message': 'Кошелек не найден'}, status=status.HTTP_NOT_FOUND)



@permission_classes([IsAuthenticated])
class TransferWalletView(APIView):
    def post(self, request):
        sender_key = request.data.get('sender_key')
        recipient_key = request.data.get('recipient_key')
        amount = request.data.get('amount')

        try:
            sender_wallet = Wallet.objects.get(key=sender_key)
            recipient_wallet = Wallet.objects.get(key=recipient_key)
        except Wallet.DoesNotExist:
            return Response({'status': 'неуспешно', 'message': 'Отправитель или получатель не найден'},
                            status=status.HTTP_NOT_FOUND)

        transaction_data = {
            'cost': amount,
            'from_wallet': sender_wallet,
            'to_wallet': recipient_wallet
        }

        transaction_serializer = TransactionSerializer(data=transaction_data)
        if transaction_serializer.is_valid():
            transaction_serializer.save()

            # Вызов функции transfer_wallet для перевода средств
            transfer_wallet(sender_key, recipient_key, amount)

            return Response({'status': 'успешно'}, status=status.HTTP_OK)
        else:
            return Response({'status': 'неуспешно', 'message': 'Параметры некорректны'}, status=status.HTTP_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class DepositWalletView(APIView):
    def post(self, request, key_wallet):
        current_wallet = Wallet.objects.get(key=key_wallet)  # Получаем текущий кошелек

        amount = request.data.get('amount')  # Получаем сумму пополнения

        transaction_data = {
            'cost': amount,
            'from_wallet': current_wallet,
            'to_wallet': current_wallet  # Пополнение кошелька, поэтому отправителя нет
        }

        transaction_serializer = TransactionSerializer(data=transaction_data)
        if transaction_serializer.is_valid():
            transaction_serializer.save()
            return Response({'status': 'успешно'}, status=status.HTTP_OK)
        else:
            return Response({'status': 'неуспешно', 'message': 'Параметры некорректны'}, status=status.HTTP_BAD_REQUEST)

