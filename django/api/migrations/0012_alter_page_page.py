# Generated by Django 4.2.10 on 2024-02-24 05:33

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_page_content_alter_page_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='page',
            field=models.PositiveIntegerField(validators=[api.models.exempt_zero]),
        ),
    ]
