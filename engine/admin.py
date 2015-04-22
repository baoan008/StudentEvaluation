#encoding: utf-8
from django.contrib import admin
from engine.models import Class, Student, Grade, Assessment, AssessmentRecord,  AssessmentRow, \
    Behavior, Comperformance, Development, ComperformanceBehaviorScore, ComperformanceDevelopmentScore, \
    ComperformancePhysicalScore, ComperformanceScore

# Register your models here.
class StudentInline(admin.TabularInline):
    model = Student
    extra = 3

class ClassAdmin(admin.ModelAdmin):
    inlines = [StudentInline]
    list_display = ('id', 'classid', 'classname')
    search_fields = ['classname']

class StudentAdmin(admin.ModelAdmin):
    def classname(self, obj):
        return obj.theclass.classname
    classname.short_description = u'班级'

    list_per_page = 10
    radio_fields = {'sex': admin.HORIZONTAL}
    list_display = ['id', 'user', 'realname', 'classname', 'sex']
    list_display_links = ['id', 'user', 'realname']
    list_filter = ['sex', 'theclass']
    search_fields = ['realname', 'theclass__classname', 'user__username']

class GradeAdmin(admin.ModelAdmin):
    def studentname(self, obj):
        return obj.student.realname
    studentname.short_description = u'学生'

    list_display = ['id', 'studentname', 'term', 'score']
    list_display_links = ['id', 'studentname']
    search_fields = ['student__realname']
    list_filter = ['term', 'student__theclass__classname']

class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'begindate', 'enddate', 'term', 'excellent', 'good', 'ordinary']
    list_filter = ['begindate', 'enddate', 'term']

class AssessmentRecordAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id', 'assessment', 'ostudent', 'dstudent', 'result']
    list_filter = ['assessment']
    search_fields = ['ostudent__realname']

class AssessmentRowAdmin(admin.ModelAdmin):
    def studentname(self, obj):
        return obj.student.realname
    studentname.short_description = u'学生'

    list_per_page = 20
    list_display = ['id', 'studentname', 'assessment', 'excellent', 'good', 'ordinary']
    list_display_links = ['id', 'studentname']
    list_filter = ['assessment__term', 'student__theclass__classname']
    search_fields = ['student__realname']


class BehaviorAdmin(admin.ModelAdmin):
    radio_fields = {'actlevel': admin.HORIZONTAL}
    list_display = ['id', 'actlevel', 'name']
    list_filter = ['actlevel']
    search_fields = ['name']

class DevelopmentAdmin(admin.ModelAdmin):
    radio_fields = {'parent': admin.HORIZONTAL}
    list_display = ['id', 'parent', 'name']
    list_filter = ['parent']
    search_fields = ['name']

class ComperformanceAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ('Basic', {'fields' : [('excellent', 'good', 'ordinary')]})
    # ]
    fields = [('excellent', 'good', 'ordinary'), ('physical', 'development', 'moral', 'behaviorup'), 'term']
    list_display = ['id', 'term', 'excellent', 'good', 'ordinary', 'physical', 'development',
                    'moral', 'behaviorup']
    list_display_links = ['id', 'term']
    list_filter = ['term']

class ComperformanceBehaviorScoreAdmin(admin.ModelAdmin):
    def studentname(self, obj):
        return obj.student.realname
    studentname.short_description = u'学生'

    list_display = ['id', 'studentname', 'comperformance', 'behavior', 'score']
    list_display_links = ['id', 'studentname']
    list_filter = ['behavior__name', 'behavior__actlevel']
    search_fields = ['student__realname']

class ComperformanceDevelopmentScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'comperformance', 'development', 'score']
    list_filter = ['development__name', 'development__parent']
    search_fields = ['student__realname']

class ComperformancePhysicalScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'comperformance', 'score']
    search_fields = ['student__realname']

class ComperformanceScoreAdmin(admin.ModelAdmin):
    def studentname(self, obj):
        return obj.student.realname
    studentname.short_description = u'学生'

    readonly_fields = ['studentname', 'comperformance', 'assessmentscore', 'score']
    list_display = ['id', 'studentname', 'comperformance', 'assessmentscore', 'score']
    list_display_links = ['id', 'studentname']
    search_fields = ['student__realname']

admin.site.register(Class, ClassAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(AssessmentRecord, AssessmentRecordAdmin)
admin.site.register(AssessmentRow, AssessmentRowAdmin)
admin.site.register(Behavior, BehaviorAdmin)
admin.site.register(Comperformance, ComperformanceAdmin)
admin.site.register(Development, DevelopmentAdmin)
admin.site.register(ComperformanceBehaviorScore, ComperformanceBehaviorScoreAdmin)
admin.site.register(ComperformanceDevelopmentScore, ComperformanceDevelopmentScoreAdmin)
admin.site.register(ComperformancePhysicalScore, ComperformancePhysicalScoreAdmin)
admin.site.register(ComperformanceScore, ComperformanceScoreAdmin)
