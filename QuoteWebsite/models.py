from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.core.exceptions import ValidationError

# The source table.
# It is the book/movie/song/game/other the Quote is taken from, combined with metadata
# The quote count should be queried whenever a new Quote is added
class QuoteSource(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=150)  # Author
    published_AC = models.BooleanField(default=True)  # Is published AC or BC
    publishment_date = models.PositiveIntegerField()  # Publishment year
    quote_count = models.PositiveIntegerField(
        default=0, null=True, blank=True, editable=False
    )  # How many quotes does the source have?

    def clean(self): # Check if valid
        if self.publishment_date > timezone.now().year and bool(self.published_AC): # Check if publishment year is real
            raise ValidationError({"publishment_date": "Нельзя процитировать источник из будущего"})
        
        def text_clean (string):
            return ''.join(e for e in string if e.isalnum()).lower() # Clean the quote from special characters, whitespaces. Make lowercase
        cleaned_sources = []
        for string in QuoteSource.objects.exclude(pk=self.pk): # Creating a list of clean sources
            cleaned_sources.append(text_clean(string.name))
        if text_clean(self.name) in cleaned_sources:
            raise ValidationError( # Check if source already exists
                {"quote_text": "Этот источник уже добавлен"}
            )
    def __str__(self):
        if len(self.name) < 35:
            return self.name
        else:
            return str(self.name)[:35] + "..."
        

class AddSourceForm(ModelForm): # Form for adding sources
    class Meta:
        model = QuoteSource
        fields = ["name", "author", "published_AC", "publishment_date"] 
        labels = {
            "name": "Название источника",
            "author": "Имя автора",
            "published_AC": "Опубликован ли источник в нашу эру?",
            "publishment_date": "Год публикации источника"
        }


# The Quote contents table
# Also indcludes the source and rating data
class Quote(models.Model):
    quote_text = models.TextField()
    quote_weight = models.PositiveIntegerField(default=50)
    # Connecting the source
    source = models.ForeignKey(QuoteSource, on_delete=models.CASCADE)
    # Making ratings 0 at start
    positive_rating = models.PositiveIntegerField(default=0, editable=False) 
    negative_rating = models.PositiveIntegerField(default=0, editable=False)
    total_rating = models.IntegerField(default=0, editable=False, null=True)
    
    def save(self, *args, **kwargs): 
        other_quotes = Quote.objects.filter(source=self.source).exclude(pk=self.pk).order_by("quote_rating", "quote_weight")
        if len(other_quotes) >= 3:
            other_quotes.first().delete()
        self.total_rating = self.positive_rating - self.negative_rating  # Update the total rating after rating changes
        super().save(*args, **kwargs)
        
    def clean(self): # Check if valid
        
        def text_clean (string):
            return ''.join(e for e in string if e.isalnum()).lower() # Clean the quote from special characters, whitespaces. Make lowercase
        cleaned_quotes = []
        for string in Quote.objects.exclude(pk=self.pk): # Creating a list of clean quotes
            cleaned_quotes.append(text_clean(string.quote_text))
            
        if self.quote_weight > 100 or self.quote_weight < 1:
            raise ValidationError(
                {"quote_weight": "Можно использовать только значения от 1 до 100"}
            )
        elif text_clean(self.quote_text) in cleaned_quotes:
            raise ValidationError(
                {"quote_text": "Эта цитата уже добавлена"}
            )
    def __str__(self):
        if len(self.quote_text) < 35:
            return self.quote_text
        else:
            return str(self.quote_text)[:35] + "..."
class AddQuoteForm(ModelForm): # Form for adding quotes
    class Meta:
        model = Quote
        fields = ["quote_text", "quote_weight", "source"] 
        labels = {
            "quote_text": "Текст цитаты",
            "quote_weight": "Вес цитаты, влияющий на шанс её выпадения (1-100)",
            "source": "Источник цитаты (книга, фильм и т.п.)",
        }
class PageViews(models.Model):
    views = models.PositiveIntegerField()
