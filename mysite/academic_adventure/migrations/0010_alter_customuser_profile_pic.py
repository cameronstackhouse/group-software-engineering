# Generated by Django 4.0.1 on 2022-03-21 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic_adventure', '0009_image_icon_image_in_store_image_rarity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academic_adventure.image'),
        ),
    ]
