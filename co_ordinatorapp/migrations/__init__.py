from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('id',         models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name',  models.CharField(max_length=50)),
                ('email',      models.EmailField(max_length=150, unique=True)),
                ('phone',      models.CharField(max_length=10)),
                ('department', models.CharField(
                    choices=[
                        ('CMPICA',  'CMPICA'),
                        ('CSPIT',   'CSPIT'),
                        ('DEPSTAR', 'DEPSTAR'),
                    ],
                    max_length=50,
                )),
                ('password',   models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name':        'Coordinator',
                'verbose_name_plural': 'Coordinators',
                'db_table':            'coordinator',
            },
        ),
    ]
