# Generated by Django 5.1.5 on 2025-01-27 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DigitalFlow", "0006_remove_orden_firma_cliente_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orden",
            name="pdf_orden",
        ),
        migrations.AddField(
            model_name="orden",
            name="pdf_generado",
            field=models.FileField(blank=True, null=True, upload_to="pdfs/"),
        ),
    ]
