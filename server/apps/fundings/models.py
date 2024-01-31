from django.db import models
from apps.users.models import User

class Funding(models.Model) :
    title = models.CharField('제목', max_length=24)
    content = models.TextField('내용', max_length=1000)
    goal_price = models.IntegerField('목표금액', default=0)
    total_price = models.IntegerField('받은금액', default=0, null=True)
    photo = models.ImageField('이미지', blank=True, upload_to='fundings/%Y%m%d')
    present_link = models.CharField('상품 링크', max_length=100)
    
    #작성자
    user=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = '작성자', related_name='funding_user')
    #펀딩 개설일
    created_date = models.DateTimeField('작성일', auto_created=True, auto_now_add=True) #auto_now_add > 데이터베이스에 추가될때 // auto_create 생성해라
    
    def __str__(self):
        return f'{self.title}'
    
class Funding_Msg(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = '작성자', related_name='funding_msg_user')
    post = models.ForeignKey(Funding, on_delete=models.CASCADE, verbose_name = '펀딩글', related_name="funding_post")
    comment_name = models.CharField('From', max_length=12)
    funding_price = models.IntegerField('선물금액', default=0, null=True)
    content = models.TextField() 