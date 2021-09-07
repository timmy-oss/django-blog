from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from users.models import BlogUser

from blog.models import BlogPost, BlogPostCategory, PostComment

from .forms import CommentForm, SignInForm, SignUpForm


# Index View
def index_view(request):
    categories = BlogPostCategory.objects.all()
    featured_categories = list(categories.order_by('?'))
    featured_categories = [
        cat for cat in featured_categories if cat.posts.count() > 0][:6]

    posts = BlogPost.objects.all()
    featured_categories = categories.order_by('?')[:6]
    context = {
        'categories': categories,
        'posts': posts,
        'featured_categories': featured_categories
    }
    return render(request, 'blog/index.html', context)


# Latest Posts View
def latest_posts_view(request):
    categories = BlogPostCategory.objects.all()
    featured_categories = list(categories.order_by('?'))
    featured_categories = [
        cat for cat in featured_categories if cat.posts.count() > 0][:6]
    posts = BlogPost.objects.order_by('-pub_date').all()
    context = {
        'posts': posts,
        'featured_categories': featured_categories,
        'categories': categories
    }
    return render(request, 'blog/latest.html', context)


# Most popular Posts View
def popular_posts_view(request):
    categories = BlogPostCategory.objects.all()
    featured_categories = list(categories.order_by('?'))
    featured_categories = [
        cat for cat in featured_categories if cat.posts.count() > 0][:6]
    posts = BlogPost.objects.order_by('-upvotes').all()
    context = {
        'posts': posts,
        'featured_categories': featured_categories,
        'categories': categories
    }
    return render(request, 'blog/popular.html', context)


# AddComment
@login_required
def add_comment_view(request, id):
    current_user = request.user
    post = get_object_or_404(BlogPost, id=id)
    form = CommentForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        PostComment.objects.create(
            content=cd['comment'],
            author=current_user,
            post=post
        )
        return redirect(reverse('blog:post', args=[post.slug_field]))
    else:
        context = {
            'commment_form': form,
            'notice': 'Your comment has been added'
        }

        return render(request, 'blog/post.html', context)


# Vote View
@login_required
def vote_view(request, slugname, vote):
    post = get_object_or_404(BlogPost, slug_field=slugname)
    if int(vote) == 1:
        post.upvotes += 1
        post.save()
    elif int(vote) == 0:
        post.downvotes += 1
        post.save()

    if not request.session.get('voted_post_ids', None):
        request.session['voted_post_ids'] = [post.id, ]
    else:
        request.session.get('voted_post_ids').append(post.id)

    return redirect(reverse('blog:post', args=[slugname]))


# Today Post View
def today_post_view(request):
    post = BlogPost.objects.order_by('?').all()[0]
    show_votes = not(post.id in request.session.get('voted_post_ids', []))
    context = {
        'post': post,
        'show_votes': show_votes,


    }
    return render(request, 'blog/post.html', context)


# Sign out view
def sign_out_view(request):
    logout(request)
    request.session.flush()
    return redirect('/')

# sign in view


def sign_in_view(request):
    if request.method == 'GET':
        categories = BlogPostCategory.objects.all()
        featured_categories = list(categories.order_by('?'))
        featured_categories = [
            cat for cat in featured_categories if cat.posts.count() > 0][:6]
        context = {
            'categories': categories,
            'featured_categories': featured_categories,
        }
        return render(request, 'blog/sign_in.html', context)

    if request.method == 'POST':
        form = SignInForm(request.POST)
        categories = BlogPostCategory.objects.all()
        featured_categories = list(categories.order_by('?'))
        featured_categories = [
            cat for cat in featured_categories if cat.posts.count() > 0][:6]
        if not form.is_valid():
            context = {
                'form': form,
                'categories': categories,
                'featured_categories': featured_categories,
            }
            return render(request, 'blog/sign_in.html', context)

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=email,  password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'blog/sign_in.html', context={
                'message': 'Incorrect email or password',
                'categories': categories,
                'featured_categories': featured_categories,
            })


# sign up view


def sign_up_view(request):
    if request.method == 'GET':
        categories = BlogPostCategory.objects.all()
        featured_categories = list(categories.order_by('?'))
        featured_categories = [
            cat for cat in featured_categories if cat.posts.count() > 0][:6]
        context = {
            'categories': categories,
            'featured_categories': featured_categories,
        }
        return render(request, 'blog/sign_up.html', context)

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        categories = BlogPostCategory.objects.all()
        featured_categories = list(categories.order_by('?'))
        featured_categories = [
            cat for cat in featured_categories if cat.posts.count() > 0][:6]
        if not form.is_valid():
            context = {
                'form': form,
                'categories': categories,
                'featured_categories': featured_categories,
            }
            return render(request, 'blog/sign_up.html', context)

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        fn = form.cleaned_data['fn']
        ln = form.cleaned_data['ln']
        BlogUser.objects.create_user(
            firstname=fn,
            lastname=ln,
            email=email,
            password=password,

        )
        return redirect('/sign-in/')


# Post View
def post_view(request, slugname):
    post = get_object_or_404(BlogPost, slug_field=slugname)
    categories = BlogPostCategory.objects.all()
    featured_categories = list(categories.order_by('?'))
    featured_categories = [
        cat for cat in featured_categories if cat.posts.count() > 0][:6]
    show_votes = not(post.id in request.session.get('voted_post_ids', []))
    context = {
        'post': post,
        'categories': categories,
        'featured_categories': featured_categories,
        'show_votes': show_votes,
    }
    return render(request, 'blog/post.html', context)


# Category View
def category_view(request, slugname):
    category = get_object_or_404(BlogPostCategory, slug_field=slugname)
    categories = BlogPostCategory.objects.all()
    featured_categories = list(categories.order_by('?'))
    featured_categories = [
        cat for cat in featured_categories if cat.posts.count() > 0][:6]
    context = {
        'category': category,
        'categories': categories,
        'featured_categories': featured_categories,
        'posts': category.posts.all(),
    }
    return render(request, 'blog/category.html', context)
