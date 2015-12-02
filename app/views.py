from flask import request, flash, render_template, redirect
from app import app
from .forms import PhoneNumberForm
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
from twilio.util import RequestValidator
import twilio.twiml
import phonenumbers

def validate_X_twilio_signature():
	validator = RequestValidator(app.config['AUTH_TOKEN'])
	# print validator.validate(request.url, request.data, request.headers['X-Twilio-Signature'])

@app.route('/', methods=['GET', 'POST'])
def hello_monkey():
	resp = twilio.twiml.Response()
	resp.say("Hello World")
	return str(resp)

@app.route('/phase1', methods=['GET', 'POST'])
def phase1():
	validate_X_twilio_signature()
	r = twilio.twiml.Response()
	with r.gather(timeout=3, action='/fizz-buzz', method='POST') as g:
		g.say("Please Enter a number to run phone buzz")
	return str(r)

@app.route('/phase2', methods=['GET', 'POST'])
def phase2():
	form = PhoneNumberForm()
	if form.validate_on_submit():
		num = form.number.data
		formatted_num = phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)
		try:
			client = TwilioRestClient(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])
			call = client.calls.create(to=formatted_num, from_="+12404534768", url=request.url_root+"/phase1")
			flash("Successfully calling " + str(num))
		except TwilioRestException as e:
			flash("Failed to call " + str(num))
			print e
		return redirect('/phase2')
	return render_template('phase2.html', form=form)

@app.route('/fizz-buzz', methods=['POST'])
def recieve_digits():
	validate_X_twilio_signature()
	digits = request.values.get('Digits', None)
	num = int(digits)
	r = twilio.twiml.Response()
	for i in range(1, num+1):
		if i%3 == 0:
			r.say("fizz")
		if i%5 == 0:
			r.say("buzz")
		if i%3 != 0 and i%5 != 0:
			r.say(str(i))
	return str(r)


