# Generated by Django 3.0.3 on 2020-04-07 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('CIF', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('meanTime', models.FloatField(blank=True, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=11, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=11, null=True)),
            ],
        ),
    ]