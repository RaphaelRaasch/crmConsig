# Generated by Django 3.0.3 on 2021-05-24 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data_consig', '0001_initial'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Está ativo')),
                ('cpf', models.CharField(default='', max_length=30, verbose_name='CPF')),
                ('matricula', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data_consig.MatriculaDetalhada')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.Usuario')),
            ],
            options={
                'verbose_name': 'Histórico Realtime',
                'verbose_name_plural': 'Históricos Realtime',
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Está ativo')),
                ('cpf', models.CharField(default='', max_length=30, verbose_name='CPF')),
                ('phone', models.CharField(max_length=30, verbose_name='Telefone')),
                ('obs', models.CharField(blank=True, default='', max_length=255, verbose_name='Observação')),
                ('status', models.IntegerField(choices=[(2, 'Mudo/Inexistente'), (4, 'Não Existe Telefone'), (6, 'Não Encontrado/Engano'), (8, 'Não Atende - Só Chama'), (10, 'Não Atende - Ocupado'), (12, 'Não Atende - Caixa Postal/Desligado'), (14, 'Nenhuma Operação Disponível no Momento'), (16, 'Falecido'), (18, 'Não Deseja Receber Contato'), (1, 'Não Pode Atender a Ligação'), (20, 'Margem Insuficiente'), (3, 'Cliente com Possibilidade'), (5, 'Recado com Terceiros'), (22, 'Cliente Sem Interesse'), (7, 'Cliente vai Pensar'), (9, 'Agendado'), (11, 'Em Negociação'), (13, 'Aceitou a Oferta'), (15, 'Cliente Já Contratado')], verbose_name='Retorno')),
                ('date_return', models.DateTimeField(blank=True, null=True, verbose_name='Data de Retorno')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.Empresa')),
                ('matricula', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data_consig.MatriculaDetalhada')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.Usuario')),
            ],
            options={
                'verbose_name': 'Atividade',
            },
        ),
    ]