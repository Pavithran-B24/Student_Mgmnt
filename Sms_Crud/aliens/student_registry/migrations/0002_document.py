# Generated by Django 4.2.5 on 2024-04-08 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_registry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myfile', models.FileField(upload_to='documents/')),
            ],
        ),
    ]
