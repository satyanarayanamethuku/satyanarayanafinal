# Generated by Django 2.2.4 on 2019-08-30 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0011_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=500)),
                ('date', models.CharField(max_length=500)),
                ('body', models.CharField(max_length=1000)),
            ],
        ),
    ]
