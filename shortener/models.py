from django.db import models
from .utils import code_generator, create_shortcode
from django.conf import settings
from .validators import validate_url	
from django_hosts.resolvers import reverse
SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX",15)
# Create your models here.

class KirrURLManager(models.Manager):
	def all(self,*args,**kwargs):
		qs= super(KirrURLManager,self).all(*args,**kwargs)
		return qs
	def refresh_shortcodes(self):
		qs = KirrURL.objects.filter(id__gte=1)
		new_codes = 0;
		for q in qs:
			q.shortcode = create_shortcode(q); 
			q.save()
			new_codes = new_codes +1
		return "New codesmade: {i}".format(i=new_codes)	



class KirrURL(models.Model):
	url = models.CharField(max_length = 220,validators = [validate_url])
	shortcode = models.CharField(max_length = SHORTCODE_MAX,unique= True,blank =True)
	updated = models.DateTimeField(auto_now = True)
	timestamp = models.DateTimeField(auto_now_add = True)
	active = models.BooleanField(default = True)
	objects = KirrURLManager()


	def save(self,*args,**kwargs):
		if self.shortcode is None or self.shortcode == "":
			self.shortcode = create_shortcode(self)
		if not "http" in self.url:
			self.url = "http://" + self.url
		super(KirrURL,self).save(*args,**kwargs)


	def __str__(self):
		return str(self.url)

	def get_short_url(self):
		url_path = reverse("scode",kwargs ={"shortcode":self.shortcode},host ='www',scheme="http")
		return url_path	


		