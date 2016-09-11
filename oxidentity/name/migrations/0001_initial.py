# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('plain', models.TextField(blank=True)),
                ('plain_full', models.TextField(blank=True)),
                ('marked_up', models.TextField(blank=True)),
                ('familiar', models.TextField(blank=True)),
                ('sort', models.TextField(blank=True)),
                ('first', models.TextField(blank=True)),
                ('last', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NameComponent',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('order', models.PositiveSmallIntegerField()),
                ('type', models.CharField(choices=[('title', 'Title'), ('given', 'Given name'), ('middle', 'Middle name'), ('family', 'Family name'), ('suffix', 'Suffix'), ('name', 'Name')], max_length=20)),
                ('value', models.TextField()),
                ('name', models.ForeignKey(to='name.Name', related_name='components')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='NameContext',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('label', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='name',
            name='contexts',
            field=models.ManyToManyField(to='name.NameContext'),
        ),
    ]
