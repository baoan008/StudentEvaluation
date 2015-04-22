#encoding:utf-8
import traceback
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from engine.models import Comperformance, Behavior, Development, ComperformanceScore, ComperformancePhysicalScore, ComperformanceBehaviorScore, Grade, ComperformanceDevelopmentScore
from engine.utils import get_datatables_records
from forms import Comperformance_SetupForm


@login_required
def comperformance_setup(request):
    username = request.user.username
    return render_to_response('comperformance/comperformance_setup.html', {
        'title': u'综合测评设置',
        'username': username
    }, context_instance=RequestContext(request))

@login_required
def addcomperformance_setup(request):
    username = request.user.username
    if request.method == 'POST':
        form = Comperformance_SetupForm(data=request.POST)
        if form.is_valid():
            form.save()
            success = True
            successinfo = u'添加'
            return render_to_response('comperformance/comperformance_setup.html', {
                'title': u'综合测评设置',
                'username': username,
                'success': success,
                'successinfo': successinfo,
                'form': form
            }, context_instance=RequestContext(request))
        else:
            return render_to_response('comperformance/comperformance_setup.html', {
                'title': u'综合测评设置',
                'username': username,
                'form': form
            }, context_instance=RequestContext(request))
    return HttpResponseRedirect('/manage/comperformance_setup/')

@login_required
def editcomperformance_setup(request):
    username = request.user.username
    if request.method == 'POST':
        form = Comperformance_SetupForm(data=request.POST)
        if form.is_valid():
            success = True
            successinfo = u'编辑'
            return render_to_response('comperformance/comperformance_setup.html', {
                'title': u'综合测评成绩管理',
                'form': form,
                'success': success,
                'successinfo': successinfo,
                'username': username
            }, context_instance=RequestContext(request))
        else:
            return render_to_response('comperformance/comperformance_setup.html', {
                'title': u'综合测评成绩管理',
                'form': form,
                'username': username
            }, context_instance=RequestContext(request))
    return HttpResponseRedirect('/manage/comperformance_setup/')

@login_required
def deletecomperformance_setup(request):
    username = request.user.username
    if request.method == 'POST':
        try:
            comperformance_setup_id = request.POST.get('id')
            try:
                delcomperformance_setup_id = Comperformance.objects.get(id=comperformance_setup_id)
                deletecomperformance_setup.delete()
                success = True
                successinfo = u'删除'
                return render_to_response('comperformance/comperformance_setup.html', {
                    'title': u'综合成绩设置',
                    'success': success,
                    'successinfo': successinfo,
                    'username': username
                }, context_instance=RequestContext(request))
            except Comperformance.DoesNotExist, e:
                traceback.print_stack()
                traceback.print_exc()
                print e
        except Exception, e:
            traceback.print_stack()
            traceback.print_exc()
            print e
    return HttpResponseRedirect('/manage/comperformance_setup/')


@login_required
def ajaxcomperformance_setup(request):
    comperformance = Comperformance.objects.all().order_by('term')
    columnIndexNameMap = {
        0: 'id',
        1: 'term',
        2: 'moral',
        3: 'behaviorup',
        4: 'physical',
        5: 'excellent',
        6: 'good',
        7: 'ordinary',
        8: 'development',
        9: 'behavior',
    }
    try:
        aaData, sEcho, iTotalRecords, iTotalDisplayRecords, sColumns = get_datatables_records(request, comperformance,
                                                                                              columnIndexNameMap,
                                                                                              None, {}, False, {}, {})
    except Exception, e:
        traceback.print_stack()
        traceback.print_exc()
        print e
        aaData, sEcho, iTotalRecords, iTotalDisplayRecords, sColumns = [], 1, 0, 0, ','.join(columnIndexNameMap.values())

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
def comperformance(request):
    username = request.user.username
    behaviors = Behavior.objects.all().order_by('-actlevel')
    developments = Development.objects.all().order_by('parent')
    behaviorstart = 5
    behaviorend = behaviorstart + Behavior.objects.count() - 1
    physical = behaviorend + 2
    developmentstart = physical + 3
    developmentend = developmentstart + Development.objects.count() -1
    return render_to_response('comperformance/comperformance.html', {
        'title': u'综合测评',
        'behavoirs': behaviors,
        'behaviorstart': behaviorstart,
        'physical': physical,
        'developmentstart': developmentstart,
        'developmentend': developmentend,
        'developments': developments,
        'username': username
    }, context_instance=RequestContext(request))

@login_required
def ajaxcomperformance(request):
    comperformancescores = ComperformanceScore.objects.all().order_by('-comperformance__term', 'student__user__username')
    customSearch = request.GET.get('sSearch', '').rstrip().encode('utf-8')
    if customSearch != '':
        kwargzs = [
            {'comperformance__term__icontains': customSearch},
            {'student__realname__icontains': customSearch},
            {'student__user__username__icontains': customSearch},
            {'student__theclass__classid__icontains': customSearch}
        ]
        outputQ = None
        for kwargz in kwargzs:
            outputQ = outputQ | Q(**kwargz) if outputQ else Q(**kwargz)
        comperformancescores = comperformancescores.filter(outputQ)

    cols = int(request.GET.get('iColumns', 0))
    iDisplayLength = min(int(request.GET.get('iDisplayLength', 10)), 100)
    startRecord = int(request.GET.get('iDisplayStart', 0))
    endRecord = startRecord + iDisplayLength
    sEcho = int(request.GET.get('sEcho', 0))

    iTotalRecords = iTotalDisplayRecords = comperformancescores.count()
    comperformancescores = comperformancescores[startRecord: endRecord]
    aaData = []

    for i in comperformancescores:
        arecord = [unicode(i.comperformance.term), unicode(i.student.realname), unicode(i.student.user.username),
                       unicode(i.student.theclass.classid), unicode(i.score)]
        behaviors = Behavior.objects.all().order_by('-actlevel')
        for j in behaviors:
            try:
                obj = j.comperformancebehaviorscore_set.filter(comperformance=i.comperformance).filter(behavior=j).get(student=i.student)
                comperformancebehaviorscore = obj.score
            except Exception, e:
                comperformancebehaviorscore = ''
            arecord.append(unicode(comperformancebehaviorscore))
        arecord.append(unicode(i.assessmentscore))

        try:
            obj = ComperformancePhysicalScore.objects.filter(comperformance=i.comperformance).get(student=i.student)
            comperformancephysicalscore = obj.score
        except Exception, e:
            comperformancephysicalscore = 0.0
        arecord.append(unicode(comperformancephysicalscore))

        comperformancebehaviorscores = ComperformanceBehaviorScore.objects.filter(comperformance=i.comperformance).filter(student=i.student)
        behaviorscores = i.comperformance.behavior
        if comperformancebehaviorscores:
            for j in comperformancebehaviorscores:
                behaviorscores += j.score
        arecord.append(unicode(behaviorscores))

        try:
            obj = Grade.objects.filter(term=i.comperformance.term).get(student=i.student)
            grade = obj.score
        except Exception, e:
            grade = 0.0
            traceback.print_stack()
            traceback.print_exc()
            print e
        arecord.append(unicode(grade))

        developments = Development.objects.all().order_by('parent')
        for j in developments:
            try:
                obj = j.comperformancedevelopmentscore_set.filter(comperformance=i.comperformance).\
                    filter(development=j).get(student=i.student)
                comperformancedevelopmentscore = obj.score
            except Exception, e:
                comperformancedevelopmentscore = ''
            arecord.append(comperformancedevelopmentscore)
        comperformancedevelopmentscores = ComperformanceDevelopmentScore.objects.filter(comperformance=i.comperformance).\
            filter(student=i.student)
        developmentscores = 0.0
        if comperformancedevelopmentscores:
            for j in comperformancedevelopmentscores:
                developmentscores += j.score
        arecord.append(unicode(developmentscores))

        if request.user.is_superuser:
            arecord.append(unicode(''))
        aaData.append(arecord)

    response_dict = {}
    response_dict.update({'aaData': aaData})
    response_dict.update({
        'sEcho': sEcho,
        'iTotalRecords': iTotalRecords,
        'iTotalDisplayRecords': iTotalDisplayRecords
    })
    response = HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')
    add_never_cache_headers(response)
    return response

@login_required
def ajaxclasscomperformances(request):
    if request.is_ajax():
        try:
            xAxis = [i[0] for i in ComperformanceScore.objects.values_list('comperformance__term').distinct()]
            classes = [i[0] for i in ComperformanceScore.objects.values_list('student__theclass__classid').distinct()]

            xAxis.reverse()
            series = []

            for i in classes:
                series.append({
                    'name': i,
                    'data': [round(ComperformanceScore.objects.filter(student__theclass__classid=i)
                    .filter(comperformance__term=j).aggregate(avgprice=Avg('score'))['avgprice'], 2) for j in xAxis]
                })
            return HttpResponse(simplejson.dumps([xAxis, series]), mimetype='application/json')
        except Exception, e:
            response = 'false'
            traceback.print_stack()
            traceback.print_exc()
            print e
            return HttpResponse(simplejson.dumps([[], []]), mimetype='application/json')
    raise Http404

@login_required
def classcomperformances(request):
    username = request.user.username

    return render_to_response('comperformance/classcomperformances.html', {
        'title': u'综合测评-班级',
        'username': username
    }, context_instance=RequestContext(request))

@login_required
def studentcomperformance(request):
    username = request.user.username
    behaviors = Behavior.objects.all().order_by('-actlevel')
    developments = Development.objects.all().order_by('parent')

    return render_to_response('comperformance/studentcomperformance.html', {
        'title': u'查看综合-学生',
        'behaviors': behaviors,
        'developments': developments,
        'username': username
    }, context_instance=RequestContext(request))



