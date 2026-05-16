from .models import Wallet, Transaction
from .serializers import RegisterSerializer, CreditDebitSerializer, TransactionSerializer, WalletSerializer
from django.db import transaction
from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    """ Register API """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class CreateWalletView(APIView):
    """ create wallet for user """
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # check if wallet already exists
        if Wallet.objects.filter(user=request.user).exists():
            return Response(
                {"error": "Wallet already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # create wallet
        wallet = Wallet.objects.create(user=request.user)
        serializer = WalletSerializer(wallet)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    

class WalletBalanceView(APIView):
    """ Wallet Balance API """
    permission_classes = [IsAuthenticated]

    def get(self, request, wallet_id):
        try:
            wallet = Wallet.objects.get(id=wallet_id)

            data = {
                "wallet_id": wallet.id,
                "balance": wallet.balance
            }
            return Response(data)
        
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet doesn't exist."},
                status=status.HTTP_404_NOT_FOUND
            )


class CreditMoneyView(APIView):
    """ Credit Money API """
    permission_classes = [IsAuthenticated]

    def post(self, request, wallet_id):
        serializer = CreditDebitSerializer(data=request.data)
        
        if serializer.is_valid():
            amount = serializer.validated_data['amount']    
            transaction_id = serializer.validated_data['transaction_id']

            # idempotency check
            if Transaction.objects.filter(transaction_id=transaction_id).exists():
                return Response(
                    {
                        "message": "Transaction already processed"
                    },
                    status=status.HTTP_200_OK
                )        
            
            try:
                with transaction.atomic():
                    wallet = Wallet.objects.select_for_update().get(id=wallet_id)               
                    
                    wallet.balance += amount
                    wallet.save()

                    Transaction.objects.create(
                        wallet=wallet,
                        transaction_id=transaction_id,
                        transaction_type='credit',
                        amount=amount
                    )
                    return Response(
                        {"message": "Money credited successfully.",
                        "balance": wallet.balance}
                    )
            
            except Wallet.DoesNotExist:
                return Response(
                    {"error": "Wallet doesn't exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class DebitMoneyView(APIView):
    """ Debit Money API """
    permission_classes = [IsAuthenticated]

    def post(self, request, wallet_id):
        serializer = CreditDebitSerializer(data=request.data)
        
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            transaction_id = serializer.validated_data['transaction_id']

            # idempotency check
            if Transaction.objects.filter(transaction_id=transaction_id).exists():
                return Response(
                    {
                        "message": "Transaction already processed"
                    },
                    status=status.HTTP_200_OK
                )  
            
            try:
                with transaction.atomic():
                    wallet = Wallet.objects.select_for_update().get(id=wallet_id)

                    if wallet.balance < amount:
                        return Response(
                            {"error": "Insufficient balance."},
                            status=status.HTTP_400_BAD_REQUEST                            
                        )
                    
                    wallet.balance -= amount
                    wallet.save()

                    Transaction.objects.create(
                        wallet=wallet,
                        transaction_id=transaction_id,
                        transaction_type='debit',
                        amount=amount
                    )
                    return Response(
                        {"message": "Money debited successfully.",
                        "balance": wallet.balance}
                    )
            
            except Wallet.DoesNotExist:
                return Response(
                    {"error": "Wallet doesn't exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )    


class TransactionHistoryView(APIView):
    """ Transaction History API """

    permission_classes = [IsAuthenticated]

    def get(self, request, wallet_id):
        try:
            wallet = Wallet.objects.get(id=wallet_id)
            transactions = wallet.transactions.all().order_by('-created_at')

            # date filter
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            if start_date and end_date:
                transactions = transactions.filter(created_at__date__range=[start_date, end_date])

            # pagination
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 5))

            start = (page - 1) * limit
            end = start + limit

            serializer = TransactionSerializer(transactions[start:end], many=True)
            return Response(serializer.data)
        
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet not found."},
                status=status.HTTP_404_NOT_FOUND
            )
