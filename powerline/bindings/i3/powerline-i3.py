#!/usr/bin/env python
# vim:fileencoding=utf-8:noet

from powerline import Powerline
from powerline.lib.monotonic import monotonic

import sys
import time
import i3
from threading import Lock

name = 'wm'
if len( sys.argv ) > 1:
	name = sys.argv[1]
powerline = Powerline(name, renderer_module='i3bgbar')
powerline.update_renderer()

interval = 0.5

print '{"version": 1, "custom_workspace": true}'
print '['
print '	[[],[]]'

lock = Lock()

def render( event=None, data=None, sub=None ):
	global lock
	lock.acquire()
	s  = '[\n' + powerline.render(side='right')[:-2] + '\n]\n'
	s += ',[\n' + powerline.render(side='left' )[:-2] + '\n]'
	print ',[\n' + s + '\n]'
	sys.stdout.flush()
	lock.release()

sub = i3.Subscription( render, 'workspace' )

while True:
	start_time = monotonic()
	render()
	time.sleep(max(interval - (monotonic() - start_time), 0.1))
