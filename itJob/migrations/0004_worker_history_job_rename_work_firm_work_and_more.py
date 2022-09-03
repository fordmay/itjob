# Generated by Django 4.0.5 on 2022-07-29 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itJob', '0003_worker_skill_remove_work_skills_remove_worker_skills_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worker_history_job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firm', models.CharField(max_length=64)),
                ('description', models.TextField(max_length=300)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itJob.worker')),
            ],
        ),
        migrations.RenameModel(
            old_name='Work',
            new_name='Firm_work',
        ),
        migrations.DeleteModel(
            name='Work_places',
        ),
    ]