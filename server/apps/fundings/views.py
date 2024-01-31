from django.shortcuts import render, redirect
from .forms import FundingForm, MessageForm
from .models import Funding, Funding_Msg
from django.db.models import F
from datetime import date

def main(request) :
    today = date.today()
    fundings = Funding.objects.filter (user__birthday__month = today.month, user__birthday__day = today.day) 
    fundings = fundings[:3]
    ctx = {
        "fundings": fundings,
           }
    return render(request, 'fundings/main.html', ctx)

def create(request) :
    if request.user.is_authenticated:
        if request.method == 'GET':
            funding = Funding()
            funding.user = request.user
            form = FundingForm(instance=funding)
            ctx = {
                'form':form
            }
            return render(request, 'fundings/fundings_create.html', ctx)
        #post일때
        elif request.method == "POST":
            funding = Funding()
            funding.user = request.user
            form = FundingForm(request.POST, request.FILES, instance=funding)
            if form.is_valid():
                form.save()
                funding_id = funding.id
                return redirect('fundings:main')
            else:
                ctx = {
                    "form": form
                }
                return render (request, 'fundings/fundings_create.html', ctx)
    else:
        return redirect('users:login')
def detail(request, pk) :
    funding = Funding.objects.get(id=pk)
    progress = int(funding.total_price / funding.goal_price * 100)
    ctx = {'funding':funding, 'progress':progress}    
    return render(request, 'fundings/fundings_detail.html', ctx)

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

def create_message(request, pk) :
    funding = Funding.objects.get (id = pk)
    if request.user.is_authenticated:
        if request.method == "GET":
            funding_msg = Funding_Msg()
            funding_msg.user = request.user
            funding_msg.post = funding
            form = MessageForm(instance=funding_msg)
            ctx = {
                'form':form
            }
            return render(request, 'fundings/fundings_message_create.html', ctx)
        
        elif request.method == "POST":
            funding_msg = Funding_Msg()
            funding_msg.user = request.user
            funding_msg.post = funding
            form = MessageForm(request.POST, instance=funding_msg)
            if form.is_valid():
                form.save()
                funding.total_price = funding.total_price + funding_msg.funding_price 
                funding.msg_count += 1
                if funding.total_price >= funding.goal_price:
                    funding.is_achieved = True
                funding.save()
                return redirect('fundings:main')
            else:
                ctx = {
                    "form": form
                }
                return render (request, 'fundings/fundings_message_create.html', ctx)
    
    else:
        if request.method == "GET":
            funding_msg = Funding_Msg()
            funding_msg.post = funding
            form = MessageForm(instance=funding_msg)
            ctx = {
                'form':form
            }
            return render(request, 'fundings/fundings_message_create.html', ctx)
        
        elif request.method == "POST":
            funding_msg = Funding_Msg()
            funding_msg.post = funding
            form = MessageForm(request.POST, instance=funding_msg)
            if form.is_valid():
                form.save()
                funding.total_price = funding.total_price + funding_msg.funding_price 
                funding.msg_count += 1
                if funding.total_price >= funding.goal_price:
                    funding.is_achieved = True
                funding.save()
                return redirect('fundings:main')
            else:
                ctx = {
                    "form": form
                }
                return render (request, 'fundings/fundings_message_create.html', ctx)