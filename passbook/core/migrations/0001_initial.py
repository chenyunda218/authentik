# Generated by Django 2.1.3 on 2018-11-22 10:03

import uuid

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('created', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('action', models.CharField(choices=[('allow', 'allow'), ('deny', 'deny')], max_length=20)),
                ('negate', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RuleModel',
            fields=[
                ('created', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserSourceConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('rulemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='passbook_core.RuleModel')),
                ('name', models.TextField()),
                ('launch_url', models.URLField(blank=True, null=True)),
                ('icon_url', models.TextField(blank=True, null=True)),
                ('provider', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='passbook_core.Provider')),
            ],
            options={
                'abstract': False,
            },
            bases=('passbook_core.rulemodel',),
        ),
        migrations.CreateModel(
            name='FieldMatcherRule',
            fields=[
                ('rule_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='passbook_core.Rule')),
                ('user_field', models.TextField()),
                ('match_action', models.CharField(choices=[('startswith', 'startswith'), ('endswith', 'endswith'), ('endswith', 'contains'), ('regexp', 'regexp'), ('exact', 'exact')], max_length=50)),
                ('value', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('passbook_core.rule',),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('rulemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='passbook_core.RuleModel')),
                ('name', models.TextField()),
                ('slug', models.SlugField()),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('passbook_core.rulemodel',),
        ),
        migrations.AddField(
            model_name='rulemodel',
            name='rules',
            field=models.ManyToManyField(to='passbook_core.Rule'),
        ),
        migrations.AddField(
            model_name='usersourceconnection',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passbook_core.Source'),
        ),
        migrations.AddField(
            model_name='user',
            name='applications',
            field=models.ManyToManyField(to='passbook_core.Application'),
        ),
        migrations.AddField(
            model_name='user',
            name='sources',
            field=models.ManyToManyField(through='passbook_core.UserSourceConnection', to='passbook_core.Source'),
        ),
        migrations.AlterUniqueTogether(
            name='usersourceconnection',
            unique_together={('user', 'source')},
        ),
    ]
