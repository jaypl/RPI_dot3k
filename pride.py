#!/usr/bin/env python
import dot3k.lcd as lcd
import dot3k.backlight as backlight
import time, datetime, copy, math, psutil
import time
from datetime import datetime, timedelta


lcd.write(chr(0) + 'Yay LGBT Pride!')# + chr(0))
lcd.set_cursor_position(0,2)
lcd.write(' Party hrs left ')# + chr(3) + chr(2) + chr(5))

eqlchar = [
	[0x0,0x1f,0x1f,0x0,0x0,0x1f,0x1f,0x0], #=
	[0x0,0x0,0x1f,0x1f,0x0,0x0,0x1f,0x1f], #= move
	[0x0,0x1f,0x1f,0x0,0x0,0x1f,0x1f,0x0], #= move
	[0x1f,0x1f,0x0,0x0,0x1f,0x1f,0x0,0x0], #= move
	[0x1f,0x1f,0x1b,0x1b,0x1f,0x1f,0x18,0x18], #P
	[0x1f,0x1f,0x1b,0x1b,0x1f,0x1f,0x1a,0x19], #R
	[0x1f,0x1f,0xe,0xe,0xe,0xe,0x1f,0x1f], #I
	[0x1e,0x1f,0x1b,0x1b,0x1b,0x1b,0x1f,0x1e], #D
	[0x1f,0x1f,0x18,0x1e,0x1e,0x18,0x1f,0x1f] #E
] #WHADDOESTHATSPELL??  Pride!

def getAnimFrame(char,fps):
	return char[ int(round(time.time()*fps) % len(char)) ]

cpu_sample_count = 200
cpu_samples = [0] * cpu_sample_count
hue = 0.0
while True:
	hue += 0.008
	backlight.sweep(hue)

	cpu_samples.append(psutil.cpu_percent() / 100.0)
	cpu_samples.pop(0)

	cpu_avg = sum(cpu_samples) / cpu_sample_count
	backlight.set_graph(cpu_avg)

	lcd.create_char(0,getAnimFrame(eqlchar,2))

	if hue > 1.0:
		hue = 0.0

	lcd.set_cursor_position(0,1)
	t = datetime.now().strftime("%H:%M:%S.%f")
	deploy = datetime(2015, 7, 1, 0, 0)
	timestamp = time.mktime(deploy.timetuple())
	deploy_utc = datetime.utcfromtimestamp(timestamp)
	elapsed = deploy_utc - datetime.utcnow()	
	trunc_micros = timedelta(days=elapsed.days, seconds=elapsed.seconds) 
	seconds = elapsed.days*86400 + elapsed.seconds
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	lcd.write(("{hours:02d}:{minutes:02d}:{seconds:02d}".format(**vars())))

	time.sleep(0.005)
