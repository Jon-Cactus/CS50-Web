# Generated by Django 5.1.4 on 2025-02-16 12:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bids', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=256)),
                ('category', models.CharField(choices=[('msc', 'Misc'), ('ctb', 'Collectibles'), ('mrb', 'Memorabilia'), ('fnt', 'Furniture')], default='msc', max_length=3)),
                ('image_URL', models.URLField()),
                ('starting_bid', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('highest_bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_highest_bids', to='auctions.bids')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='won_auctions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bids',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_bids', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(related_name='watching_user', to='auctions.listing'),
        ),
    ]
