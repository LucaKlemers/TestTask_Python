from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


# The source table.
# It is the book/movie/song/game/other the Quote is taken from, combined with metadata
# The quote count should be queried whenever a new Quote is added
class QuoteSource(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(
        max_length=100, null=True, blank=True, default=None
    )  # Author with default being None
    published_AC = models.BooleanField(default=True)  # Is published AC or BC
    publishment_date = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=None,
    )  # Publishment year with default being None
    quote_count = models.PositiveIntegerField(
        default=0, editable=False
    )  # How many quotes does the source have?

    def clean(self):
        if self.publishment_date > timezone.now().year and bool(self.published_AC):
            raise ValueError(
                {"self.publishment_date": "You can't quote sources from future"}
            )


# The Quote contents table
# Also indcludes the source and rating data
class Quote(models.Model):
    quote_text = models.TextField()
    quote_weight = models.PositiveIntegerField(default=5)
    source = models.ForeignKey(QuoteSource, on_delete=models.CASCADE)
    positive_rating = models.PositiveIntegerField(default=0)
    negative_rating = models.PositiveIntegerField(default=0)
    weighted_rating = models.IntegerField(default=0)


class PageViews(models.Model):
    views = models.PositiveIntegerField()
