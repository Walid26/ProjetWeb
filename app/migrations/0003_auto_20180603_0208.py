# Generated by Django 2.0 on 2018-06-03 02:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180603_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requete',
            name='demandeurRequete',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idDemandeurRequete', to=settings.AUTH_USER_MODEL, verbose_name='Pseudo demandeur'),
        ),
    ]
