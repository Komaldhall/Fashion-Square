# Generated by Django 2.0.7 on 2018-12-07 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('its_eCommerce', '0012_remove_user_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='catType',
            field=models.CharField(default='men', max_length=100),
            preserve_default=False,
        ),
    ]
