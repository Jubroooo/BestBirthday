from django.shortcuts import render, redirect
from .forms import FundingForm
from .models import Funding, Funding_Msg


def main(request) :
    funding = Funding.objects.all()
    ctx = {"fundings" : funding}
    return render(request, 'fundings/main.html', ctx)

def create(request) :
    if request.method == 'GET':
        form = FundingForm()
        ctx = {'form':form}
        return render(request, 'fundings/funding_create.html', ctx)
    #post일때
    form = FundingForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    return redirect('fundings:detail')

def detail(request, pk) :
    funding = Funding.objects.get(id=pk)
    ctx = {'funding':funding}
    return render(request, 'fundings/funding_detail.html', ctx)

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
        return render(request, 'fundings/funding_update.html', ctx)
    
    form=FundingForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        form.save()
    return redirect('fundings:detail', pk)
