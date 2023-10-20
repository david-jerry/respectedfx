from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from respectedfx.newsletter.models import Newsletter

@csrf_exempt
def apply_news_letter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        # Perform necessary validations here
        # ...

        # Save the FXRequest object
        Newsletter.objects.create(
            email=email,
        )

        return JsonResponse({'message': f'Subscribed to mail list successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)

