from datetime import datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.views.generic.base import View, HttpResponseRedirect, HttpResponse
from .forms import  NewVideoForm , CommentForm
from .models import Video, Comment, Like, Favourite, History, Tag, Flag, Playlist, playlist_video
from django.core.files.storage import FileSystemStorage
import os
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.generic import View
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .token_generator import generate_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login, authenticate
from django.http import HttpResponse,JsonResponse
from django.conf import settings
import threading
from django.core.exceptions import ObjectDoesNotExist
import random
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    return render(request, 'products/home.html');


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        bval = False
        if len(name) < 4:
            messages.add_message(request, messages.ERROR, 'your name must have lenght>4')
            bval = True
        if (password != cpassword):
            messages.add_message(request, messages.ERROR, 'password do not match!')
            bval = True
        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'passwword at least 6 length!')
            bval = True
        try:
            if User.object.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email is taken!')
                bval = True
        except Exception as identifier:
            pass

        if bval:
            return render(request, 'products/signup.html')
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.is_active = False
        user.save()
        email_subject = 'Activate Your Account'
        current_site = get_current_site(request)
        message = render_to_string('products/activate.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),
        })
        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )
        EmailThread(email_message).start()
        messages.add_message(request, messages.SUCCESS, 'account created succesfully')
        return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
    else:
        return render(request, 'products/signup.html')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'account activated successfully')
            return redirect('login')
        return render(request, 'products/signup.html', status=401)


class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'email or password is incorrect !')
            return render(request, 'products/login.html')
    else:
        return render(request, 'products/login.html')



def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')


#View for index.html
#fetching all the video object and displaying it



class HomeView(View):
    template_name = 'products/index.html'

    def get(self, request):
        most_recent_videos = Video.objects.order_by('-upload_date')
        return render(request, self.template_name, {'menu_active_item': 'home', 'most_recent_videos': most_recent_videos})



class PlaylistView(View):
    template_name = 'products/playlist.html'

    def get(self, request):
        playlist_list = Playlist.objects.order_by('-upload_date')
        return render(request, self.template_name, {'playlist_list': playlist_list})


class SearchView(View):
    template_name = 'products/search.html'
    def post(self, request):
        text = self.request.POST.get('search_text')
        q1 = Video.objects.filter(title__contains = text)
        q2 = Video.objects.filter(category__contains = text)
        q4 = Video.objects.filter(description__contains=text)
        tag = Tag.objects.filter(title__contains = text)
        tagid = []
        for x in tag:
            tagid.append(x.video.id)
        q3 = Video.objects.filter(id__in = tagid)
        print(q2)
        print(q3)
        q2 = (q1 | q2 | q3 | q4).distinct()
        return render(request, self.template_name, {'menu_active_item': 'home', 'most_recent_videos': q2})


class FavouriteVideo(View):
    template_name = 'products/favourite.html'

    def get(self, request):
        favourite_videos = Favourite.objects.filter(user=request.user).filter(favourite=True)
        return render(request, self.template_name,
                      {'favourite_videos': favourite_videos , 'playlist_id' : 0})


class HistoryVideo(View):
    template_name = 'products/history.html'

    def get(self, request):
        history_videos = History.objects.filter(user=request.user).order_by('-dateTime')[:15]
        return render(request, self.template_name,
                      {'history_videos': history_videos,'playlist_id': 0})




#View to view Video

class VideoView(View):
    template_name = 'products/video.html'

    def get(self, request, id, id1):

        if id1 == 0:

            next_video = []
            next_v = Video.objects.filter(id__gt=id).order_by('upload_date')
            for x in next_v:
                next_video.append(x)
            next_v = Video.objects.filter(id__lte=id).order_by('upload_date')
            for x in next_v:
                next_video.append(x)
            context = {'next_video' : next_video[0].id}

            previous_video = []
            previous_v = Video.objects.filter(id__lt=id).order_by('-upload_date')
            for x in previous_v:
                previous_video.append(x)
            previous_v = Video.objects.filter(id__gte=id).order_by('-upload_date')
            for x in previous_v:
                previous_video.append(x)
            context['previous_video'] = previous_video[0].id
            context['most_recent_videos'] = next_video
        else:
            playlist = playlist_video.objects.filter(playlist_id = id1).order_by('video_id')
            next_video = []
            for x in playlist:
                v = Video.objects.get(id=x.video_id)
                next_video.append(v)

            if id == 0:
                id = next_video[0].id
                next_video.append(next_video[0])
                next_video.pop(0)
            else:
                st = []
                while next_video[0].id != id:
                    st.append(next_video[0])
                    next_video.pop(0)
                st.append(next_video[0])
                next_video.pop(0)
                for x in st:
                    next_video.append(x)
                print(next_video)
            context = {'next_video': next_video[0].id}
            if len(next_video)==1:
                context['previous_video'] = next_video[0].id
            else:
                context['previous_video'] = next_video[len(next_video)-2].id
            context['most_recent_videos'] = next_video

        video_by_id = get_object_or_404(Video, pk=id)
        video_by_id.views = video_by_id.views + 1
        video_by_id.save()

        context['video'] = video_by_id
        comments = Comment.objects.filter(video__id=id).order_by('-datetime')
        context['comments'] = comments
        video = Video.objects.get(id=id)
        tag = Tag.objects.filter(video=id)
        context['tag'] = tag

        try:
            go = Like.objects.get(video_id=id, user=request.user)
        except ObjectDoesNotExist:
            liked_now = Like(like=0, user=request.user, video=video)
            liked_now.save()
            go = Like.objects.get(video_id=id, user=request.user)

        try:
            fav = Favourite.objects.get(video_id=id, user=request.user)
        except ObjectDoesNotExist:
            fav_add = Favourite(user=request.user, video=video)
            fav_add.save()
            fav = Favourite.objects.get(video=video, user=request.user)

        try:
            history = History.objects.get(video_id=id, user=request.user)
            history.dateTime = datetime.now()
            if history.duration_time - history.pause_time < 5.0:
                if history.duration_time > history.pause_time:
                    history.pause_time = 0
                else:
                    history.pause_time = 0
                    history.duration_time = 1

            history.save()
        except ObjectDoesNotExist:
            add_history = History(user=request.user, video=video)
            add_history.save()
            history = History.objects.get(video=video, user=request.user)

        context['history'] = history
        context['like_dislike'] = go
        context['fav'] = fav
        context['playlist_id'] = id1

        print(context)

        return render(request, self.template_name, context)


def comment(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text',False)
        video_id = request.POST.get('video_id',False)
        print(comment_text)
        print(video_id)
        video = Video.objects.get(id = video_id)
        new_comment = Comment(text = comment_text, user = request.user , video = video)
        new_comment.save()
        comments = Comment.objects.filter(video_id=video_id).order_by('-datetime')
        return JsonResponse({'comments': list(comments.values())})

def delete_comment(request):
    if request.method == 'GET':
        comment_id = request.GET.get('comment_id',False)
        video_id = request.GET.get('video_id', False)
        print(video_id)
        print(comment_id)
        Comment.objects.filter(pk = comment_id).delete();
        comments = Comment.objects.filter(video_id=video_id).order_by('-datetime')
        return JsonResponse({'comments': list(comments.values())})



def edit_comment(request):
    if request.method == 'GET':
        comment_id = request.GET.get('comment_id',False)
        video_id = request.GET.get('video_id', False)
        text = request.GET.get('text', False)
        print(video_id)
        print(comment_id)
        print(text)
        comment = Comment.objects.get(pk = comment_id)
        comment.text = text
        comment.save()
        comments = Comment.objects.filter(video_id=video_id).order_by('-datetime')
        sol = False
        if request.user.is_staff:
            sol = True

        return JsonResponse({'comments': list(comments.values()), 'sol': sol})




def liked(request):
    if request.method == 'GET':
        video_id = request.GET.get('video_id', False)
        video = Video.objects.get(id = video_id)
        go = Like.objects.get(video=video,user=request.user)
        if go.like == 1:
            go.like = 0
            video.likes = video.likes - 1;
        else:
            if go.like == -1:
                video.dislikes = video.dislikes - 1;
            go.like = 1
            video.likes = video.likes + 1;
        go.save()
        video.save()
        context = {'like': go.like}
        context['total_like'] = video.likes
        context['total_dislike'] = video.dislikes
        return JsonResponse(context)


def disliked(request):
    if request.method == 'GET':
        video_id = request.GET.get('video_id', False)
        video = Video.objects.get(id=video_id)
        go = Like.objects.get(video=video, user=request.user)
        if go.like == -1:
            go.like = 0
            video.dislikes = video.dislikes - 1;
        else:
            if go.like == 1:
                video.likes = video.likes - 1;
            go.like = -1
            video.dislikes = video.dislikes + 1;
        go.save()
        video.save()
        context =   {'dislike': go.like}
        context['total_dislike'] = video.dislikes
        context['total_like'] = video.likes
        return JsonResponse(context)


def favourite(request):
    if request.method == 'GET':
        video_id = request.GET.get('video_id', False)
        video = Video.objects.get(id = video_id)
        fav = Favourite.objects.get(video=video,user=request.user)
        if fav.favourite == False:
            fav.favourite = True
        else:
            fav.favourite = False
        fav.save()
        context = {'fav': fav.favourite}
        return JsonResponse(context)


def comment_list(request):
    video_id = request.POST.get('video_id', False)
    comments = Comment.objects.filter(video_id=2).order_by('-datetime')[:5]
    return JsonResponse({'comments': list(comments.values())})


def new_video(request):
    if request.method=='POST':
        bvl=False
        video=Video()
        video.title =request.POST.get('video_title')
        video.description =request.POST.get('video_description')
        play=request.FILES.get('video_filename')
        img=request.FILES.get('video_thumbtail')
        video.type=request.POST.get('video_type')
        video.category = request.POST.get('video_category')
        url=request.POST.get('video_link')
        if request.POST.get('video_type')!='upload from system' and len(url)==0:
            bvl=True
            messages.add_message(request, messages.ERROR, 'url field cannot be empty !')
        if request.POST.get('video_type')=='upload from system' and play==None:
            bvl=True
            messages.add_message(request, messages.ERROR, 'filename cannot be empty !')
        if img==None:
            bvl=True
            messages.add_message(request, messages.ERROR, 'add a valid thumbtail !')
        if bvl:
            return redirect('new_video')

        video.filename=play
        video.thumbtail=img
        video.link=request.POST.get('video_link')
        video.subtitle=request.POST.get('video_subtitle')
        if request.POST.get('video_premium'):
            video.premium=True
        else:
            video.premium=False
        video.upload_date=timezone.datetime.now()
        video.save()
        return HttpResponseRedirect('video/{}/0'.format(str(video.id)))

    return render(request,'products/new_video.html')


def add_tag(request):
    if request.method == 'POST':
        video_id = request.POST.get('video_id', False)
        video = Video.objects.get(id=video_id)
        tag = Tag()
        tag.title = request.POST.get('tag_info')
        tag.video = video
        tag.save()
        return HttpResponseRedirect('video/{}'.format(str(video.id)))
    else:
        return render(request, 'products/index.html')


def notification(request):
    items = Flag.objects.all().order_by('-date')
    return render(request, 'products/notification.html', {'items': items})


def delete_video(request):
    if request.method == 'POST':
        id = request.POST.get('idvideo')
        video_to_delete = Video.objects.get(id=id)
        video_to_delete.filename.delete()
        video_to_delete.delete()
        messages.success(request, 'video deleated successfully')
        return redirect('home_view')


def ignore_goto_video(request):
    if request.method == 'GET':
        id = request.GET.get('notification_v_id', False)
        flag = Flag.objects.get(id=id)

        flag.user_response = True
        flag.save()
        print(flag.reason)
        print('hello world')
        redirect = 'video/{}/0'.format(str(flag.video.id))

        return JsonResponse({'id': flag.video.id, 'redirect': redirect})


def ignore_v(request):
    if request.method == 'GET':
        id = request.GET.get('notification_v_id', False)
        flag = Flag.objects.get(id=id)
        flag.user_response = True
        flag.save()
        flgs = Flag.objects.all().order_by('-date')
        flg = list(flgs.values())
        return JsonResponse({'flg': flg})

def save_video_time(request):
    if request.method == 'GET':
        time = request.GET.get('time', False)
        end = request.GET.get('end', False)
        id = request.GET.get('video_id', False)
        history = History.objects.get(video_id=id, user=request.user)
        history.pause_time = time
        history.duration_time = end
        history.save()
        return JsonResponse({'TEXT':"sAVED"})

def add_comment_flag(request):
    if request.method == 'GET':
        comment_id = request.GET.get('comment_id',False)
        video_id = request.GET.get('video_id', False)
        text = request.GET.get('text', False)
        flag=Flag()
        flag.video=Video.objects.get(id=video_id)
        comment = Comment.objects.get(pk = comment_id)
        comment_text = comment.text
        flag.comment=comment
        flag.user=request.user
        flag.reason='(reason to flag :'+text+')'+'--Comment :'+comment_text
        flag.date=timezone.datetime.now()
        flag.user_response=False
        flag.name=request.user.first_name
        flag.save()
        return JsonResponse({})

def delete_comm(request):
    if request.method == 'GET':
        flag_id = request.GET.get('notf_id',False)
        flag=Flag.objects.get(id=flag_id)
        flag.user_response=True
        comment=flag.comment
        comment.delete()
        return JsonResponse({})


def add_video_flag(request):
    if request.method == 'GET':
        video_id = request.GET.get('video_id', False)
        text = request.GET.get('text', False)
        flag=Flag()
        flag.video=Video.objects.get(id=video_id)
        flag.user=request.user
        flag.reason=text
        flag.date=timezone.datetime.now()
        flag.user_response=False
        flag.name=request.user.first_name
        flag.save()
        return JsonResponse({})


def create_playlist(request):
    context={"new_playlist" : False}
    videos = Video.objects.order_by('-upload_date')
    context["videos"] = videos
    if request.method == 'POST':
        bvl = False
        playlist = Playlist()
        playlist.title = request.POST.get('playlist_title')
        playlist.description = request.POST.get('playlist_description')
        img = request.FILES.get('playlist_thumbtail')
        if img == None:
            bvl = True
            messages.add_message(request, messages.ERROR, 'add a valid thumbtail')
        if bvl:
            return render(request, 'products/create_playlist.html',context)
        playlist.thumbtail = img
        if request.POST.get('playlist_premium'):
            playlist.premium = True
        else:
            playlist.premium = False
        playlist.upload_date = timezone.datetime.now()
        playlist.save()
        context["new_playlist"] = True
        context["playlist_id"]=playlist.id
        return render(request, 'products/create_playlist.html' , context)
    return render(request, 'products/create_playlist.html',context)

def add_to_playlist(request):
    if request.method == "GET":
        video_id = request.GET.get('video_id', False)
        video = Video.objects.get(pk=video_id)
        playlist_id = request.GET.get('playlist_id', False)
        playlist = Playlist.objects.get(pk = playlist_id)
        try:
            pv = playlist_video.objects.get(video = video, playlist = playlist)
        except ObjectDoesNotExist:
            pv = playlist_video(video=video,datetime=video.upload_date,name = video.title, playlist=playlist)
            pv.save()
        pv = playlist_video.objects.filter(playlist = playlist)
        return JsonResponse({"pv":list(pv.values())})

