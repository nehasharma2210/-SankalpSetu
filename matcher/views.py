from django.shortcuts import render
from .matcher_utils import match_ngo, ngos
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def ngo_matcher_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query')
        if query:
            raw_results = match_ngo(query)
            # Parse results as in your existing view, or just return raw_results
            return JsonResponse({'results': raw_results}, safe=False)
        return JsonResponse({'error': 'No query provided'}, status=400)
    return JsonResponse({'error': 'POST only'}, status=405)
