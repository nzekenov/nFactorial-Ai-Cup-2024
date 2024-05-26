# Generated by Django 4.2.13 on 2024-05-26 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import financial_advisor.wallet.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0002_wallet'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Wallet',
        ),
        migrations.AlterField(
            model_name='category',
            name='user',
            field=models.ForeignKey(default=financial_advisor.wallet.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='expense',
            name='user',
            field=models.ForeignKey(default=financial_advisor.wallet.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='income',
            name='user',
            field=models.ForeignKey(default=financial_advisor.wallet.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
