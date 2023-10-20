from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from respectedfx.fxrates.models import FXRequest, TransferToBanks, FXTransferRequest

@csrf_exempt
def create_internationa_transfer_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        bank_id = int(data.get('bank'))
        amount = Decimal(data.get('amount'))
        currency = data.get('currency')
        recipient_account_number = data.get('account_number')
        recipient_account_name = data.get('account_name')
        recipient_bank_code = data.get('bank_code')

        # Perform necessary validations here
        # ...

        # Save the FXRequest object
        fx_request = FXTransferRequest.objects.create(
            email=email,
            bank=TransferToBanks.objects.get(id=bank_id),
            amount=amount,
            currency=currency,
            recipient_account_number=recipient_account_number,
            recipient_account_name=recipient_account_name,
            recipient_bank_code=recipient_bank_code,
        )

        # Perform any additional tasks here
        # ...
        bank = TransferToBanks.objects.get(id=bank_id)



        return JsonResponse({'message': f'Foreign Transfer Request created successfully. <br>Make your deposit into this account to complete this request.<br><br><br>Bank Name: {bank.bank_name.upper()}<br>Account Name: {bank.account_name}<br>Account Number: {bank.account_number}'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def create_fx_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        bank_id = int(data.get('bank'))
        amount = Decimal(data.get('amount'))
        currency = data.get('currency')
        account_number = data.get('account_number')
        account_name = data.get('account_name')

        # Perform necessary validations here
        # ...

        # Save the FXRequest object
        fx_request = FXRequest.objects.create(
            email=email,
            bank=TransferToBanks.objects.get(id=bank_id),
            amount=amount,
            currency=currency,
            account_number=account_number,
            account_name=account_name
        )

        # Perform any additional tasks here
        # ...
        bank = TransferToBanks.objects.get(id=bank_id)



        return JsonResponse({'message': f'FXChange Request created successfully. <br><br>Make your deposit into this account to complete this request.<br><br><br>Bank Name: {bank.bank_name.upper()}<br>Account Name: {bank.account_name}<br>Account Number: {bank.account_number}'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def create_fx_local_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        bank_id = int(data.get('bank'))
        amount = Decimal(data.get('amount'))
        currency = data.get('currency')
        to_currency = data.get('to_currency')
        account_number = data.get('account_number')
        account_name = data.get('account_name')

        # Perform necessary validations here
        # ...

        # Save the FXRequest object
        fx_request = FXRequest.objects.create(
            email=email,
            bank=TransferToBanks.objects.get(id=bank_id),
            amount=amount,
            currency=currency,
            to_currency=to_currency,
            account_number=account_number,
            account_name=account_name
        )

        # Perform any additional tasks here
        # ...
        bank = TransferToBanks.objects.get(id=bank_id)



        return JsonResponse({'message': f'FXChange Request created successfully. <br><br>Make your deposit into this account to complete this request.<br><br><br>Bank Name: {bank.bank_name.upper()}<br>Account Name: {bank.account_name}<br>Account Number: {bank.account_number}'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Create your views here.
