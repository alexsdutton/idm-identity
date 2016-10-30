# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
                ('realm', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_relationship', to='organization.Organization')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationship', to='organization.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationRelationshipType',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationTag',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='organizationrelationship',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.OrganizationRelationshipType'),
        ),
        migrations.AddField(
            model_name='organization',
            name='relationships',
            field=models.ManyToManyField(through='organization.OrganizationRelationship', to='organization.Organization'),
        ),
        migrations.AddField(
            model_name='organization',
            name='tags',
            field=models.ManyToManyField(blank=True, to='organization.OrganizationTag'),
        ),
    ]