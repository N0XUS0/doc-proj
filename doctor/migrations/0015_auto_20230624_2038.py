# Generated by Django 3.2 on 2023-06-24 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0014_auto_20230624_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialization',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='specialization_image/', verbose_name='الصوره'),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='spec',
            field=models.CharField(max_length=200, verbose_name='تخصص2'),
        ),
    ]
