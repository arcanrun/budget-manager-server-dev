# Generated by Django 2.1.7 on 2019-11-20 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0014_auto_20191120_1410'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vkuser',
            old_name='isCostumDarkTheme',
            new_name='is_costom_dark_theme',
        ),
        migrations.RenameField(
            model_name='vkuser',
            old_name='isVkTheme',
            new_name='is_vk_theme',
        ),
    ]
