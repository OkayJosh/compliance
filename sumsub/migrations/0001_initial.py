# Generated by Django 5.1.2 on 2024-10-17 11:31

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantModel',
            fields=[
                ('uuid', models.UUIDField(default=uuid.UUID('0b757ef5-3bb3-4292-9b4b-0ce205decfd8'), primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('dob', models.DateField()),
                ('nationality', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('applicant_id', models.CharField(max_length=100, unique=True)),
                ('verification_status', models.CharField(max_length=100)),
            ],
        ),
    ]
