from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Quote, QuoteSource, AddQuoteForm, AddSourceForm, PageViews
from random import choices


def index(request):  # Main page
    def random_quote(
        influence=0.25,
    ):  # Get a random quote, with influence the weight has being 0.25 by default
        all_quotes = Quote.objects.all()
        all_weights = [quote.quote_weight for quote in all_quotes]
        n = len(all_quotes)
        total_weight = sum(all_weights)
        influenced_weights = []
        for weight in all_weights:
            influenced_weights.append(
                (influence * (weight / total_weight)) + ((1 - influence) * (1 / n))
            )
        selected_quote = choices(all_quotes, weights=influenced_weights, k=1)
        return selected_quote[0]
    # Claculate views
    page_views, created = PageViews.objects.get_or_create(name="views")
    page_views.views += 1
    page_views.save()
    context = {"selected_quote": random_quote(0.25), "views": page_views.views}
    return render(request, "QuoteWebsite/index.html", context)


def add_quote(request):  # Page to add new quotes
    if request.method == "POST":
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            form = AddQuoteForm()
            return render(
                request,
                "QuoteWebsite/add_quote.html",
                {"form": form, "success": "Цитата добавлена!"},  # Optional
            )
    else:
        form = AddQuoteForm()
    return render(request, "QuoteWebsite/add_quote.html", {"form": form})


def vote(request, quote_id):  # Like/dislike buttons
    return HttpResponse(
        "Upvote or downvote buttons for the quote indexed %s will be here" % quote_id
    )


def statistics(request):  # Statistics page (top quotes, etc.)
    top_quotes = Quote.objects.order_by("total_rating")[:10]
    context = {"top_quotes": top_quotes,}
    return render(request, "QuoteWebsite/statistics.html", context)


def source_info(request, source_id):  # Source pages
    quote_source = get_object_or_404(QuoteSource, pk=source_id)
    source_quotes = Quote.objects.filter(source=quote_source)
    context = {"quote_source": quote_source, "source_quotes": source_quotes,}
    return render(request, "QuoteWebsite/source_info.html", context)


def add_source(request):  # Page to add new sources
    if request.method == "POST":
        form = AddSourceForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            form = AddSourceForm()
            return render(
                request,
                "QuoteWebsite/add_source.html",
                {"form": form, "success": "Источник добавлен!"},  # Optional
            )
    else:
        form = AddSourceForm()
    return render(request, "QuoteWebsite/add_source.html", {"form": form})
