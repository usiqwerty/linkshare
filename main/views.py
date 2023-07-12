from django.shortcuts import render
from math import log, ceil
import random
from django.http import Http404
from django.core.exceptions import BadRequest
from django.http import HttpResponse
# Create your views here.
alph="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alph+=alph.lower()
class Link:
	def __init__(self, url, autodelete:bool, allowdelete:bool):
		self.url=url
		self.autodelete=autodelete
		self.allowdelete=allowdelete
db=dict()
strings={
	'dbItems': 0,
	'inputNewPH':'Введите URL или код',
	'submitNew':'Создать',
	'submitOpen':'Открыть',
	'autodelete':'Удалить при открытии',
	'allowdelete':'Разрешить удаление при просмотре',
	'ad_msg':'Ссылка автоматически удалена',
	'delete':'Удалить ссылку'
}
def main(request):
	return render(request, 'index.html', strings)

def post(request):
	print(db)
	if request.POST:
		data=request.POST['data'].strip()
		#print(request.POST)
		if 'open' in request.POST:
			type='open'
		else:
			type='new'
		if type=='new':
			autodelete='autodelete' in request.POST
			allowdelete='allowdelete' in request.POST
			l=len(db)
			if l<2: l=2

			strlen=ceil( log(l, len(alph)) )

			code=None
			while not code or code in db:
				code=''
				for i in range(strlen):
					code+=random.choice(alph)


			db[code]=Link(data, autodelete,allowdelete)
			strings['dbItems']+=1
			return render(request, 'created.html', {'code': code})
		if type=="open":
			code=data.strip()
			print(code)
			if code in db:
				link=db[code]
				url=link.url
				ad_msg=''
				if link.autodelete:
					ad_msg=strings['ad_msg']
					strings['dbItems']-=1
					db.pop(code)
				vars={'link': url,
					'ad_msg': ad_msg,
					'allowdelete' : link.allowdelete,
					'delete':strings['delete'],
					'code': code,
					}
				return render(request, 'open.html', vars)

			else:
				raise Http404
def delete(request):
	if request.POST:
		if 'code' in request.POST:
			code=request.POST['code']
			db.pop(code)
			strings['dbItems']-=1
			return render(request, 'deleted.html', vars)
		else:
			raise Http404('3')
	else:
		raise BadRequest('Bad request')


def handler_400(request, exc):
	return HttpResponse(request, "<center><h1>#_# 400 Bad request</h1></center>")
def handler_403(request, exc):
	return HttpResponse(request, "<center><h1>o_O 403 Forbidden</h1></center>")
def handler_404(request, exc):
	return HttpResponse(request, "<center><h1>@_@ 404 Not found</h1></center>")
def handler_500(request):
	return HttpResponse(request, "<center><h1>x_x 500 Internal server error</h1></center>")

