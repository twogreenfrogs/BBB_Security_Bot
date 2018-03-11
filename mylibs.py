#!/usr/bin/python
from twython import Twython, TwythonStreamer
import pickle, time, smtplib
import myvariables
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

#robot default status
def pickle_robot_status():
	status = [
    	{
        	'desc': u'wifi',
        	'status': u'on',
    	},
    	{
        	'desc': u'umts',
        	'status': u'off',
    	},
    	{
        	'desc': u'webcam',
        	'status': u'off',
    	},
    	{
        	'desc': u'ipcam',
        	'status': u'off',
    	},
    	{
        	'desc': u'robot',
        	'status': u'off',
    	},
    	{
        	'desc': u'move',
        	'status': u'stop',
    	},
    	{
        	'desc': u'armed',
        	'status': u'off',

    	},
    	{
        	'desc': u'lamp',
        	'status': u'off',
    	},
	]

	with open('robot_status.pickle', 'wb') as handle:
        	pickle.dump(status, handle)

	'''
	with open('robot_status.pickle', 'rb') as handle:
        	curr_status = pickle.load(handle)
	print curr_status
	'''

# post message in twitter
def post_msg_twitter(msg): 
	twitter = Twython(myvariables.TWITTER_KEY, myvariables.TWITTER_SECRET, myvariables.TWITTER_TOKEN, myvariables.TWITTER_TOKEN_SECRET)
	twitter.update_status(status=msg)

# send mail
def send_email(to_mail, txt, subject):
        print("Sending Email")
        #smtpserver = smtplib.SMTP("smtp.live.com", 25)
        smtpserver = smtplib.SMTP("smtp.live.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(myvariables.EMAIL_USER, myvariables.EMAIL_PASS)
        header = 'To:' + to_mail + '\n' + 'From: ' + myvariables.EMAIL_USER
        header = header + '\n' + 'Subject:' + subject + '\n'
        print header
        msg = header + '\n' + txt + ' \n\n'
        smtpserver.sendmail(myvariables.EMAIL_USER, to_mail, msg)
        smtpserver.close()

# monitor particular message in twitter
def mon_msg_twitter(msg):
	TERMS = msg 

	class BlinkyStreamer(TwythonStreamer):
        	def on_success(self, data):
                	if 'text' in data:
                        	print data['text'].encode('utf-8')
                        	print

	stream = BlinkyStreamer(myvariables.TWITTER_KEY, myvariables.TWITTER_SECRET, myvariables.TWITTER_TOKEN, myvariables.TWITTER_TOKEN_SECRET)
	stream.statuses.filter(track=TERMS)

# send sms to mobile phone
def send_sms(msg):
	client = TwilioRestClient(myvariables.TWILIO_SID, myvariables.TWILIO_TOKEN)
	message = client.messages.create(to=myvariables.CELL_NUM, from_=myvariables.TWILIO_NUM,body=msg)

