# Generated by Django 5.1.1 on 2024-09-26 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bid_listing'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='watchlist',
            unique_together={('listing', 'user')},
        ),
    ]
