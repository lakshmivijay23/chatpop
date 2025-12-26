from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import os
import bleach
import markdown
from langchain_google_genai import ChatGoogleGenerativeAI

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

ALLOWED_TAGS = ['b', 'strong', 'i', 'em', 'a', 'ul', 'ol', 'li', 'p', 'br']
ALLOWED_ATTRS = {'a': ['href', 'target']}

llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        top_p=0.95,
    )
def chat_view(request):
    
    if request.method == "POST":
        user_message = request.POST.get("message")
        messages = [
            (
                "system",
                "You are a helpful assistant that guides humans with the queries!",
            ),
            ("human", str(user_message)),
        ]
        llm_response = llm.invoke(messages)
        llm_response = markdown.markdown(llm_response.text, extensions=['extra'])
        safe_response = bleach.clean(
            llm_response,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRS,
            strip=True
        )
        safe_response = safe_response.replace('<a ', '<a target="_blank" rel="noopener noreferrer" ')

        # llm_response = "hello im a response"
        return JsonResponse({"message": safe_response})
    return render(request, "chat/chat.html")
