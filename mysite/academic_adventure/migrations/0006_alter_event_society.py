# Generated by Django 4.0.1 on 2022-02-25 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic_adventure', '0005_alter_event_society_alter_society_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='society',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='academic_adventure.society'),
        ),
    ]