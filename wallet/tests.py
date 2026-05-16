from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Wallet, Transaction


class WalletAPITestCase(APITestCase):

    def setUp(self):

        # CREATE USER
        self.user = User.objects.create_user(
            username='ishank',
            email='ishank@gmail.com',
            password='123456'
        )

        # LOGIN USER
        response = self.client.post(
            '/wallet/login/',
            {
                'username': 'ishank',
                'password': '123456'
            }
        )

        self.token = response.data['access']

        # AUTH HEADER
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )

        # CREATE WALLET
        self.wallet = Wallet.objects.create(
            user=self.user
        )

    # REGISTER TEST
    def test_user_registration(self):

        data = {
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "123456"
        }

        response = self.client.post(
            '/wallet/register/',
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    # LOGIN TEST
    def test_user_login(self):

        data = {
            "username": "ishank",
            "password": "123456"
        }

        response = self.client.post(
            '/wallet/login/',
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn('access', response.data)

    # CREATE WALLET TEST
    def test_create_wallet(self):

        new_user = User.objects.create_user(
            username='newuser',
            password='123456'
        )

        login_response = self.client.post(
            '/wallet/login/',
            {
                'username': 'newuser',
                'password': '123456'
            }
        )

        token = login_response.data['access']

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        response = self.client.post(
            '/wallet/create/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    # CREDIT MONEY TEST
    def test_credit_money(self):

        data = {
            "amount": 1000,
            "transaction_id": "txn_101"
        }

        response = self.client.post(
            f'/wallet/{self.wallet.id}/credit/',
            data
        )

        self.wallet.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            float(self.wallet.balance),
            1000.0
        )

    # DEBIT MONEY TEST
    def test_debit_money(self):

        self.wallet.balance = 2000
        self.wallet.save()

        data = {
            "amount": 500,
            "transaction_id": "txn_102"
        }

        response = self.client.post(
            f'/wallet/{self.wallet.id}/debit/',
            data
        )

        self.wallet.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            float(self.wallet.balance),
            1500.0
        )

    # INSUFFICIENT BALANCE TEST
    def test_insufficient_balance(self):

        data = {
            "amount": 500,
            "transaction_id": "txn_103"
        }

        response = self.client.post(
            f'/wallet/{self.wallet.id}/debit/',
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    # IDEMPOTENCY TEST
    def test_duplicate_transaction(self):

        data = {
            "amount": 1000,
            "transaction_id": "txn_104"
        }

        # FIRST REQUEST
        self.client.post(
            f'/wallet/{self.wallet.id}/credit/',
            data
        )

        # SECOND SAME REQUEST
        response = self.client.post(
            f'/wallet/{self.wallet.id}/credit/',
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['message'],
            'Transaction already processed'
        )

    # BALANCE TEST
    def test_wallet_balance(self):

        self.wallet.balance = 3000
        self.wallet.save()

        response = self.client.get(
            f'/wallet/{self.wallet.id}/balance/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            float(response.data['balance']),
            3000.0
        )

    # TRANSACTION HISTORY TEST
    def test_transaction_history(self):

        Transaction.objects.create(
            wallet=self.wallet,
            transaction_id='txn_201',
            transaction_type='credit',
            amount=1000
        )

        response = self.client.get(
            f'/wallet/{self.wallet.id}/transactions/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )
        