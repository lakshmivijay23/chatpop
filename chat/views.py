from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

# from openai import OpenAI

# client = OpenAI(api_key=settings.OPENAI_API_KEY)

def chat_view(request):
    if request.method == "POST":
        print(request)
        llm_response = "hello im a response"
        return JsonResponse({"message": llm_response})
    return render(request, "chat/chat.html")
