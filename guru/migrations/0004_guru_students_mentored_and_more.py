# Generated by Django 4.2.1 on 2023-10-13 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guru', '0003_guru_guru_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guru',
            name='students_mentored',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Students mentored'),
        ),
        migrations.AddField(
            model_name='historicalguru',
            name='students_mentored',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Students mentored'),
        ),
        migrations.AlterField(
            model_name='guru',
            name='guru_description',
            field=models.TextField(blank=True, help_text="Insert '|' between sentences to create distinct bullet points.", null=True),
        ),
        migrations.AlterField(
            model_name='historicalguru',
            name='guru_description',
            field=models.TextField(blank=True, help_text="Insert '|' between sentences to create distinct bullet points.", null=True),
        ),
    ]