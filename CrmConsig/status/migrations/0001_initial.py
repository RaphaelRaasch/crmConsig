# Generated by Django 3.0.3 on 2021-05-26 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('perfil', models.CharField(choices=[('COMERCIAL', 'COMERCIAL'), ('ESTEIRA', 'ESTEIRA'), ('TELEFONE', 'TELEFONE')], max_length=12)),
                ('descricao', models.CharField(max_length=155)),
            ],
        ),
    ]
