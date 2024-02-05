# Generated by Django 5.0.1 on 2024-02-04 06:16

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundings', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='funding',
            name='is_achieved',
            field=models.BooleanField(blank=True, default=False, verbose_name='펀딩 달성 여부'),
        ),
        migrations.AddField(
            model_name='funding',
            name='is_closed',
            field=models.BooleanField(blank=True, default=False, verbose_name='펀딩 종료'),
        ),
        migrations.AddField(
            model_name='funding',
            name='msg_count',
            field=models.IntegerField(default=0, verbose_name='메시지 개수'),
        ),
        migrations.AddField(
            model_name='funding_msg',
            name='written_date',
            field=models.DateTimeField(auto_created=True, auto_now_add=True, default=django.utils.timezone.now, verbose_name='메시지 작성일'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='funding',
            name='total_price',
            field=models.IntegerField(default=0, verbose_name='받은금액'),
        ),
        migrations.AlterField(
            model_name='funding_msg',
            name='comment_name',
            field=models.CharField(max_length=12, verbose_name='친구에게 보여질 이름'),
        ),
        migrations.AlterField(
            model_name='funding_msg',
            name='content',
            field=models.TextField(verbose_name='축하 메시지'),
        ),
        migrations.AlterField(
            model_name='funding_msg',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='funding_msg_user', to=settings.AUTH_USER_MODEL, verbose_name='작성자'),
        ),
    ]