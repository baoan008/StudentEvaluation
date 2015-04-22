#encoding:utf-8
import traceback
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from models import Student, SEX_CHOICES, User, Class
from utils import get_datatables_records
from forms import StudentForm

@login_required
def index(request):
    username = request.user.username
    return render_to_response('student/student.html', {
        "title": u'同学管理',
        "username": username,
    }, context_instance=RequestContext(request))

@login_required
def studentprofile(request):
    username = request.user.username
    student = request.user.student
    return render_to_response('student/profile.html', {
        'title': u'学生信息',
        'studentid': username,
        'realname': student.realname,
        'sex': dict(SEX_CHOICES)[student.sex],
        'class': student.theclass.classname,
        'username': username
    }, context_instance=RequestContext(request))

@login_required
def initstudent(request):
    username = request.user.username
    if request.method == 'POST':
        try:
            student_id = request.POST.get('id')
            try:
                initstudent = Student.objects.get(id=student_id)
                user = initstudent.user
                user.set_password('000000')
                user.save()
                success = True
                successinfo = u'密码已初始化'
                return render_to_response('student/student.html', {
                    'title': u'学生管理',
                    'username': username,
                    'success': success,
                    'successinfo': successinfo
                }, context_instance=RequestContext(request))
            except Student.DoesNotExit:
                traceback.print_stack()
        except Exception, e:
            traceback.print_stack()
    return HttpResponseRedirect('/manage/student/')

@login_required
def addstudent(request):
    username = request.user.username
    if request.method == 'POST':
        form = StudentForm(data=request.POST)
        if form.is_valid():
            form.save()
            success = True
            successinfo = u'添加'
            return render_to_response('student/student.html', {
                'title': u'学生管理',
                'form': form,
                'successinfo': successinfo,
                'success': success,
                'username': username,
            }, context_instance=RequestContext(request))
        else:
            return render_to_response('student/student.html', {
                'title': u'学生管理',
                'form': form,
                'username': username
            }, context_instance=RequestContext(request))
    return HttpResponseRedirect('/manage/student/')

@login_required
def editstudent(request):
    username = request.user.username
    if request.method == 'POST':
        form = StudentForm(data=request.POST)
        if form.is_valid():
            form.update()
            success = True
            successinfo = u'修改'
            return render_to_response('student/student.html', {
                'title': u'学生管理',
                'form': form,
                'username': username,
                'success': success,
                'successinfo': successinfo
            }, context_instance=RequestContext(request))
        else:
            return render_to_response('student/student.html', {
                'title': u'学生管理',
                'form': form,
                'username': username
            }, context_instance=RequestContext(request))
    return HttpResponseRedirect('/manage/student/')

@login_required
def deletestudent(request):
    username = request.user.username
    if request.method == 'POST':
        try:
            student_id = request.POST.get('id')
            try:
                delstudent = Student.objects.get(id=student_id)
                deluser = delstudent.user
                delstudent.delete()
                deluser.delete()
                success = True
                successinfo = u'删除'
                return render_to_response('student/student.html', {
                    'title': u'学生管理',
                    'successinfo': successinfo,
                    'success': success,
                    'username': username
                }, context_instance=RequestContext(request))
            except Student.DoesNotExist:
                traceback.print_stack()
        except Exception, e:
            traceback.print_stack()
    return HttpResponseRedirect('/manage/student/')

@login_required
def get_students_list(request):
    students = Student.objects.all().reverse()
    columnIndexNameMap = {
        0: 'id',
        1: 'user',
        2: 'realname',
        3: 'sex',
        4: 'theclass',
    }
    columnNameIndexMap = dict([[v,k] for k, v in columnIndexNameMap.items()])
    updatefilter = {
        1: 'user__username',
        4: 'theclass__classid',
    }
    extrafilters = {'sex': SEX_CHOICES}
    updateitems = {
        1: 'user_id',
        4: 'theclass_id',
    }
    try:
        aaData, sEcho, iTotalRecords, iTotalDisplayRecords, sColumns = get_datatables_records(request,
                                                                                              students,
                                                                                              columnIndexNameMap,
                                                                                              None,
                                                                                              extrafilters,
                                                                                              False,
                                                                                              updatefilter,
                                                                                              updateitems)
    except Exception, e:
        traceback.print_stack()
        aaData, sEcho, iTotalRecords, iTotalDisplayRecords, sColumns = \
            [], 1, 0, 0, ','.join(columnIndexNameMap.values())

    for i in aaData:
        i[columnNameIndexMap['sex']] = dict(SEX_CHOICES)[i[columnNameIndexMap['sex']]]
        i[columnNameIndexMap['user']] = User.objects.get(id=i[columnNameIndexMap['user']]).username
        i[columnNameIndexMap['theclass']] = Class.objects.get(id=i[columnNameIndexMap['theclass']]).classid

    response_dict = {}
    response_dict.update({'aaData': aaData})
    response_dict.update({
        'sEcho': sEcho,
        'iTotalRecords': iTotalRecords,
        'iTotalDisplayRecords': iTotalDisplayRecords,
        'sColumns': sColumns
    })
    response = HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')

    #阻止缓存
    add_never_cache_headers(response)
    return response