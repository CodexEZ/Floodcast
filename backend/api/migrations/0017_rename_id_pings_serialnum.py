# Generated by Django 4.1.6 on 2024-02-03 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_pings_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pings',
            old_name='id',
            new_name='serialnum',
        ),
    ]