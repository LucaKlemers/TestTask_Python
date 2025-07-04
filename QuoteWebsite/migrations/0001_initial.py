# Generated by Django 5.2.3 on 2025-07-02 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageViews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='QuoteRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positive_rating', models.PositiveIntegerField(default=0)),
                ('negative_rating', models.PositiveIntegerField(default=0)),
                ('weighted_rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='QuoteSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('author', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('published_AC', models.BooleanField(default=True)),
                ('publishment_date', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('quote_count', models.PositiveIntegerField(default=0, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_text', models.TextField()),
                ('quote_weight', models.PositiveIntegerField(default=5)),
                ('rating', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='QuoteWebsite.quoterating')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuoteWebsite.quotesource')),
            ],
        ),
    ]
