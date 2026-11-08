from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payroll", "0018_seed_algeria_parameters_2026"),
    ]

    operations = [
        migrations.AddField(
            model_name="filingstatus",
            name="tax_engine",
            field=models.CharField(
                choices=[
                    ("standard", "Standard slabs"),
                    ("dz_irg", "Algeria IRG"),
                ],
                default="standard",
                max_length=20,
                verbose_name="Tax engine",
            ),
        ),
    ]
