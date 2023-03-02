# Generated by Django 4.1.6 on 2023-02-07 07:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('sexo', models.CharField(choices=[('F', 'Feminino'), ('M', 'Masculino')], max_length=1)),
                ('idade', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=19)),
                ('nutri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DadosPaciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('peso', models.FloatField()),
                ('altura', models.FloatField()),
                ('percentual_gordura', models.FloatField()),
                ('percentual_musculo', models.FloatField()),
                ('colesterol_hdl', models.FloatField()),
                ('colesterol_ldl', models.FloatField()),
                ('colesterol_total', models.FloatField()),
                ('trigliceridios', models.FloatField()),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.paciente')),
            ],
        ),
    ]
