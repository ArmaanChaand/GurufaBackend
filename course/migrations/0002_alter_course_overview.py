# Generated by Django 4.2.1 on 2023-06-05 15:13

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='overview',
            field=ckeditor.fields.RichTextField(blank=True, max_length=200, null=True, verbose_name='Course Overview'),
        ),
    ]