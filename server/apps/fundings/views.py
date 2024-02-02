from django.shortcuts import render, redirect
from .forms import FundingForm, MessageForm
from .models import Funding, Funding_Msg

# 예진:html보려고 추가한 것
def all_list(request):
    return render(request,'fundings/all_birthday_list.html')
def main(request) :
    funding = Funding.objects.all()
    ctx = {"fundings" : funding}
    return render(request, 'fundings/main2.html', ctx)

def create(request) :
    if request.method == 'GET':
        form = FundingForm()
        ctx = {'form':form}
        return render(request, 'fundings/fundings_create.html', ctx)
    #post일때
    form = FundingForm(request.POST, request.FILES)
    if form.is_valid():
        new_funding = form.save(user=request.user)
        pk_of_new_funding = new_funding.pk
        return redirect('fundings:detail', pk=pk_of_new_funding)
#뷰 확인용
def detail(request) :
    return render(request, 'fundings/fundings_detail.html')

# def detail(request, pk) :
#     funding = Funding.objects.get(id=pk)
#     progress = int(funding.total_price / funding.goal_price * 100)
#     ctx = {'funding':funding, 'progress':progress}    
#     return render(request, 'fundings/fundings_detail.html', ctx)

def delete(request, pk) :
    if request.method == "POST":
        posts = Funding.objects.get(id=pk)
        posts.delete()
        # = Post.objects.get(id=pk).delete()
    return redirect('fundings:main')

def update(request, pk) :
    post=Funding.objects.get(id=pk)
    
    if request.method=='GET':
        form = FundingForm(instance=post)
        ctx = {'form':form, 'pk':pk}
        return render(request, 'fundings/fundings_update.html', ctx)
    
    form=FundingForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        form.save()
    return redirect('fundings:detail', pk)

def message(request) :
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, request=request, current_post=current_post)
        if form.is_valid():
            # Save the form
            form.save()
            # Your additional logic here
    else:
        form = MessageForm(request=request, current_post=current_post)