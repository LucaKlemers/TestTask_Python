from django.contrib import admin

# Register your models here.
from .models import QuoteSource
from .models import Quote
admin.site.register(QuoteSource)
admin.site.register(Quote)
