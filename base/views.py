from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import FollowUser, Notification, User, Question, Answer, Post
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from itertools import chain


def home(request):
    q = request.POST.get('q') if request.POST else ''

    answers = Answer.objects.all().filter(Q(ques__body__icontains=q) |
                                          Q(user__username__icontains=q) | Q(body__icontains=q))
    posts = Post.objects.all().filter(Q(title__icontains=q) |
                                      Q(user__username__icontains=q) |
                                      Q(body__icontains=q))

    mess = sorted(chain(answers, posts),
                  key=lambda post: post.created_at, reverse=True)

    context = {'mess': mess}
    return render(request, 'base/home.html', context)


login_required(login_url='login')


def answer(request, pk):
    que = Question.objects.get(id=pk)
    answers = Answer.objects.filter(ques=que)
    if request.method == "POST":
        user = request.user
        ques = que
        answerA = request.POST.get('answer')
        a = Answer.objects.create(ques=que, user=user, body=answerA)
        a.save()
        return redirect('home')

    context = {'que': que, 'answers': answers}
    return render(request, 'base/answer.html', context)


def questions(request):
    ques = Question.objects.all().order_by('-created_at')
    context = {'ques': ques}
    return render(request, 'base/questions.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'base/login_page.html')


def logoutPage(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = User.objects.filter(username=username)
        if user or password1 != password2:
            return redirect('register')
        user = User.objects.create(username=username, email=email)
        user.set_password(password1)
        user.save()
        login(request, user)
        return redirect('home')

    return render(request, 'base/register_page.html')


login_required(login_url='login')


def ask(request):
    if request.method == 'POST':
        user = request.user
        a2a = request.POST.get('a2a')
        body = request.POST.get('ques')
        ques = Question.objects.create(user=user, body=body)
        ques.save()
        if a2a:
            a2aUser = User.objects.get(username=a2a)
            notif = Notification.objects.create(user=a2aUser, ques=ques)
            notif.save()
        return redirect('questions')

    return render(request, 'base/ask.html')


login_required(login_url='login')


def notifications(request):
    if request.user.is_authenticated:
        notifs = Notification.objects.filter(
            user=request.user).order_by('-created_at')
        context = {'notifs': notifs}
        return render(request, 'base/notifications.html', context)
    else:
        return redirect('login')


login_required(login_url='login')


def post(request):
    if request.method == 'POST':
        user = request.user
        content = request.POST.get('content')
        title = request.POST.get('title')
        if title:
            p = Post.objects.create(user=user, body=content, title=title)
        else:
            p = Post.objects.create(user=user, body=content)
        p.save()
        return redirect('home')

    return render(request, 'base/post.html')


login_required(login_url='login')


def profile(request, pk):
    user = User.objects.get(id=pk)
    answers = Answer.objects.filter(user=user)
    posts = Post.objects.filter(user=user)
    followers = FollowUser.objects.filter(user=user)
    following = FollowUser.objects.filter(follower=user)
    isFollowing = FollowUser.objects.filter(user=user, follower=request.user)

    mess = sorted(chain(answers, posts),
                  key=lambda post: post.created_at, reverse=True)

    context = {'user': user, 'mess': mess,
               'followers': followers, 'following': following, 'isFollowing': isFollowing}

    return render(request, 'base/profile_page.html', context)


login_required(login_url='login')


def follow(request, pk):
    follower = request.user
    followee = User.objects.get(id=pk)
    a = FollowUser.objects.filter(user=followee, follower=follower)
    if a:
        return redirect(request.META['HTTP_REFERER'])

    f = FollowUser.objects.create(user=followee, follower=follower)
    f.save()
    return redirect(request.META['HTTP_REFERER'])


login_required(login_url='login')


def unfollow(request, pk):
    follower = request.user
    followee = User.objects.get(id=pk)
    a = FollowUser.objects.get(user=followee, follower=follower)
    if a:
        a.delete()
    return redirect(request.META['HTTP_REFERER'])


login_required(login_url='login')


def followPosts(request):
    q = request.POST.get('q') if request.POST else ''

    followees = FollowUser.objects.filter(follower=request.user)
    mess = ''
    if followees:
        a = followees[0].user
        answers = Answer.objects.filter(user=a)
        posts = Post.objects.filter(user=a)
        mess = sorted(chain(answers, posts),
                      key=lambda post: post.created_at, reverse=True)

    for i in range(1, followees.count()):
        a = followees[i].user
        answers = Answer.objects.filter(Q(user=a) & (
                                        Q(ques__body__icontains=q) |
                                        Q(user__username__icontains=q) |
                                        Q(body__icontains=q)))
        posts = Post.objects.filter(Q(user=a) & (
                                    Q(title__icontains=q) |
                                    Q(user__username__icontains=q) |
                                    Q(body__icontains=q)))
        b = sorted(chain(answers, posts),
                   key=lambda post: post.created_at, reverse=True)
        mess = sorted(chain(mess, b),
                      key=lambda post: post.created_at, reverse=True)

    context = {'mess': mess, 'followees': followees}
    print(mess)
    return render(request, 'base/followers_post.html', context)


login_required(login_url='login')


def editProfile(request):
    form = UserForm(instance=request.user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.id)

    context = {'form': form}
    return render(request, 'base/edit.html', context)
