from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from xrp.course.models import Grade
from xrp.userprofile.forms import UserForm, UserProfileForm
from xrp.userprofile.models import UserProfile
from xrp.quiz.models import MCQuestionAttempt


def index (request, template_name):
    """
    Landing page for anonymous user
    Sign in and Sign up functionality handled
    """
    if request.user.is_authenticated():
        try:
            userprofile = UserProfile.objects.get(user = request.user)
        except UserProfile.DoesNotExist:
            return HttpResponseRedirect(reverse('registration_register'))
        grades = Grade.objects.filter(student = userprofile.user, course__start_date__lte = datetime.now()).order_by('-date_added')
        try:
            course_id = MCQuestionAttempt.objects.filter(student = request.user)[0].mcquestion.quiz.course.id
        except IndexError:
            course_id = None
        return render_to_response('faucet/faucet.html', context_instance=RequestContext(request, {'userprofile': userprofile, 'grades': grades, 'course': course_id}))
    else:
        if request.POST:
            form_type = request.POST['form']
            if form_type == 'form1':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        try:
                            userprofile = UserProfile.objects.get(user = user)
                        except UserProfile.DoesNotExist:
                            return HttpResponseRedirect(reverse('registration_register'))
                        grades = Grade.objects.filter(student = userprofile.user, course__start_date__lte = datetime.now()).order_by('-date_added')
                        return render_to_response('faucet/faucet.html', context_instance=RequestContext(request, {'userprofile': userprofile, 'grades': grades}))
                else:
                    form = AuthenticationForm(None, request.POST)
                    return render_to_response('registration/login.html', context_instance=RequestContext(request, {'form': form}))
            if form_type == 'form2':
                form = UserForm(request.POST)
                if form.is_valid():
                    user = User.objects.create_user(**form.cleaned_data)
                    new_user = authenticate(username=request.POST['username'],
                                            password=request.POST['password'])
                    login(request, new_user)
                return HttpResponseRedirect(reverse('registration_register'))
        else:
            form = UserForm()
            return render_to_response(template_name, context_instance=RequestContext(request, {'form': form}))
    return HttpResponseRedirect(reverse('registration_register'))

@login_required
def registration (request, template_name):
    """
    Show, Create and Edit users profile
    """
    try:
        userprofile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        userprofile = {}

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            if userprofile:
                if request.FILES and request.FILES['avatar'] is not None:
                    userprofile.avatar = request.FILES['avatar']
                userprofile.address = request.POST['address']
                userprofile.country = request.POST['country']
                userprofile.city = request.POST['city']
                userprofile.phone = request.POST['phone']
                if request.POST['date_of_birth']:
                    userprofile.date_of_birth = request.POST['date_of_birth']
                userprofile.website = request.POST['website']
                userprofile.save()
            else:
                obj = form.save(commit = False)
                obj.user = request.user
                obj.save()
            grades = Grade.objects.filter(student = request.user, course__start_date__lte = datetime.now()).order_by('-date_added')
            return render_to_response('faucet/faucet.html', context_instance=RequestContext(request, {'userprofile': userprofile, 'grades': grades}))
        else:
            return render_to_response(template_name, context_instance=RequestContext(request, {'form': form}))
    else:
        if userprofile:
            data = {
                "avatar": userprofile.avatar,
                "address": userprofile.address,
                "country": userprofile.country,
                "city": userprofile.city,
                "phone": userprofile.phone,
                "date_of_birth": userprofile.date_of_birth,
                "website": userprofile.website,
            }
            form = UserProfileForm(data)
        else:
            form = UserProfileForm()

        return render_to_response(template_name, context_instance=RequestContext(request, {'form': form}))
