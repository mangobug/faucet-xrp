import datetime, time

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.utils import simplejson

from xrp.course.forms import AddCourseForm, AddForumForm, AddVideoForm, AddPdfForm
from xrp.course.models import Course, Forum, Grade, UploadedFile
from xrp.institute.models import Institute
from xrp.quiz.models import MCQuestionAttempt, LikertAttempt, xrpEndedAttempt, Quiz

from annoying.decorators import ajax_request
from threadedcomments.models import ThreadedComment


@login_required
def course(request, course_id, template_name):
    """
    Course Page
    """
    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))
    return render_to_response(template_name, context_instance=RequestContext(request, {'course': course}))

@login_required
def all_user_courses(request, template_name):
    """
    Display all courses for a user
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('registration_register'))

    grades = Grade.objects.filter(student = user, course__start_date__lte = datetime.datetime.now()).order_by('-date_added')

    return render_to_response(template_name, context_instance=RequestContext(request, {'grades': grades}))

@login_required
def course_pdf_list(request, course_id, template_name):
    """
    Display list of pdfs against a course
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('registration_register'))

    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))

    pdfs = UploadedFile.objects.filter(file_type = 'PDF', course = course.id)

    return render_to_response(template_name, context_instance=RequestContext(request, {'pdfs': pdfs, 'course': course}))

@login_required
def view_file(request, course_id, pdf_id, template_name):
    """
    Display pdf file
    """
    pdf = UploadedFile.objects.get(id = pdf_id)
    return HttpResponseRedirect(str(pdf.uploads.url))

@login_required
def course_video_list(request, course_id, template_name):
    """
    Display list of videos against a course
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('registration_register'))

    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))

    videos = UploadedFile.objects.filter(file_type = 'VID', course = course.id)
    return render_to_response(template_name, context_instance=RequestContext(request, {'videos': videos, 'course': course}))

@login_required
def view_video_file(request, course_id, video_id, template_name):
    vid = UploadedFile.objects.get(id = video_id)
    return render_to_response(template_name,  context_instance=RequestContext(request, {'vid': vid}))

@login_required
def course_forum_list(request, course_id, template_name):
    """
    Display list of forums against a course
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('registration_register'))

    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        course = None

    forums = Forum.objects.filter(course = course)
    return render_to_response(template_name, context_instance=RequestContext(request, {'forums': forums, 'course': course}))

@login_required
def view_forum(request, course_id, forum_id, template_name):
    """
    Display the forum
    """
    try:
        forum = Forum.objects.get(id = forum_id)
    except Forum.DoesNotExist:
        forum = None
    return render_to_response(template_name, context_instance=RequestContext(request, {'forum': forum}))

@login_required
@ajax_request
def add_comment(request, course_id, forum_id):
    """
    Add a comment in the forum
    """
    if request.is_ajax() and request.POST.get('comment'):
        if request.method == 'POST':
            try:
                user = User.objects.get(username = request.user.username)
            except User.DoesNotExist:
                return HttpResponseRedirect(reverse('registration_register'))
            comment = request.POST.get('comment')

            comment = ThreadedComment.objects.create(comment = comment, user_id = user.id, content_type_id = '21', site_id = '1', object_pk = forum_id, submit_date = datetime.datetime.now())

            date = comment.submit_date.strftime("%b. %d, %Y, %I:%M ")
            if comment.submit_date.strftime('%p') == 'AM':
                date = str(date) + 'a.m.'
            else:
                date = str(date) + 'p.m.'

            if user.get_profile().avatar:
                avatar = str(user.get_profile().avatar.url)
            else:
                avatar = settings.STATIC_URL + "img/blank-avatar-50x50.jpg"

            return HttpResponse(simplejson.dumps({"status": True, "name": user.get_full_name(), "avatar": avatar, "comment": comment.comment, "date": str(date)}), mimetype = 'application/json')
    return HttpResponse(simplejson.dumps({"status": False}))

@login_required
def available_course(request, template_name):
    """
    Display list of courses available to the user
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('registration_register'))

    user_courses = Grade.objects.filter(student = user).values('course')

    list_course_ids = [course['course'] for course in user_courses]
    courses = Course.objects.exclude(id__in=list_course_ids)

    return render_to_response(template_name, context_instance=RequestContext(request, {'courses': courses}))

@login_required
def course_quiz_list(request, course_id, template_name):
    """
    Display list of quizzes against a course
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('registration_register'))

    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))

    mcq = MCQuestionAttempt.objects.filter(student = user).values_list('mcquestion__quiz__id')
    lik = LikertAttempt.objects.filter(student = user).values_list('likert__quiz__id')
    xrpded = xrpEndedAttempt.objects.filter(student = user).values_list('xrpended__quiz__id')

    q_ids = [i[0] for i in mcq] + [i[0] for i in lik] + [i[0] for i in xrpded]
    quizzes = Quiz.objects.filter(course = course.id).exclude(id__in = q_ids)
    return render_to_response(template_name, context_instance=RequestContext(request, {'quizzes': quizzes, 'course': course}))

@login_required
@ajax_request
def add_course(request):
    """
    User can add a course
    """
    if request.is_ajax() and request.POST.get('course_id'):
        if request.method == 'POST':
            try:
                user = User.objects.get(username = request.user.username)
            except User.DoesNotExist:
                return HttpResponseRedirect(reverse('registration_register'))

            course_id = request.POST.get('course_id')

            try:
                course = Course.objects.get(id = course_id)
            except Course.DoesNotExist:
                return HttpResponse(simplejson.dumps({"status": False}))

            grade = Grade.objects.create(student = user, course = course)
            return HttpResponse(simplejson.dumps({"status": True, "course_id": course.id}))
    return HttpResponse(simplejson.dumps({"status": False}))

@login_required
def add_forum(request, course_id, template_name):
    """
    Create a new forum
    """
    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        course = None

    if request.method == 'POST':
        form = AddForumForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            file = request.FILES.get('uploads')
            file_type = file.name.split('.')[-1]
            if file_type == 'pdf':
                file_type = 'PDF'
            else:
                file_type = 'VID'
            uploads = UploadedFile.objects.create(uploader = request.user, course = course, uploads = file, file_type = file_type, title = file.name)
            forum = Forum.objects.create(course = course, user = request.user, uploads = uploads, title = title)
            return render_to_response('course/view_forum.html', context_instance=RequestContext(request, {'forum': forum}))
        else:
            return render_to_response(template_name, context_instance=RequestContext(request, {'form': form, 'course': course, 'course_id': course_id}))
    else:
        form = AddForumForm()
        return render_to_response(template_name, context_instance=RequestContext(request, {'form': form, 'course': course, 'course_id': course_id}))

def add_new_course(request, template_name):
    """
    Create a new Course
    """
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            try:
                institute = Institute.objects.get(id = request.POST.get('institute', ''))
            except Institute.DoesNotExist:
                institute = None
            course, flag = Course.objects.get_or_create(user = request.user, description = request.POST.get('description', ''),
                                institute = institute, title = request.POST.get('title', ''),
                                code = request.POST.get('code', ''))
            if request.POST.get('start_date'):
                course.start_date = request.POST.get('start_date')
            else:
                course.start_date = time.strftime('%Y-%m-%d')
            if request.POST.get('end_date'):
                course.end_date = request.POST.get('end_date')
            course.save()
            if flag:
                Grade.objects.create(student = course.user, course = course)
            return HttpResponseRedirect(reverse('all_user_courses'))
        else:
            return render_to_response(template_name, context_instance=RequestContext(request, {'form': form}))
    else:
        form = AddCourseForm()
        return render_to_response(template_name, context_instance=RequestContext(request, {'form': form}))

@login_required
def add_video(request, course_id, template_name):
    """
    Upload video
    """
    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        course = None

    if request.method == 'POST':
        form = AddVideoForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            file = request.FILES.get('uploads')
            file_type = file.name.split('.')[-1]

            uploads = UploadedFile.objects.create(uploader = request.user, course = course, uploads = file, file_type = 'VID', title = title)

            return render_to_response('course/view_video_file.html', context_instance=RequestContext(request, {'vid': uploads}))
        else:
            return render_to_response(template_name, context_instance=RequestContext(request, {'form': form, 'course': course, 'course_id': course_id}))
    else:
        form = AddVideoForm()
        return render_to_response(template_name, context_instance=RequestContext(request, {'form': form, 'course': course, 'course_id': course_id}))

@login_required
def add_pdf(request, course_id, template_name):
    """
    Upload pdf
    """
    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        course = None

    if request.method == 'POST':
        form = AddPdfForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            file = request.FILES.get('uploads')
            file_type = file.name.split('.')[-1]

            uploads = UploadedFile.objects.create(uploader = request.user, course = course, uploads = file, file_type = 'PDF', title = title)
            return HttpResponseRedirect(reverse('course_pdf_list', kwargs={'course_id': course.id}))
        else:
            return render_to_response(template_name, context_instance=RequestContext(request, {'form': form, 'course': course, 'course_id': course_id}))
    else:
        form = AddPdfForm()
        return render_to_response(template_name, context_instance=RequestContext(request, {'form': form, 'course': course, 'course_id': course_id}))
