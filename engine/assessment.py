#encoding:utf-8
import traceback
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from engine.models import Assessment, AssessmentRow, SEX_CHOICES, AssessmentRecord, EVALUATE_CHOICES
from engine.utils import get_datatables_records
from engine.forms import AssessmentForm

@login_required
def index(request):
    username = request.user.username
    return render_to_response('assessment/assessment.html', {
        'title': u'互评管理',
        'username': username
    }, context_instance=RequestContext(request))

@login_required
def addassessment(request):
    username = request.user.username
    if request.method == 'POST':
        form = AssessmentForm(data=request.POST)
        if form.is_valid():
            form.save()
            success = True
            successinfo = u'添加'
            return render_to_response('assessment/assessment.html', {
                'title': u'互评设置',
                'form': form,
                'success': success,
                'successinfo': successinfo,
                'username': username
            }, context_instance=RequestContext(request))
        else:
            return render_to_response('assessment/assessment.html', {
                'title': u'互评设置',
                'form': form,
                'username': username
            }, context_instance=RequestContext(request))
    return HttpResponseRedirect('/manage/assessment/')

@login_required
def editassessment(request):
    username = request.user.username
    if request.method == 'POST':
        form = AssessmentForm(data=request.POST)
        if form.is_valid():
            form.update()
            success = True,
            successinfo = u'修改'
            return render_to_response('assessment/assessment.html', {
                'title': u'互评设置',
                'form': form,
                'success': success,
                'successinfo': successinfo,
                'username': username
            }, context_instance=RequestContext(request))
        else:
            return render_to_response('assessment/assessment.html', {
                'title': u'互评设置',
                'form': form,
                'username': username
            }, context_instance=RequestContext(request))
    return HttpResponseRedirect('/manage/assessment/')

@login_required
def deleteassessment(request):
    username = request.user.username
    if request.method == 'POST':
        try:
            assessment_id = request.POST.get('id')
            try:
                delassessment = Assessment.objects.get(id=assessment_id)
                delassessment.delete()
                success = True
                successinfo = u'删除'
                return render_to_response('assessment/assessment.html', {
                    'title': u'互评设置',
                    'success': success,
                    'successinfo': successinfo,
                    'username': username
                }, context_instance=RequestContext(request))
            except Assessment.DoesNotExist, e:
                traceback.print_stack()
        except Exception, e:
            traceback.print_stack()
    return HttpResponseRedirect('/manage/assessment/')

@login_required
def get_assessments_list(request):
    assessments = Assessment.objects.all().reverse()
    columnIndexNameMap = {
        0: 'id',
        1: 'term',
        2: 'begindate',
        3: 'enddate',
        4: 'excellent',
        5: 'good',
        6: 'ordinary'
    }
    try:
        aaData, sEcho, iTotalRecords, iTotalDisplayRecords, sColumns = get_datatables_records(request,
                                                                                              assessments,
                                                                                              columnIndexNameMap,
                                                                                          None, {}, False, {}, {})
    except Exception, e:
        traceback.print_stack()
        aaData, sEcho, iTotalRecords, iTotalDisplayRecords, sColumns = [], 1, 0, 0, ','\
            .join(columnIndexNameMap.values())
    response_dict = {}
    response_dict.update({'aaData': aaData})
    response_dict.update({
        'sEcho': sEcho,
        'iTotalRecords': iTotalRecords,
        'iTotaldisplayRecords': iTotalDisplayRecords,
        'sColumns': sColumns
    })
    response = HttpResponse(simplejson.dumps(response_dict), mimetype='application/ajax')

    #阻止缓存
    add_never_cache_headers(response)
    return response

@login_required
def viewassessment(request):
    username = request.user.username
    return render_to_response('assessment/viewassessments.html', {
        'title': u'查看互评',
        'username': username
    }, context_instance=RequestContext(request))

@login_required
def view_assessments_list(request):

    if not request.user.is_superuser:
        assessmentrows = AssessmentRow.objects.filter(student=request.user.student)
    else:
        assessmentrows = AssessmentRow.objects.all().order_by('-assessment__term', 'student__user__username')

    #实时搜索
    customSearch = request.GET.get('sSearch', '').strip().encode('utf-8')
    if customSearch != '':
        kwargzs = [
            {"assessment__term__icontains": customSearch},
            {"student__realname__icontains": customSearch},
            {"student__user__username__icontains": customSearch},
            {"student__theclass__classid__icontains": customSearch},
        ]
        outputQ = None
        for kwargz in kwargzs:
            outputQ = outputQ | Q(**kwargz) if outputQ else Q(**kwargz)
        assessmentrows = assessmentrows.filter(outputQ)

    #获取database配置信息
    cols = int(request.GET.get('iColumns', 0)) #多少列
    iDisplayLength = min(int(request.GET.get('iDisplayLength', 10)), 100) #每页显示记录数
    startRecord = int(request.GET.get('iDisplayStart', 0)) #本页的第一条数据是所有数据的第几条
    endRecord = startRecord + iDisplayLength
    sEcho = int(request.GET.get('sEcho', 0)) #页码
    iTotalRecords = iTotaldisplayRecords = assessmentrows.count() #所有记录
    assessmentrows = assessmentrows[startRecord: endRecord]
    aaData = [[unicode(i.assessment.term), unicode(i.student.realname), unicode(i.student.user.username),
               unicode(i.student.theclass.classid), unicode(i.excellent), unicode(i.good),
               unicode(i.ordinary)] for i in assessmentrows]

    response_dict = {}
    response_dict.update({'aaData':aaData})
    response_dict.update({
        'sEcho': sEcho,
        'iTotalRecords': iTotalRecords,
        'iTotaldisplayRecords': iTotaldisplayRecords
    })

    response = HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')
    add_never_cache_headers(response)
    return response

@login_required
def goassessment(request):
    username = request.user.username
    return render_to_response('assessment/goassessment.html', {
        'title': u'进行互评',
        'username': username
    }, context_instance=RequestContext(request))

@login_required
def go_assessments_list(request):
    today = datetime.date.today()
    kwargzs = [
        {'assessment__enddate__gte': today},
        {'assessment__begindate__lte': today},
    ]
    outputQ = None
    for kwargz in kwargzs:
        outputQ = outputQ & Q(**kwargz) if outputQ else Q(**kwargz)
    assessmentrecords = AssessmentRecord.objects.filter(ostudent=request.user.student).filter(outputQ).\
        order_by('-assessment__term', 'dstudent__user__username')

    customSearch = request.GET.get('sSearch', '').rstrip().encode('utf-8')
    if customSearch != '':
        kwargzs = [
            {'dstudent__realname__icontains': customSearch},
            {'dstudent__user__username__icontains': customSearch},
        ]
        outputQ = None
        for kwargz in kwargzs:
            outputQ = outputQ | Q(**kwargz) if outputQ else Q(**kwargz)
        assessmentrecords = assessmentrecords.filter(outputQ)

    cols = int(request.GET.get('iColumns', 0)) #获取列数
    iDisplayLength = min(int(request.GET.get('iDisplayLength', 10)), 100)
    startRecord = int(request.GET.get('iDisplayStart', 0))
    endRecord = startRecord + iDisplayLength
    sEcho = int(request.GET.get('sEcho', 0))

    iTotalRecords = iTotalDislayRecords = assessmentrecords.count()
    assessmentrecords = assessmentrecords[startRecord: endRecord]
    #注意此时：不能使用unicode(dict(EVALUATE_CHOICES)[i.result])
    aaData = [[unicode(i.assessment.term), unicode(i.dstudent.realname), unicode(i.dstudent.user.username),
               dict(SEX_CHOICES)[i.dstudent.sex], dict(EVALUATE_CHOICES)[i.result]] for i in assessmentrecords]

    response_dict = {}
    response_dict.update({'aaData': aaData})
    response_dict.update({
        'sEcho': sEcho,
        'iTotalRecords': iTotalRecords,
        'iTotalDisplayRecords': iTotalDislayRecords
    })
    response = HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')
    add_never_cache_headers(response)
    return response

@login_required
def go_assessments(request):
    if request.is_ajax():
        response = 'true'
        try:
            term = request.GET['term']
            username = request.GET['username']
            result = request.GET['result']

            today = datetime.date.today()
            kwargzs = [
                {"assessment__enddate__gte": today},
                {"assessment__begindate__lte": today},
            ]
            outputQ = None
            for kwargz in kwargzs:
                outputQ = outputQ & Q(**kwargz) if outputQ else Q(**kwargz)
            assessmentrecord = AssessmentRecord.objects.filter(ostudent=request.user.student).filter(outputQ).filter(assessment__term = term.encode('utf-8')).get(dstudent=User.objects.get(username = username).student)

            oriresult = assessmentrecord.result

            #目前已经含有的相应评价的个数
            hasresults = AssessmentRecord.objects.filter(ostudent=request.user.student).filter(outputQ).filter(assessment__term = term.encode('utf-8')).filter(result=dict([[i[1],i[0]] for i in EVALUATE_CHOICES])[result.encode('utf-8')]).count()

            #获取班级同学总数
            studentnum = User.objects.get(username = username).student.theclass.student_set.count()

            assessmentrow = AssessmentRow.objects.get(student=User.objects.get(username = username).student)

            if result.encode('utf-8') == "优":
                assessment = Assessment.objects.get(term=term.encode('utf-8'))
                if hasresults < assessment.excellent*studentnum/100 + 1:
                    assessmentrecord.result = dict([[i[1],i[0]] for i in EVALUATE_CHOICES])[result.encode('utf-8')]
                    assessmentrecord.save()
                    assessmentrow.excellent+=1
                else:
                    response = 'false'
                    response_num = assessment.excellent*studentnum/100 + 1
            elif result.encode('utf-8') == "良":
                assessment = Assessment.objects.get(term=term.encode('utf-8'))
                if hasresults < assessment.good*studentnum/100 + 1:
                    assessmentrecord.result = dict([[i[1],i[0]] for i in EVALUATE_CHOICES])[result.encode('utf-8')]
                    assessmentrecord.save()
                    assessmentrow.good+=1
                else:
                    response = 'false'
                    response_num = assessment.good*studentnum/100 + 1
            elif result.encode('utf-8') == "中":
                assessment = Assessment.objects.get(term=term.encode('utf-8'))
                if hasresults <= (studentnum - assessment.excellent*studentnum/100 - 2 - assessment.good*studentnum/100):
                    assessmentrecord.result = dict([[i[1],i[0]] for i in EVALUATE_CHOICES])[result.encode('utf-8')]
                    assessmentrecord.save()
                    assessmentrow.ordinary+=1
                else:
                    response = 'false'
                    response_num = studentnum - assessment.excellent*studentnum/100 - 2 - assessment.good*studentnum/100

            if response == 'false':
                return HttpResponse(simplejson.dumps([response,str(response_num)]), mimetype='application/json')
            else:
                if oriresult == '0':
                    assessmentrow.excellent -= 1
                elif oriresult == '1':
                    assessmentrow.good -= 1
                elif oriresult == '2':
                    assessmentrow.ordinary -= 1
                assessmentrow.save()
                return HttpResponse(simplejson.dumps([response]), mimetype='application/json')
        except Exception,e:
            response = 'false'
            traceback.print_stack()
            print e
            return HttpResponse(simplejson.dumps([response,"error"]), mimetype='application/json')

    raise Http404



