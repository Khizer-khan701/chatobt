from django.shortcuts import render
from .rag_pipeline import run_rag

def ask_question(request):
    answer = None
    if request.method == "POST":
        query = request.POST.get("question")
        filepath = r"C:/Users/PMYLS/Desktop/chatobt/data/CHATBOT data requirements.docx"  # absolute or relative path
        answer = run_rag(filepath, query)
    return render(request, "ask.html", {"answer": answer})
