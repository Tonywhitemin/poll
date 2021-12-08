from django.shortcuts import render
from django.views.generic import ListView,DetailView,RedirectView
from .models import *
from django.urls import reverse
from django.views.generic.edit import CreateView,UpdateView,DeleteView

# Create your views here.
class PollList(ListView):
    model=Poll

class PollCreate(CreateView):
    model=Poll
    fields=["subject"]
    success_url="/poll/"
    template_name="form.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["title"]="新增投票主題"
        context["backpath"]="/"
        return context

class PollUpdate(UpdateView):
    model=Poll
    fields=["subject"]
    success_url="/poll/"
    template_name="form.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["title"]="修改投票主題"
        context["backpath"]="/"
        return context

class PollDelete(DeleteView):
    model=Poll
    fields=["subject"]
    success_url="/poll/"
    template_name="confirm_delete.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["title"]="刪除投票主題"
        context["backpath"]="/poll/"
        return context

class PollDetail(DetailView):
    model=Poll
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        options=Option.objects.filter(poll_id=self.kwargs["pk"])
        context["options"]=options
        return context

class PollVote(RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        option=Option.objects.get(id=self.kwargs["pk"])
        option.count +=1
        option.save()
        #return "/poll/"+str(option.poll_id)+"/"
        return "/poll/"

class OptionCreate(CreateView):
    model=Option
    fields=["title"]
    template_name="form.html"
    def get_success_url(self):
        return "/poll/"+str(self.kwargs["pid"])+"/"
    def form_valid(self,form):
        form.instance.poll_id=self.kwargs["pid"]
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["title"]="新增投票選項"
        context["backpath"]=reverse("poll_view", kwargs={"pk":self.kwargs["pid"]})
        return context

class OptionUpdate(UpdateView):
    model=Option
    fields=["title"]
    template_name="form.html"
    def get_success_url(self):
        return "/poll/"+str(self.object.poll_id)+"/"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["title"]="修改投票選項"
        context["backpath"]=reverse("poll_view", kwargs={"pk":self.object.poll_id})
        return context

class OptionDelete(DeleteView):
    model=Option
    fields=["title"]
    template_name="confirm_delete.html"
    def get_success_url(self):
        return reverse("poll_view",kwargs={"pk":self.object.poll_id})
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["title"]="刪除投票選項"
        context["backpath"]=reverse("poll_view", kwargs={"pk":self.object.poll_id})
        return context
