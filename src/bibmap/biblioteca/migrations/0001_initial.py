# Generated by Django 2.2.4 on 2019-11-18 04:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('livro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Biblioteca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('nome', models.CharField(max_length=256)),
                ('foto', models.ImageField(upload_to='images/bib/')),
                ('nome_bibliotecario', models.CharField(max_length=256)),
                ('independente', models.BooleanField()),
                ('aquisicao_acervo', models.BooleanField()),
                ('aberto_a_comunidade', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True, verbose_name='Biblioteca está ativa?')),
                ('mapeada', models.BooleanField()),
                ('latitude', models.DecimalField(decimal_places=16, max_digits=19)),
                ('longitude', models.DecimalField(decimal_places=15, max_digits=19)),
                ('last_reseted_views', models.DateField(default=datetime.date(2000, 1, 1))),
                ('visualizacoes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(max_length=9)),
                ('rua', models.CharField(max_length=256)),
                ('numero', models.IntegerField()),
                ('bairro', models.CharField(max_length=256)),
                ('cidade', models.CharField(max_length=256)),
                ('estado', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='RecursosOpcionais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('computador', models.BooleanField()),
                ('ar_condicionado', models.BooleanField()),
                ('mesa_de_estudo', models.BooleanField()),
                ('empresta_livro', models.BooleanField()),
                ('wifi', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='LivroAssociado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('estado', models.IntegerField(choices=[(0, 'Excelente'), (1, 'Ótimo'), (2, 'Bom'), (3, 'Regular'), (4, 'Ruim'), (5, 'Péssimo')], default=0)),
                ('numero_protocolo', models.IntegerField(default=0)),
                ('corredor', models.CharField(max_length=5)),
                ('prateleira', models.CharField(max_length=5)),
                ('biblioteca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.Biblioteca')),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livro.Livro')),
            ],
        ),
        migrations.AddField(
            model_name='biblioteca',
            name='endereco',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='biblioteca.Endereco'),
        ),
        migrations.AddField(
            model_name='biblioteca',
            name='recursos_opcionais',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='biblioteca.RecursosOpcionais'),
        ),
    ]
