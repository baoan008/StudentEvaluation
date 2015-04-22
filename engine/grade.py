#encoding:utf-8
import os
from time import strftime, localtime
import traceback
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from xlrd import open_workbook
from StudentEvaluation import settings
from engine.models import Grade, Student
from forms import ImportForm


@login_required
def importgrades(request):
    username = request.user.username
    if request.POST:
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                xlsfile = request.FILES.get('grades', '')
                filename = xlsfile.name
                #文件存储路径创建
                fname = os.path.normpath(os.path.join(settings.MEDIA_ROOT, 'uploads/grades/%s' %strftime('%Y/%m/%d', localtime()), filename))
                if os.path.exists(fname):
                    os.remove(fname)
                dirs = os.path.dirname(fname)
                if not os.path.exists(dirs):
                    os.makedirs(dirs)
                #Writing into file
                if os.path.isfile(fname):
                    os.remove(fname)
                content = xlsfile.read()
                fp = open(fname, 'wb')
                fp.write(content)
                fp.close()
                #格式化xls文件中数据， 将其存在到数据库中
                book = open_workbook(fname)
                sheet = book.sheet_by_index(0)

                for row_index in range(sheet.nrows):
                    record = sheet.row_values(row_index, 0)
                    try:
                        student = Student.objects.get(user__username=str(record[1]).rstrip(".0"))
                        grade = Grade(term=record[0], student=student, socre=record[2])
                        grade.save()
                    except Student.DoseNotExist, e:
                        traceback.print_stack()
                        traceback.print_exc()
                        print e
                successinfo = u'上传'
                success = True
                return render_to_response('grade/import.html', {
                    'title': u'导入成绩',
                    'form': form,
                    'successinfo': successinfo,
                    'success': success,
                    'username': username
                }, context_instance=RequestContext(request))
            except Exception, e:
                traceback.print_stack()
                traceback.print_exc()
                print e
        else:
            return render_to_response('grade/import.html', {
                'title': u'导入成绩',
                'form': form,
                'username': username
            }, context_instance=RequestContext(request))
    return render_to_response('grade/import.html', {
        'title': u'学生成绩',
        'username': username
    }, context_instance=RequestContext(request))


@login_required
def index(request):
    username = request.user.username
    return render_to_response('grade/grades.html', {
        'title': u'成绩管理',
        'username': username
    }, context_instance=RequestContext(request))

@login_required
def studentgrades(request):
    if int(request.GET.get('iSortCol_0')) == 2:
        if request.GET.get('sSortDir_0') == 'desc':
            grades = Grade.objects.all().order_by('-term', '-student__user__username')
        else:
            grades = Grade.objects.all().order_by('-term', 'student__user__username')
    elif int(request.GET.get('iSortCol_0')) == 4:
        if request.GET.get('sSortDir_0') == 'desc':
            grades = Grade.objects.all().order_by('-term', '-score')
        else:
            grades = Grade.objects.all().order_by('-term', 'score')
    else:
        grades = Grade.objects.all().order_by('-term', 'student__user__username')

    customSearch = request.GET.get('sSearch', '').rstrip().encode('utf-8')
    if customSearch != '':
        kwargzs = [
            {'term__icontains': customSearch},
            {'student__realname__icontains': customSearch},
            {'student__user__username__icontains': customSearch},
            {'student__theclass__classid__icontains': customSearch}
        ]
        outputQ = None
        for kwargz in kwargzs:
            outputQ = outputQ | Q(**kwargz) if outputQ else Q(**kwargz)
        grades = grades.filter(outputQ)

    cols = int(request.GET.get('iColumns', 0))
    iDisplayLength = min(int(request.GET.get('iDisplayLength', 10)), 100)
    startRecord = int(request.GET.get('iDisplayStart', 0))#本页第一条数据，是所有数据的第几个,从0开始
    endRecord = startRecord + iDisplayLength
    sEcho = int(request.GET.get('sEcho', 0))

    iTotalRecords = iTotalDisplayRecords = grades.count()
    grades = grades[startRecord:endRecord]
    aaData = [[unicode(i.term), unicode(i.student.realname), unicode(i.student.user.username),
               unicode(i.student.theclass.classid), unicode(str(i.score)),] for i in grades]
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
def classgrades(request):
    username = request.user.username
    return render_to_response('grade/classgrades.html', {
        'title': '班级成绩',
        'username': username
    }, context_instance=RequestContext(request))

@login_required
def ajaxclassgrades(request):
    if request.is_ajax():
        try:
            xAxis = [i[0] for i in Grade.objects.values_list('term').distinct()]
            classes = [i[0] for i in Grade.objects.values_list('student__theclass__classid').distinct()]
            xAxis.reverse()
            series = []

            #控制小数点位数
            for i in classes:
                series.append({
                    'name': i,
                    'data': [round(Grade.objects.filter(
                        student__theclass__classid=i).filter(term=j).aggregate(
                        avgprice=Avg('score'))['avgprice'], 2) for j in xAxis]
                })
            return HttpResponse(simplejson.dumps([xAxis, series]), mimetype='application/json')
        except Exception, e:
            response = 'false'
            traceback.print_stack()
            print e
            return HttpResponse(simplejson.dumps([[],[]]), mimetype='application/json')
    raise Http404
