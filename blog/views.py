from django.shortcuts import render, redirect

from .forms import PostForm
# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_obj'

class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['title','author','body', 'photo']
    #Guardar la imagen

class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title','body','photo']

class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    #reverse_lazy es una funcion que espera que se ejecute la vista
    success_url = reverse_lazy('home')
# class BlogCreateViewImage():
#     if request.method == 'POST':
#         form = PostForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = PostForm()
#     return render(request,'post_new.html',{'form':form})


