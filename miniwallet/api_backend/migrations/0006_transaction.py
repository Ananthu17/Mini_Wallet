# Generated by Django 3.1.6 on 2021-02-09 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_backend', '0005_auto_20210209_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('reference_id', models.CharField(max_length=50)),
            ],
        ),
    ]
