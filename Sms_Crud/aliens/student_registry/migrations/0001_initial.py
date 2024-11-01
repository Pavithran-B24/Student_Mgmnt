# Generated by Django 4.2.5 on 2024-03-15 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=60)),
                ('role_no', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.IntegerField()),
                ('degree', models.CharField(max_length=30)),
                ('dept', models.CharField(max_length=50)),
            ],
        ),
    ]
