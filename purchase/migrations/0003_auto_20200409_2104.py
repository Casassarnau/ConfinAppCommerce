# Generated by Django 3.0.3 on 2020-04-09 21:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0002_purchase_endtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('E', 'Expired'), ('P', 'Pending')], default='E', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]