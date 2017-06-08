from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect, Http404
from .models import KirrURL
from .forms import SubmitUrlForm
from analytics.models import ClickEvent
# Create your views here.

class HomeView(View):
	def get(self,request,*args,**kwargs):
		the_form = SubmitUrlForm()
		bg_image = ''	
		context = {"title":"Kirr.co", "form": the_form, "bg_image":bg_image}
		return render(request,"shortener/home.html",context)

	def post(self,request,*args,**kwargs):
		form = SubmitUrlForm(request.POST)
		context = {"title":"Kirr.co", "form": form}
		template = "shortener/home.html"
		if form.is_valid():
			new_url = form.cleaned_data.get('url')
			obj,created = KirrURL.objects.get_or_create(url= new_url)
			context = {
			"object" : obj,
			"created" : created ,
			}
			if created:
				template = "shortener/success.html"
			else:
				template = "shortener/already-exists.html"
		return render(request,template,context)




#middleware work function view
# def kirr_redirect_view(request,shortcode = None,*args,**kwargs):
# 	obj = get_object_or_404(KirrURL,shortcode = shortcode)
# 	# return HttpResponse("Hello {sc}".format(sc=obj.url) )	
# 	return HttpResponseRedirect(obj.url)
#middleware work


class URLRedirectView(View):
	def get(self,request,shortcode = None,*args,**kwargs):
		qs = KirrURL.objects.filter(shortcode__iexact = shortcode)
		if qs.count() != 1 and not qs.exists():
			raise Http404
		obj = qs.first()
		print(ClickEvent.objects.create_event(obj))
		return HttpResponseRedirect(obj.url)
		


'''
def kirr_redirect_view(request,shortcode = None,*args,**kwargs):

	obj = get_object_or_404(KirrURL,shortcode = shortcode)
	# obj_url =obj.url
	# print(request.method)
	# obj_url =None
	# qs = KirrURL.objects.filter(shortcode__iexact = shortcode.upper())
	# if qs.exists() and qs.count() == 1:
	# 	obj = qs.first()
	# 	obj_url = obj.url
	return HttpResponse("Hello {sc}".format(sc=obj.url) )
'''		