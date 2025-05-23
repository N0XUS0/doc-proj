# Generated by Django 3.2 on 2023-06-09 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0007_alter_profile_doctor_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor_image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='doctor/image_doctor/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='profile_doctor',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='doctor/profile/', verbose_name='Image'),
        ),
    ]
