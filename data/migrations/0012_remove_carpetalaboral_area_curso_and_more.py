# Generated by Django 4.1.7 on 2023-10-10 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_remove_areacurso_carpeta_laboral_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carpetalaboral',
            name='area_curso',
        ),
        migrations.RemoveField(
            model_name='carpetalaboral',
            name='capacitador',
        ),
        migrations.RemoveField(
            model_name='carpetalaboral',
            name='ocupacion',
        ),
        migrations.RemoveField(
            model_name='carpetalaboral',
            name='puesto',
        ),
        migrations.AddField(
            model_name='areacurso',
            name='carpeta_laboral',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='data.carpetalaboral'),
        ),
        migrations.AddField(
            model_name='capacitador',
            name='carpeta_laboral',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='data.carpetalaboral'),
        ),
        migrations.AddField(
            model_name='ocupacion',
            name='carpeta_laboral',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='data.carpetalaboral'),
        ),
        migrations.AddField(
            model_name='puesto',
            name='carpeta_laboral',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='data.carpetalaboral'),
        ),
    ]
