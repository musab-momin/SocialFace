from email import message
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib import auth
from socialmedia.models import Profile, User, Post, LikePost, FollowingCount, Comment
from django.contrib.auth.decorators import login_required
import calendar
from itertools import chain
from django.http import JsonResponse
from django.core import serializers
import json

# Create your views here.
@login_required(login_url='/signin')
def index(request):
    context = {'title':'SocialFace'}
    logedin_user = Profile.objects.get(user = request.user)
    context['user'] = logedin_user
    
    #print(profile_images)

    #creating user feed 
    following_users_lst = []    
    feed = []

    #fetching all the users whom logedin user is following
    for user in FollowingCount.objects.filter(following_user_id=request.user.id):
        following_users_lst.append(user.user.id)

    #fetching post according user of following_users_lst
    for user in following_users_lst:
        feed_lst = Post.objects.filter(user=User.objects.get(id=user))
        feed.append(feed_lst)

    #using chain method convert query_set into normal python list 
    feed_lsts = list(chain(*feed))

    profile_images = []
    for post in feed_lsts:
        profile_images.append({'id':post.user.id,'profile_pic': Profile.objects.get(user=post.user).profile_pic})

    context['post_lst'] = feed_lsts
    context['profile_pics'] = profile_images
    

    #user suggestions not recommended approach
    context['suggestions'] = [user for user in Profile.objects.all().order_by('?')[:5] if user.user != request.user ]
    return render(request, 'socialmedia/index.html', context)


def signin(request):
    context = {
        'title': 'Login'
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        print(f'''
            name of the user trying to signin: {name}
            password of the user trying to signin: {password}
        ''')
        if User.objects.filter(username=name).exists():
            user = auth.authenticate(username = name, password = password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Bad Credentials')
        else:
            messages.info(request, 'Username doesnot exists')

    return render(request, 'socialmedia/signin.html', context)
    

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        bio = request.POST.get('bio')
        image = request.FILES.get('profile-pic')

        print(f'''
          Name of the user is : {name}
          Email of the user is : {email}
          Password of the user is : {password}
          Dob of the user is : {dob}
          Gender of the user is : {gender}
          Bio of the user is : {bio}
          Image of ther user is : {image}
        ''')
        #doing some validations
        if User.objects.filter(email = email).exists():
            messages.info(request, 'Email is already registered')
            return redirect('/signup')
        elif User.objects.filter(username = name).exists():
            messages.info(request, 'This user name is not available')
            return redirect('/signup')
        #saving user to db
        user = User.objects.create_user(username = name, email = email, password = password)
        user.save()
        if image == None:
            profile = Profile(user = user, id_user = user.id, dob = dob, gender = gender, bio = bio, profile_pic= None )
        else:
            profile = Profile(user = user, id_user = user.id, dob = dob, gender = gender, bio = bio, profile_pic=image)
        profile.save()
        messages.info(request, 'You are successfully registered!')
        return redirect('/signup')
        
    context = {
        'title': 'Signup'
    }
    return render(request, 'socialmedia/signup.html', context)


@login_required(login_url='/signin')
def signout(request):
    auth.logout(request)
    return redirect('/signin')


@login_required(login_url='/signin')
def explore(request):
    all_profiles = list(Profile.objects.all().values())
    
    for profile in all_profiles:
        current_user = User.objects.get(id = profile['user_id'])
        profile['username'] = current_user.username
        profile['post_count'] = len(Post.objects.filter(user=current_user))
        profile['follower_count'] = len(FollowingCount.objects.filter(user=current_user))
        profile['following_count'] = len(FollowingCount.objects.filter(following_user_id=profile['user_id']))
    
    print(all_profiles[0])
    
    context = {
        'title': 'Explore',
        'all_profiles': all_profiles,
        'user': Profile.objects.get(user = request.user)
    }
    return render(request, 'socialmedia/explore.html', context)


@login_required(login_url='/signin')
def get_profile(request):
    logedin_user = Profile.objects.get(user = request.user)
    posts = Post.objects.filter(user=request.user)
    followers_obj = FollowingCount.objects.filter(user=request.user)
    following_obj = FollowingCount.objects.filter(following_user_id=request.user.id)
    context = {
        'title': 'Profile', 
        'active_user': logedin_user,
        'profile_image_url': logedin_user.profile_pic,
        'posts': posts,
        'posts_count': len(posts),
        'is_allowed_to_post': True,
        'followers_count': len(followers_obj),
        'following_count': len(following_obj)
        }
    return render(request, 'socialmedia/profile.html', context)


@login_required(login_url='/signin')
def get_profile_by_id(request, id):
    context ={
        'title': 'Profile',
        'logedin_user': Profile.objects.get(user = request.user),
        'profile_image_url': Profile.objects.get(user=request.user).profile_pic,
    }
    if Profile.objects.filter(user__id = id).exists():
        active_profile_user = Profile.objects.get(user__id = id)
        posts = Post.objects.filter(user= User.objects.get(id=active_profile_user.id_user) )
        followers_obj = FollowingCount.objects.filter(user=User.objects.get(id = id))
        following_obj = FollowingCount.objects.filter(following_user_id=User.objects.get(id = id).id)
        is_already_following = False


        for follower in followers_obj:
            if follower.following_user_id == request.user.id:
                is_already_following = True
                break;
        
        

        context['active_user'] = active_profile_user
        context['posts'] = posts
        context['posts_count'] = len(posts)
        context['is_allowed_to_post'] = True if id == request.user.id else False
        context['is_already_following'] = is_already_following
        context['followers_count'] = len(followers_obj)
        context['following_count'] = len(following_obj)
        return render(request, 'socialmedia/profile.html', context)
    return redirect('/')


@login_required(login_url='/signin')
def update_profile(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    dob = request.POST.get('dob')
    gender = request.POST.get('gender')
    bio = request.POST.get('bio')
    image = request.FILES.get('profile-pic')

    logedin_user = Profile.objects.get(user = request.user)

    if logedin_user.user.username != name:
        if User.objects.filter(username=name).exists():
            messages.info(request, 'Name is not available')
        else:
            #setting the new name
            logedin_user.user.username = name
    
    if logedin_user.user.email != email:
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email is already registered')
        else:
            #setting the new email
            logedin_user.user.email = email
    
    if dob != "":
        logedin_user.dob = dob    

    if logedin_user.gender != gender:
        logedin_user.gender = gender

    if logedin_user.bio != bio:
        logedin_user.bio = bio

    if image != None:
        logedin_user.profile_pic = image

    print(f'''
        {logedin_user.user.id}
        {logedin_user.user.username}
        {logedin_user.user.email}
        {logedin_user.id_user}
        {dob}
        {gender}
        {bio.strip()}
        {image}
    ''')
    #updating auth user table 
    logedin_user.user.save()
    #updating in profile table
    logedin_user.save()
    return redirect('/profile')


@login_required(login_url='/signin')
def make_post(request):
    logedin_user = Profile.objects.get(user = request.user)
    post_image = request.FILES.get('post_image')
    caption = request.POST.get('caption')
   
    obj = Post(user = request.user, post_image=post_image, caption=caption)
    print(f'''
    id: {obj.id}
    Image name: {post_image}
    caption is: {caption}
    ''')
    obj.save()
    return redirect('/profile')


def like_post(request, id):
    liked_post_obj = LikePost.objects.filter(username=request.user.username, post_id=id).first()
    print(f'''
        {liked_post_obj}
    ''')
    
    if liked_post_obj == None:
        like_obj = LikePost.objects.create(username=request.user.username, post_id=id)
        like_obj.save()
        post_which_we_are_liking = Post.objects.get(id = id)
        post_which_we_are_liking.likes = post_which_we_are_liking.likes + 1
        post_which_we_are_liking.save()
    else:
        like_obj = LikePost.objects.get(username=request.user.username, post_id=id)
        like_obj.delete()
        post_which_we_are_liking = Post.objects.get(id = id)
        post_which_we_are_liking.likes = post_which_we_are_liking.likes - 1
        post_which_we_are_liking.save()

    return redirect('/')


@login_required(login_url='/signup')
def handle_followers(request, logedin_user_id, follower_id):
    try:
        follower = User.objects.filter(id=logedin_user_id);
        user_gets_follow = User.objects.filter(id = follower_id)
        flag = True
        print(f'''
            Follower obj: {follower}
            user gets followed: {user_gets_follow}
        '''
        )

        if follower.exists() and user_gets_follow.exists():
            #jis user ki profile open ki hue hai us ke followers 
            followers_of_active_user = FollowingCount.objects.filter(user= User.objects.get(id = follower_id) )

            for user in followers_of_active_user:
                if user.following_user_id == request.user.id:
                    user.delete()
                    flag = False
                    break

            if(flag):
                obj = FollowingCount(user=user_gets_follow.first(), following_user_id= follower.first().id)
                obj.save()
            url = f'/profile/{ user_gets_follow.first().id }'
            return redirect(url)
    except Exception as err:
        print('Something went wrong...')
        print(err)
        return redirect("/")

    return redirect("/")

@login_required(login_url='signup')
def do_search(request):
    search_txt = request.POST.get('searched_txt')
    print(f'''
    This is the searched text : { search_txt }
    
    ''')
    try:
        searched_user =  User.objects.filter(username = search_txt)
        if searched_user.exists():
            url = f'/profile/{ searched_user.first().id }'
            return redirect(url)
        else:
            print('user profile not found')
            messages.info(request, 'User not found!')
            redirect("/")
    except Exception as exc:
        print(exc)
    return redirect("/")


@login_required(login_url='signup')
def search_suggestions(request, search_text):
    try:
        user_lst = User.objects.filter(username__startswith=search_text)
        user_lst = serializers.serialize('json', user_lst)
        return JsonResponse(user_lst, safe=False)
    except Exception as ex:
        print(ex)
        res = serializers.serialize('json', {'status':501, 'mssg': 'InternalServerError'})
    return JsonResponse(res, safe=False)


@login_required(login_url='signup')
def refresh_suggestions(request):
    suggestions_lst = Profile.objects.all().order_by('?')[:5]
    data = serializers.serialize('json', suggestions_lst)
    print(data)
    return JsonResponse(data, safe=False)


@login_required(login_url='signup')
def make_comment(request):
    comment_text = request.POST.get('comment')
    post_id = request.POST.get('post_id')
    print(f'''
        This is comment : {comment_text}
        This is post on which user did comment: { post_id }
    ''')
    try:
        commented_post = Post.objects.get(id = post_id)
        comment_obj = Comment.objects.create(commented_by=request.user.username, content=comment_text, post=commented_post)
        comment_obj.save()
    except Exception as ex:
        print(ex)


    return redirect("/")


@login_required(login_url='signup')
def fetch_comment(request, id):
    
    try:
        comments_of_active_post = Comment.objects.filter(post__id=id)
        comments_of_active_post = serializers.serialize('json', comments_of_active_post)
          # json_obj = json.loads(comments_of_active_post)   
        # for single_comment in json_obj:
        #     name_of_commented_user = single_comment['fields']['commented_by']
        #     commented_user = User.objects.filter(username = name_of_commented_user).first()
        #     profile_pic_of_commented_user = Profile.objects.filter(id_user=commented_user.id).first()
        #     print(type(json.loads(single_comment['fields']['commented_by'])))

        # print(json_obj[0])
        # print(comments_of_active_post)
        return JsonResponse(comments_of_active_post, safe=False)    
    except Exception as ex:
        return JsonResponse({'mssg': 'something went wrong...'})  




      