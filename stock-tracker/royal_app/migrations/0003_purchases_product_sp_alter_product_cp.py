# Generated by Django 4.1 on 2022-12-12 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('royal_app', '0002_remove_product_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('nos', models.IntegerField()),
                ('payment', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sp',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='cp',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
