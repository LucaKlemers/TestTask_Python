from django.shortcuts import render
from django.http import HttpResponse
from .models import Quote, AddQuoteForm, AddSourceForm


def index(request):  # Main page
    return render(request, "QuoteWebsite/index.html")


def add_quote(request):  # Page to add new quotes
    if request.method == "POST":
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            form = AddQuoteForm()
            return render(request, "QuoteWebsite/add_quote.html", {
                "form": form,
                "success": "Цитата добавлена!"  # Optional
            })
    else:
        form = AddQuoteForm()
    return render(request, "QuoteWebsite/add_quote.html", {"form": form})


def vote(request, quote_id):  # Like/dislike buttons
    return HttpResponse(
        "Upvote or downvote buttons for the quote indexed %s will be here" % quote_id
    )


def statistics(request):  # Statistics page (top quotes, etc.)
    best_quotes = Quote.objects.order_by("total_rating")[:10]
    output = "/n".join([q.quote_text for q in best_quotes])
    return HttpResponse(output)


def source_info(request, source_id):  # Source pages
    return HttpResponse("The source info will be here")


def add_source(request):  # Page to add new sources
    if request.method == "POST":
        form = AddSourceForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            form = AddSourceForm()
            return render(request, "QuoteWebsite/add_source.html", {
                "form": form,
                "success": "Источник добавлен!"  # Optional
            })
    else:
        form = AddSourceForm()
    return render(request, "QuoteWebsite/add_source.html", {"form": form})
