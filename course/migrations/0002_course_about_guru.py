# Generated by Django 4.2.1 on 2023-06-12 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='about_guru',
            field=models.TextField(blank=True, null=True, verbose_name='About Guru'),
        ),
    ]