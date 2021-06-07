# Generated by Django 3.0.3 on 2021-05-24 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('uploads_sms', '0001_initial'),
        ('filial', '0001_initial'),
        ('authentication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EnvioSms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.IntegerField(blank=True, null=True)),
                ('matricula', models.IntegerField(blank=True, null=True)),
                ('celular', models.CharField(blank=True, max_length=11, null=True)),
                ('potencial', models.IntegerField()),
                ('mensagem', models.CharField(blank=True, max_length=160, null=True)),
                ('data_envio', models.DateTimeField(blank=True, null=True)),
                ('id_envio', models.CharField(blank=True, max_length=155)),
                ('status_sms', models.CharField(blank=True, max_length=3)),
                ('resposta', models.CharField(blank=True, max_length=160)),
                ('nr_resposta', models.IntegerField(default=0)),
                ('data_hora_resposta', models.DateTimeField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('empresa_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.Empresa')),
                ('filial_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filial.Filial')),
                ('upload_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uploads_sms.UploadSms', to_field='pathFile')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
