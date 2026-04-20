from django.db import migrations, models
 
 
class Migration(migrations.Migration):
 
    initial = True
 
    dependencies = []
 
    operations = [
        migrations.CreateModel(
            name='CollegeAdmin',
            fields=[
                ('id',          models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name',   models.CharField(max_length=100)),
                ('email',       models.EmailField(max_length=150, unique=True)),
                ('password',    models.CharField(max_length=128)),
                ('college_name',models.CharField(max_length=200)),
            ],
        ),
    ]