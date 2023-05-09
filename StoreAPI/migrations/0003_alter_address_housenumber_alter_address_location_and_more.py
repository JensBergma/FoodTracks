# Generated by Django 4.2.1 on 2023-05-09 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StoreAPI', '0002_alter_openinghours_dayofweek'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='houseNumber',
            field=models.CharField(help_text='The house or building number.', max_length=10),
        ),
        migrations.AlterField(
            model_name='address',
            name='location',
            field=models.CharField(help_text='The city or town name.', max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='postcode',
            field=models.CharField(help_text='The postal code or ZIP code.', max_length=10),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(help_text='The street name.', max_length=100),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='closingTime',
            field=models.TimeField(help_text='The time the store closes.'),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='dayOfWeek',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], help_text='The day of the week.'),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='isClosed',
            field=models.BooleanField(default=False, help_text='Whether the store is closed on this day.'),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='isSpecialTime',
            field=models.BooleanField(default=False, help_text='Whether this is a special opening time, such as a holiday.'),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='openingTime',
            field=models.TimeField(help_text='The time the store opens.'),
        ),
        migrations.AlterField(
            model_name='store',
            name='address',
            field=models.ManyToManyField(help_text='The address of the store.', to='StoreAPI.address'),
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(help_text='The name of the store.', max_length=150),
        ),
        migrations.AlterField(
            model_name='store',
            name='openingHours',
            field=models.ManyToManyField(help_text='The opening hours of the store.', to='StoreAPI.openinghours'),
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together={('street', 'houseNumber', 'location', 'postcode')},
        ),
    ]
