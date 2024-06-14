from django.shortcuts import render
from django.http import JsonResponse
from .forms import TextForm
from .utils import summarize_text_using_local_model, summarize_text_using_gemini_ai

def home(request):
    return render(request, 'summariser/summarise.html')

def summarize(request):
    if request.method == 'POST':
        form = request.POST
        print(f'Received Form: {form}')
        text_to_summarize = form.get('text')
        min_length = int(form.get('minLength'))
        max_length = int(form.get('maxLength'))
        use_local_model = bool(form.get('useLocalModel'))
        if use_local_model:
            print('Using local model...')
            summary = summarize_text_using_local_model(text_to_summarize, max_length, min_length)
        else:
            print('Using Gemini AI...')
            summary = summarize_text_using_local_model(text_to_summarize, max_length, min_length)
            # summary = summarize_text_using_gemini_ai(text_to_summarize, max_length, min_length) # To reduce token usage
        return JsonResponse({'summary': summary})
    return JsonResponse({'error': 'Invalid form'}, status=400)
