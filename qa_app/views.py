from django.shortcuts import render
from .forms import QAForm
from .rag_pipeline import run_rag

qa_chain = None  # global chain memory

def ask_question(request):
    global qa_chain
    answer = None   # no text initially

    if request.method == "POST":
        form = QAForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["question"]
            answer, qa_chain = run_rag(r"C:/Users/PMYLS/Desktop/chatobt/data/CHATBOT data requirements.docx", query, qa_chain)
    else:
        form = QAForm()

    return render(request, "ask.html", {"form": form, "answer": answer})

