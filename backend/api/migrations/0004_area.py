# Generated by Django 4.1.6 on 2023-11-11 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_users_email_alter_users_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('boundary', models.BinaryField()),
                ('station', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
    ]
