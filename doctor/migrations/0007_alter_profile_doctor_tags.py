# Generated by Django 3.2 on 2023-06-04 05:28

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('doctor', '0006_auto_20230604_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_doctor',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
