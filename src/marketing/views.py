import json
import datetime
from django.shortcuts import render , HttpResponse , Http404
from django.http import HttpResponseBadRequest
from django.utils import timezone
from django.conf import settings
from .forms import EmailForm
from accounts.models import EmailMarketingSignUp
# Create your views here.
def dismiss_marketing_message(request):
	if request.is_ajax():
		data={"success":True}
		json_data = json.dumps(data)
		request.session["dismiss_message_for"] = str(timezone.now()\
			+ datetime.timedelta(hours=settings.MARKETING_HOURS_OFFSET \
				,seconds=settings.MARKETING_SECONDS_OFFSET))
		return HttpResponse(json_data, content_type="application/json")
	else:
		raise Http404

def email_signup(request):
	if request.method=="POST":
		form = EmailForm(request.POST or None)
		if form.is_valid():
			email = form.cleaned_data["email"]
			EmailMarketingSignUp.objects.create(email=email)
			request.session["marketing_email_added"] = True
			return HttpResponse("success %s" %(email))
		if form.errors:
			json_data = json.dumps(form.errors)
			return HttpResponseBadRequest(json_data , content_type="application/json")
	else:
		raise Http404