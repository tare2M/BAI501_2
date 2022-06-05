# Generated by Django 4.0.4 on 2022-05-18 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='heuristic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heuristic_name', models.CharField(max_length=50)),
                ('heuristic_value', models.IntegerField()),
                ('country_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='heuristic', to='main.country')),
            ],
        ),
        migrations.CreateModel(
            name='graph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name1', models.CharField(max_length=50)),
                ('city_name2', models.CharField(max_length=50)),
                ('actual_distance', models.IntegerField()),
                ('country_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='graph', to='main.country')),
            ],
        ),
    ]
