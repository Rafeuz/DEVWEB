# Generated by Django 2.2.5 on 2019-09-05 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='postagem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Postagem'),
        ),
        migrations.AlterField(
            model_name='postagem',
            name='data',
            field=models.DateTimeField(verbose_name='Data de publicação'),
        ),
    ]
