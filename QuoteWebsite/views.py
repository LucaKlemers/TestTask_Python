from random import choices
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Quote, QuoteSource, AddQuoteForm, AddSourceForm, PageViews


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

    page_views = PageViews.objects.get_or_create(name="views")[0]
    
    if request.POST.get("vote") == "upvote" or request.POST.get("vote") == "downvote":
        selected_quote_id = request.COOKIES.get("quote_cookie")
        selected_quote = (
            Quote.objects.get(pk=selected_quote_id) if selected_quote_id else None
        )
        vote_type = request.POST.get("vote")
        cookie = f"{selected_quote.pk}_vote"
        current_vote = request.COOKIES.get(cookie)
        context = {"selected_quote": selected_quote, "views": page_views.views}
        request.session["was_button"] = True
        response = HttpResponseRedirect(reverse("index"))
        # Vote toggling
        if vote_type == current_vote:
            if vote_type == "upvote":
                selected_quote.positive_rating -= 1
            elif vote_type == "downvote":
                selected_quote.negative_rating -= 1
            response.delete_cookie(cookie)
        else:
            if current_vote == "upvote":
                selected_quote.positive_rating -= 1
            elif current_vote == "downvote":
                selected_quote.negative_rating -= 1

            if vote_type == "upvote":
                selected_quote.positive_rating += 1
            elif vote_type == "downvote":
                selected_quote.negative_rating += 1

            response.set_cookie(  # Adding a cookie
                cookie,
                vote_type,
                max_age=30 * 24 * 60 * 60,
                httponly=True,
                samesite="Lax",
            )
        selected_quote.save()
        return response
    elif request.session.get("was_button"):
        request.session["was_button"] = False
        selected_quote_id = request.COOKIES.get("quote_cookie")
        selected_quote = (
            Quote.objects.get(pk=selected_quote_id) if selected_quote_id else None
        )
        context = {"selected_quote": selected_quote, "views": page_views.views, "vote_status": selected_quote.check_vote(request),}
        response = render(request, "QuoteWebsite/index.html", context)
        return response
    else:
        page_views.views += 1
        page_views.save()
        selected_quote = random_quote(0.25)
        context = {"selected_quote": selected_quote, "views": page_views.views, "vote_status": selected_quote.check_vote(request),}
        response = render(request, "QuoteWebsite/index.html", context)
        response.delete_cookie("quote_cookie")
        response.set_cookie(
            "quote_cookie",
            selected_quote.pk,
            max_age=30 * 24 * 60 * 60,
            httponly=True,
            samesite="Lax",
        )
        return response


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


def vote(request, selected_quote):  # Like/dislike buttons
    vote_type = request.POST.get("vote")
    cookie = f"{selected_quote.pk}+_vote"
    current_vote = request.COOKIES.get(cookie)
    response = HttpResponse(status=204)
    # Vote toggling
    if vote_type == current_vote:
        if vote_type == "upvote":
            selected_quote.positive_rating -= 1
        elif vote_type == "downvote":
            selected_quote.negative_rating -= 1
        response.delete_cookie(cookie)
    else:
        if current_vote == "upvote":
            selected_quote.positive_rating -= 1
        elif current_vote == "downvote":
            selected_quote.negative_rating -= 1

        if vote_type == "upvote":
            selected_quote.positive_rating += 1
        elif vote_type == "downvote":
            selected_quote.negative_rating += 1

        response.set_cookie(  # Adding a cookie
            cookie, vote_type, max_age=30 * 24 * 60 * 60, httponly=True, samesite="Lax"
        )
    selected_quote.save()
    return response


def statistics(request):  # Statistics page (top quotes, etc.)
    top_quotes = Quote.objects.order_by("-total_rating")[:10]
    context = {
        "top_quotes": top_quotes,
    }
    return render(request, "QuoteWebsite/statistics.html", context)


def source_info(request, source_id):  # Source pages
    quote_source = get_object_or_404(QuoteSource, pk=source_id)
    source_quotes = Quote.objects.filter(source=quote_source)
    context = {
        "quote_source": quote_source,
        "source_quotes": source_quotes,
    }
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
