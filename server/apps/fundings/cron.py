from .models import Funding
from django.utils import timezone

def update_funding_status():
    # 현재 시간을 가져옵니다.
    current_time = timezone.now()

    # 7일 이상 지난 펀딩을 가져옵니다.
    fundings_to_close = Funding.objects.filter(is_closed=False, created_date__lte=current_time - timezone.timedelta(days=7))

    # 가져온 펀딩을 순회하면서 is_closed를 True로 설정합니다.
    for funding in fundings_to_close:
        funding.is_closed = True
        funding.save()