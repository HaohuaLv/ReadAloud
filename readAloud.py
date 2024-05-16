import multiprocessing
from multiprocessing import *
import pyttsx3
from threading import Thread
import keyboard
import pyperclip
import time

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

def speak(phrase, volume, rate):
    engine.setProperty("volume", volume)
    engine.setProperty("rate", rate)
    engine.say(phrase)
    engine.runAndWait()
    

def stop_speaker():
    global term
    term = True
    t.join()

@threaded
def manage_process(p):
	global term
	global speaking
	while p.is_alive():
		if term:
			p.terminate()
			term = False
		else:
			continue
	speaking = False

	
def say(phrase):
	global t
	global term
	global speaking
	global volume
	global rate
	speaking = True
	term = False
	p = multiprocessing.Process(target=speak, args=(phrase, volume, rate))
	p.start()
	t = manage_process(p)
		
engine = pyttsx3.init()
speaking = False
volume, rate = 1.0, 250


if __name__ == "__main__":
	multiprocessing.freeze_support()
	while True:
		if keyboard.is_pressed("Alt+Shift+A"):
			paste_bk = pyperclip.paste()
			# copy current selected text
			keyboard.release("Alt+Shift+A")
			keyboard.press("Ctrl+c")
			keyboard.release("Ctrl+c")
			time.sleep(0.1)
			text = pyperclip.paste()
			pyperclip.copy(paste_bk)
			if speaking:
				stop_speaker()
				say(text)
			if not speaking:
				say(text)
    
		elif keyboard.is_pressed("Alt+Shift+S"):
			if speaking:
				stop_speaker()
    
		elif keyboard.is_pressed("Alt+Shift+="):
			volume += 0.1
			if speaking:
				stop_speaker()
				say("测试音量")
			if not speaking:
				say("测试音量")

		elif keyboard.is_pressed("Alt+Shift+-"):
			volume -= 0.1 if volume >= 0.2 else volume
			if speaking:
				stop_speaker()
				say("测试音量")
			if not speaking:
				say("测试音量")

		elif keyboard.is_pressed("Alt+Shift+]"):
			rate += 50
			if speaking:
				stop_speaker()
				say("测试语速")
			if not speaking:
				say("测试语速")

		elif keyboard.is_pressed("Alt+Shift+["):
			rate -= 50 if rate >= 50 else rate
			if speaking:
				stop_speaker()
				say("测试语速")
			if not speaking:
				say("测试语速")
    
		elif keyboard.is_pressed("Alt+Shift+Q"):
			if speaking:
				stop_speaker()
			engine.stop()
			break
		
		time.sleep(0.1)