# Generated by Django 4.1.6 on 2024-02-03 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_pings_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pings',
            name='id',
            field=models.AutoField(max_length=5, primary_key=True, serialize=False),
        ),
    ]