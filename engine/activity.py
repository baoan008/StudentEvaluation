#encoding:utf-8
import traceback
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from engine.forms import BehaviorForm, DevelopmentForm
from engine.models import Behavior, LEVEL_CHOICES, Development, DEVELOPMENT_LEVEL_CHOICES
from engine.utils import get_datatables_records


@login_required
def behavior(request):
    username = request.user.username
    return render_to_response('activity/behavior.html', {
        'title': u'日常行为活动',
        'username': username
    }, context_instance=RequestContext(request))

@login_required
def addbehavior(request):
    username = request.user.username
    if request.method == 'POST':
        form = BehaviorForm(data=request.POST)
        if form.is_valid():
            form.save()
            success = True
            successinfo = u'添加'
            return render_to_response('activity/behavior.html', {
                'title': u'日常行为管理活动',
                'form': form,
                'successinfo': successinfo,
                'success': success,
                'username': username
            }, context_instance=RequestContext(request))
        else:
            return render_to_response('activity/behavior.html', {
                'title': u'日常行为管理活动',
                'form': form,
                'username': username
            }, context_instance=RequestContext(request))
    return HttpResponseRedirect('/manage/behavior/')

@login_required
def deletebehavior(request):
    username = request.user.username
    if request.method == 'POST':
        try:
            behavior_id = request.POST.get('id')
            try:
                delbehavior = Behavior.objects.get(id=behavior_id)
                delbehavior.delete()
                success = True
                successinfo = u'删除'
                return render_to_response('activity/behavior.html', {
                    'title': u'日常行为活动管理',
                    'successinfo': successinfo,
                    'success': success
                }, context_instance=RequestContext(request))
            except Behavior.DoesNotExist, e:
                traceback.print_stack()
                traceback.print_exc()
                print e
        except Exception, e:
            traceback.print_stack()
            traceback.print_exc()
            print e
    return HttpResponseRedirect('/manage/behavior/')

@login_required
def editbehavior(request):
    username = request.user.username
    if request.method == 'POST':
        form = BehaviorForm(data=request.POST)
        if form.is_valid():
            form.update()
            success = True
            successinfo = u'修改'
            return render_to_response('activity/behavior.html', {
                'title': u'日常行为活动管理',
                'form': form,
                'success': success,
                'successinfo': successinfo,
                'username': username
            }, context_instance=RequestContext(request))
        else:
            return render_to_response('activity/behavior.html', {
                'title': u'日常行为活动管理',
                'username': username,
                'form': form
            }, context_instace=RequestContext(request))
    return HttpResponseRedirect('/manage/behavior/')

@login_required
def adddevelopment(request):
    username = request.user.username
    if request.method == 'POST':
        form = DevelopmentForm(data=request.POST)
        if form.is_valid():
            form.save()
            success = True
            successinfo = u'添加'
            return render_to_response('activity/development.html', {
                'title': u'个性发展活动管理',
                'form': form,
                'successinfo': successinfo,
                'success': success,
                'username': username
            }, context_instance=RequestContext(request))
        else:
            return render_to_response('activity/development.html', {
                'title': u'个性发展活动管理',
                'form': form,
                'username': username
            }, context_instance=RequestContext(request))

    return HttpResponseRedirect('/manage/development/')

@login_required
def ajaxdevelopment(request):
    developments = Development.objects.all().reverse()
    columnIndexNameMap = {
        0: 'id',
        1: 'parent',
        2: 'name'
    }
    try:
        aaData, sEcho, iTotalRecords, iTotalDisplayRecords, sColumns = get_datatables_records(request, developments, columnIndexNameMap,
                                                                                              None, {}, False, {}, {})
    except Exception, e:
        traceback.print_stack()
        traceback.print_exc()
        print e
        aaData, sEcho, iTotalRecords, iTotalDisplayRecords, sColumns = [], 1, 0, 0, ','.join(columnIndexNameMap.values())

    for i in aaData:
        i[1] = dict(DEVELOPMENT_LEVEL_CHOICES)[i[1]]
    response_dict = {}
    response_dict.update({'aaData': aaData})
    response_dict.update({
        'sEcho': sEcho,
        'iTotalRecords': iTotalRecords,
        'iTotalDisplayRecords': iTotalDisplayRecords,
        'sColumns': sColumns
    })
    response = HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')
    add_never_cache_headers(response)
    return response

@login_required
def development(request):
    username = request.user.username
    return render_to_response('activity/development.html', {
        'title': u'个性发展活动管理',
        'username': username
    }, context_instance=RequestContext(request))

@login_required
def editdevelopment(request):
    username = request.user.username
    if request.method == 'POST':
        form = DevelopmentForm(data=request.POST)
        if form.is_valid():
            form.update()
            success = True
            successinfo = u'修改'
            return render_to_response('activity/development.html', {
                "title": u'个性发展活动管理',
                'form': form,
                'successinfo': successinfo,
                'success': success,
                'username': username
            }, context_instance = RequestContext(request))
        else:
            return render_to_response('activity/development.html', {
                "title": u'个性发展活动管理',
                'form': form,
                'username': username}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/manage/development/')

@login_required
def deletedevelopment(request):
    username = request.user.username
    try:
        development_id = request.POST.get('id')
        try:
            deldevelopment = Development.objects.get(id=development_id)
            deldevelopment.delete()
            success = True
            successinfo = u'删除'
            return render_to_response('activity/development.html', {
                "title": u'个性发展活动管理',
                'successinfo': successinfo,
                'success': success,
                'username': username
            }, context_instance = RequestContext(request))
        except Behavior.DoesNotExist:
            traceback.print_stack()
            traceback.print_exc()
            print e
    except Exception,e:
        traceback.print_stack()
        traceback.print_exc()
        print e
    return HttpResponseRedirect('/manage/development/')

@login_required
def ajaxbehavior(request):
    behaviors = Behavior.objects.all().reverse()
    columnIndexNameMap = {
        0: 'id',
        1: 'actlevel',
        2: 'name',
    }
    try:
        aaData, sEcho, iTotalRecords, iTotalDisplayRecords, sColumns = get_datatables_records(request,
                                                                                              behaviors,
                                                                                              columnIndexNameMap,
                                                                                              None, {}, False, {}, {})
    except Exception, e:
        traceback.print_stack()
        traceback.print_exc()
        print e
        aaData, sEcho, iTotalRecords, iTotalDisplayRecords, sColumns = [], 1, 0, 0, ','.join(columnIndexNameMap.values())

    for i in aaData:
        i[1] = dict(LEVEL_CHOICES)[i[1]]
    response_dict = {}
    response_dict.update({'aaData': aaData})
    response_dict.update({
        'sEcho': sEcho,
        'iTotalRecords': iTotalRecords,
        'iTotalDisplayRecords': iTotalDisplayRecords,
        'sColumns': sColumns
    })
    response = HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')
    add_never_cache_headers(response)
    return response
