from django.db import models

# The source table.
# It is the book/movie/song/game/other the citation is taken from, combined with metadata
# The citation count should be queried whenever a new citation is added
class CitationSource (models.Model): 
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100, null=True, blank=True, default=None) # Author with default being None 
    publishment_date = models.DateField(null=True, blank=True, default=None) # Publishment year with default being None 
    citation_count = models.IntegerField(default=0) # How many citations does the source have?

class CitationRating (models.Model):
    positive_rating = models.PositiveIntegerField(default=0)
    negative_rating = models.PositiveIntegerField(default=0)
    weighted_rating = models.IntegerField(default=0) 

    def save(self, *args, **kwargs):
        self.weighted_rating = self.positive_rating - self.negative_rating  # Update the weighted rating after rating changes
        super().save(*args, **kwargs)

# The citation contents table
# Also indcludes the source and rating data
class Citation (models.Model):
    citation_text = models.TextField()
    citation_weight = models.PositiveIntegerField(default=5)
    source = models.ForeignKey(CitationSource, on_delete=models.CASCADE)
    rating = models.OneToOneField(CitationRating, on_delete=models.CASCADE)

class PageViews (models.Model):
    views = models.PositiveIntegerField()