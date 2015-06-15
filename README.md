# Exception Handling Module (EHM)
### Description
Exception reporting module for python. This is useful for long running scripts as it allows the user to get notified by mail or on a Slack Channel if a specific error is happening too often in his python script.

### Usage
Place ehm.py in your script folder and then import it as follows
```
import ehm
```
You can instantiate an EHM object as Follows
```
obj = ehm.exeptionHandlingModule('Application Name')
```

###Editable Options
* SLACK_TOKEN (Access token for posting notifications on slack channel)
* CRITICAL_ERROR_THRESHOLD (Threshold limit which defines when to nofify via Email or Slack)
* LOG_FILE ('full path/name' of log file to log through EHM. Default is 'EHM_log.log' in the same directory)
* POST_CRITICAL_ON_SLACK (Boolean : flag to turn on slack notifications for critical errors. Note: SLACK_TOKEN and SLACK_CHANNEL must be defined)
* POST_IGNORABLE_ON_SLACK (Boolean : flag to turn on slack notifications for ignorable errors.)
* SEND_EMAIL_ON_THRESHOLD_REACH (Boolean : Flag to turn on email notification on threshold limit reach)
* SMTP_HOST (smtp server host)
* SMTP_PORT (port for smtp server)
* SENDING_EMAIL_ADDRESS (email to use for sending notifications)
* EMAIL_PASSWORD (password for email address)
* EMAIL_ADDRESS (email address on which notifications will be sent)
* SLACK_CHANNEL (slack channel on which notifications will be sent)

You can set an attribute as following:
```
obj.set(attributeName::String, Value);
```
For Example:
```
obj.set('LOG_FILE', '/home/PC/test-app/ehm.log');
```
