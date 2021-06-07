# Generated by Django 3.0.3 on 2021-05-24 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Convenio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_convenio', models.CharField(choices=[('INSS', 'INSS'), ('FEDERAL', 'FEDERAL'), ('FORCAS', 'FORCAS'), ('GOVERNO', 'GOVERNO')], max_length=11)),
                ('convenio', models.CharField(max_length=155)),
                ('perfil', models.CharField(max_length=11)),
                ('descricao', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]