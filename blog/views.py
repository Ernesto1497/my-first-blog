# Create your views here.
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'myblog/lista.html', {'posts': posts})
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'myblog/detalles.html', {'post': post})
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
            return render(request, 'myblog/lista.html', {'posts': posts})

#            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'myblog/editar.html', {'form': form})

