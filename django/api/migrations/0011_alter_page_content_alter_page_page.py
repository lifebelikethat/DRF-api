# Generated by Django 4.2.10 on 2024-02-24 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_page_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='content',
            field=models.TextField(max_length=512),
        ),
        migrations.AlterField(
            model_name='page',
            name='page',
            field=models.PositiveIntegerField(),
        ),
    ]
