#encoding:utf-8
from django.forms.fields import CharField
from validators import username, password, classid, classname, studentid, studentname, term

class UsernameField(CharField):
    default_error_message = {
        'invalid':u'学生：学号，管理员：6-12位， 由数字、下划线组成，首字符必须为字母',
        'required':u'用户名必填（学生：学号，管理员：6-12位， 由数字、下划线组成，首字符必须为字母）',
        'max_length':u'用户名最多12位',
        'min_length':u'用户名最多6位',
    }
    default_validators = [username]

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(UsernameField, self).clean(value)

class PasswordField(CharField):
    default_error_messages = {
        'invalid':u'密码是有字母或下划线组成的字符串，最少为8位',
        'required':u'密码为必填项(由字母数字下划线组成的字符串，最少为6位)',
        'max_length':u'密码最多为16位',
        'min_length':u'密码最少为8位',
    }
    default_validators = [password]

class ClassidField(CharField):
    default_error_messages = {
        'invalid':u'班号由7位数数字组成',
        'required':u'班号必须要填(7位数数字)',
    }
    default_validators = [classid]

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(ClassidField, self).clean(value)

class ClassnameField(CharField):
    default_error_messages = {
        'invalid':u'班级姓名必须是2-6个汉字',
        'required':u'班级姓名必须要填（2-6个汉字）',
    }
    default_validators = [classname]

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(ClassnameField, self).clean(value)

class StudentidField(CharField):
    default_error_messages = {
        'invalid': u'学号必须为9位数字',
        'required': u'学号必须要填(9位数数字)',
    }

    default_validators = [studentid]

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(StudentidField, self).clean(value)

class StudentnameField(CharField):
    default_error_messages = {
        'invalid': u'学生姓名必须是2-4个汉字',
        'required': u'学生姓名必须要填（2-4个汉字）',
    }

    default_validators = [studentname]

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(StudentnameField, self).clean(value)

class TermField(CharField):
    default_error_messages={
        'invalid': u'要按照(2014年秋)格式填',
        'required': u'学期为必填项'
    }

    default_validators = [term]
    def clean(self, value):
        value = self.to_python(value).strip()
        return super(TermField, self).clean(value)
