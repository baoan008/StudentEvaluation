#encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

@login_required
def index(request):
    username = request.user.username
    return render_to_response('index.html', {
        'title': u'主页',
        'username': username
    }, context_instance=RequestContext(request))

