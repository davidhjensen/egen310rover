from subprocess import call

to_speak = "this is a test message from the pi I can say numbers like 75.46"

call(['espeak -ven-scottish -s140 ' + to_speak.replace(' ', '_') + ' 2>/dev/null &'], shell=True)
