# Exception handling module for python scripts

import datetime
from pyslack import SlackClient
import time
import smtplib


def ehmlog(message):
	try:
		ts = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
		f = open('ehm_err.log', 'a')
		f.write('LOG [ %s ] %s \n'%(ts, message))
		f.close()
	except Exception, e:
		print "[ EHM ERROR ] while creating EHM Log: %s"%e

def logToFile(filename, message, error_type):
	try:
		ts = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
		f = open(filename, 'a')
		if error_type == exeptionHandlingModule.EHM_LOG:
			f.write('LOG [ %s ] %s \n'%(ts, message))
		if error_type == exeptionHandlingModule.EHM_EXCEPTION_CRITICAL:
			f.write('CRITICAL [ %s ] %s \n'%(ts, message))
		if error_type == exeptionHandlingModule.EHM_EXCEPTION_WARNING:
			f.write('WARNING [ %s ] %s \n'%(ts, message))
		if error_type == exeptionHandlingModule.EHM_EXCEPTION_IGNORABLE:
			f.write('IGNORABLE [ %s ] %s \n'%(ts, message))
		f.close()
	except Exception, e:
		print "[ EHM ERROR ] while writing to log file: %s"%e
		ehmlog("[ EHM ERROR ] while writing to log file: %s"%e)

def postOnSlack(channel, botName, message, access_token, log_type):
	slackMessage = ""
	channel = "#%s"%channel
	
	if (time.time() - exeptionHandlingModule.EHM_SLACK_POST_TIME) > 1:
		if log_type == exeptionHandlingModule.EHM_LOG:
			slackMessage = slackMessage + "[ %s - Log ] :information_source: \n"%exeptionHandlingModule.EHM_APP_NAME
			slackMessage = slackMessage + "```Message: %s \nEHM Code: %s ```"%(message, exeptionHandlingModule.EHM_LOG)
		elif log_type == exeptionHandlingModule.EHM_EXCEPTION_CRITICAL:
			slackMessage = slackMessage + "[ %s - CRITICAL ERROR ] :no_entry: \n"%exeptionHandlingModule.EHM_APP_NAME
			slackMessage = slackMessage + "```Message: %s \nEHM Code: %s ```"%(message, exeptionHandlingModule.EHM_LOG)
		elif log_type == exeptionHandlingModule.EHM_EXCEPTION_WARNING:
			slackMessage = slackMessage + "[ %s - WARNING ] :warning: \n"%exeptionHandlingModule.EHM_APP_NAME
			slackMessage = slackMessage + "```Message: %s \nEHM Code: %s ```"%(message, exeptionHandlingModule.EHM_LOG)
		elif log_type == exeptionHandlingModule.EHM_EXCEPTION_IGNORABLE:
			slackMessage = slackMessage + "[ %s - IGNORABLE ERROR ] :heavy_exclamation_mark: \n"%exeptionHandlingModule.EHM_APP_NAME
			slackMessage = slackMessage + "```Message: %s \nEHM Code: %s ```"%(message, exeptionHandlingModule.EHM_LOG)
		try:
			token = access_token
			client = SlackClient(token)
			client.chat_post_message(channel, slackMessage, username=botName)
			exeptionHandlingModule.EHM_SLACK_POST_TIME = time.time()
		except Exception, e:
			print "[ EHM ERROR ] while posting message to slack: %s"%e
			ehmlog("[ EHM ERROR ] while posting message to slack: %s"%e)

def logToScreen(message, error_type):
	try:
		if error_type == exeptionHandlingModule.EHM_LOG:
			print "[ LOG ] %s"%message	
		elif error_type == exeptionHandlingModule.EHM_EXCEPTION_CRITICAL:
			print "[ CRITICAL ] %s"%message
		elif error_type == exeptionHandlingModule.EHM_EXCEPTION_WARNING:
			print "[ WARNING ] %s"%message
		elif error_type == exeptionHandlingModule.EHM_EXCEPTION_IGNORABLE:
			print "[ IGNORABLE ] %s"%message
	except Exception, e:
		print "[ EHM ERROR ] while Loging to screen: %s"%e
		ehmlog("[ EHM ERROR ] while Loging to screen: %s"%e)


def sendEmail(body, to, sender, subject, smtp_host, smtp_port, login, password):
	receivers = to

	message = """From: EHM LOGGER <%s>
To: Monitor <%s>
Subject: %s

%s."""%(sender, 'saadanjum91@gmail.com', subject, body)

	try:
		smtpObj = smtplib.SMTP(str(smtp_host), smtp_port)
		smtpObj.login(str(login), str(password))
		smtpObj.sendmail(sender, receivers, message)         
		print "Successfully sent email"
	except Exception, e:
		print "Error: %s"%e

class exeptionHandlingModule:

	EHM_EXCEPTION_CRITICAL = 1
	EHM_EXCEPTION_WARNING = 3
	EHM_EXCEPTION_IGNORABLE = 2
	EHM_LOG = 4
	EHM_APP_NAME = "Default App"
	EHM_SLACK_POST_TIME = None

	def __init__(self, app_name):
		self.REPORTING_METHOD = ['file', 'slack', 'email']
		self.SLACK_TOKEN = None
		self.CRITICAL_ERROR_THRESHOLD = 3
		self.LOG_FILE = 'EHM_log.log'
		self.CURRENT_CRITICAL_COUNT = {}
		self.POST_CRITICAL_ON_SLACK = False
		self.POST_IGNORABLE_ON_SLACK = False
		exeptionHandlingModule.EHM_APP_NAME = app_name
		exeptionHandlingModule.EHM_SLACK_POST_TIME = time.time()
		self.SEND_EMAIL_ON_THRESHOLD_REACH = False
		self.SMTP_HOST = None
		self.SMTP_PORT = 25
		self.SENDING_EMAIL_ADDRESS = None
		self.EMAIL_PASSWORD = None
		self.EMAIL_ADDRESS = None
		self.EMAIL_SENT_STATUS = {}
		self.SLACK_CHANNEL = None

	def getReportingMethod(self):
		return self.REPORTING_METHOD

	def getSlackToken(self):
		return self.SLACK_TOKEN

	def getNotificationEmail(self):
		return self.NOTIFICATION_EMAIL

	def getCriticalErrorThreshold(self):
		return self.CRITICAL_ERROR_THRESHOLD

	def set(self, attribute, value):
		if attribute == 'REPORTING_METHOD':
			self.REPORTING_METHOD = value
		elif attribute == 'SLACK_TOKEN':
			self.SLACK_TOKEN = value
		elif attribute == 'CRITICAL_ERROR_THRESHOLD':
			self.CRITICAL_ERROR_THRESHOLD = value
		elif attribute == 'LOG_FILE':
			self.LOG_FILE = value
		elif attribute == 'POST_CRITICAL_ON_SLACK':
			self.POST_CRITICAL_ON_SLACK = value
		elif attribute == 'POST_IGNORABLE_ON_SLACK':
			self.POST_IGNORABLE_ON_SLACK = value
		elif attribute == 'SEND_EMAIL_ON_THRESHOLD_REACH':
			self.SEND_EMAIL_ON_THRESHOLD_REACH = value
		elif attribute == 'SMTP_HOST':
			self.SMTP_HOST = value
		elif attribute == 'SMTP_PORT':
			self.SMTP_PORT = value
		elif attribute == 'SENDING_EMAIL_ADDRESS':
			self.SENDING_EMAIL_ADDRESS = value
		elif attribute == 'EMAIL_PASSWORD':
			self.EMAIL_PASSWORD = value
		elif attribute == 'EMAIL_ADDRESS':
			self.EMAIL_ADDRESS = value

		return self

	def reportError(self, error_type, error_message, error_code):
		if error_type == exeptionHandlingModule.EHM_EXCEPTION_CRITICAL:
			error_previously_reported = False
			for prev_error_code in self.CURRENT_CRITICAL_COUNT:
				if prev_error_code == error_code:
					error_previously_reported = True

			if error_previously_reported == False:
				self.CURRENT_CRITICAL_COUNT[error_code] = 1
				self.EMAIL_SENT_STATUS[error_code] = False
			else:
				self.CURRENT_CRITICAL_COUNT[error_code] = self.CURRENT_CRITICAL_COUNT[error_code] + 1

			if self.CURRENT_CRITICAL_COUNT[error_code] < self.CRITICAL_ERROR_THRESHOLD:
				#report error
				if self.POST_CRITICAL_ON_SLACK == True:
					if self.SLACK_TOKEN is not None:
						if self.SLACK_CHANNEL is not None:
							postOnSlack(self.SLACK_CHANNEL, 'EHM', "%s (%s) occured %s time(s)"%(error_message, error_code, self.CURRENT_CRITICAL_COUNT[error_code]), self.SLACK_TOKEN, error_type)
						else:
							print "[ EHM ERROR ] SLACK_CHANNEL not defined. Provide a valid SLACK_CHANNEL"
							ehmlog("[ EHM ERROR ] SLACK_CHANNEL not defined. Provide a valid SLACK_CHANNEL")	
					else:
						print "[ EHM ERROR ] SLACK_TOKEN not defined. Please provide a valid SLACK ACCESS TOKEN."
						ehmlog("[ EHM ERROR ] SLACK_TOKEN not defined. Please provide a valid SLACK ACCESS TOKEN.")

				logToFile(self.LOG_FILE, "%s (%s) occured %s time(s)"%(error_message, error_code, self.CURRENT_CRITICAL_COUNT[error_code]), error_type)
				logToScreen("%s (%s) occured %s time(s)"%(error_message, error_code, self.CURRENT_CRITICAL_COUNT[error_code]), error_type)
			else:
				#report error mention threshold limit reached
				if self.POST_CRITICAL_ON_SLACK == True:
					if self.SLACK_TOKEN is not None:
						if self.SLACK_CHANNEL is not None:
							postOnSlack(self.SLACK_CHANNEL, 'EHM', "%s (%s) occured %s time(s) [ THRESHOLD REACHED ]"%(error_message, error_code, self.CURRENT_CRITICAL_COUNT[error_code]), self.SLACK_TOKEN, error_type)
						else:
							print "[ EHM ERROR ] SLACK_CHANNEL not defined. Provide a valid SLACK_CHANNEL"
							ehmlog("[ EHM ERROR ] SLACK_CHANNEL not defined. Provide a valid SLACK_CHANNEL")
					else:
						print "[ EHM ERROR ] SLACK_TOKEN not defined. Please provide a valid SLACK ACCESS TOKEN."
						ehmlog("[ EHM ERROR ] SLACK_TOKEN not defined. Please provide a valid SLACK ACCESS TOKEN.")

				if self.SEND_EMAIL_ON_THRESHOLD_REACH == True:
					if self.EMAIL_PASSWORD == None or self.SENDING_EMAIL_ADDRESS == None:
						print "[ EHM ERROR ] Email Address/password not defined. Define SENDING_EMAIL_ADDRESS and EMAIL_PASSWORD"
						ehmlog("[ EHM ERROR ] Email Address/password not defined. Define SENDING_EMAIL_ADDRESS and EMAIL_PASSWORD")
						return
					if self.SMTP_HOST == None:
						print "[ EHM ERROR ] SMTP Configuration Error. Please define SMTP_HOST and SMTP_PORT"
						ehmlog("[ EHM ERROR ] SMTP Configuration Error. Please define SMTP_HOST and SMTP_PORT")
						return
					if self.EMAIL_ADDRESS == None:
						print "[ EHM ERROR ] Email Recipient not defined. Please Define EMAIL_ADDRESS"
						ehmlog("[ EHM ERROR ] Email Recipient not defined. Please Define EMAIL_ADDRESS")
						return

					body = 'THRESHOLD LIMIT for Error Code: %s reached. \nMessage: %s (%s) occured %s time(s) [ THRESHOLD REACHED ]\n\nThis Email was autogenerated By EHM'%(error_code, error_message, error_code, self.CURRENT_CRITICAL_COUNT[error_code])
					to = self.EMAIL_ADDRESS
					sender = self.SENDING_EMAIL_ADDRESS
					subject = "[ %s ] EHM ERROR CODE: %s"%(exeptionHandlingModule.EHM_APP_NAME, error_code)
					smtp_host = self.SMTP_HOST
					smtp_port = self.SMTP_PORT
					login = sender
					password = self.EMAIL_PASSWORD

					if self.EMAIL_SENT_STATUS[error_code] == False:
						sendEmail(body, to, sender, subject, smtp_host, smtp_port, login, password)
						self.EMAIL_SENT_STATUS[error_code] = True


				logToFile(self.LOG_FILE, "%s (%s) occured %s time(s) [ THRESHOLD REACHED ]"%(error_message, error_code, self.CURRENT_CRITICAL_COUNT[error_code]), error_type)
				logToScreen("%s (%s) occured %s time(s) [ THRESHOLD REACHED ]"%(error_message, error_code, self.CURRENT_CRITICAL_COUNT[error_code]), error_type)
				#do something to stop the script some how.

		elif error_type == exeptionHandlingModule.EHM_EXCEPTION_IGNORABLE:
			if self.POST_IGNORABLE_ON_SLACK == True:
					postOnSlack('mapping-app-testing', 'EHM', "%s (%s)"%(error_message, error_code), self.SLACK_TOKEN, error_type)
			logToFile(self.LOG_FILE, "%s (%s)"%(error_message, error_code), error_type)
			logToScreen("%s (%s)"%(error_message, error_code), error_type)

		elif error_type == exeptionHandlingModule.EHM_EXCEPTION_WARNING or error_type == exeptionHandlingModule.EHM_LOG:
			logToFile(self.LOG_FILE, "%s (%s)"%(error_message, error_code), error_type)
			logToScreen("%s (%s)"%(error_message, error_code), error_type)




	def __del__(self):
		class_name = self.__class__.__name__
		return class_name