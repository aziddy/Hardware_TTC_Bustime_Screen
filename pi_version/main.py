import pygame
import requests
import json
import math
import threading
import Queue
import time

pygame.init()
screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
pygame.font.init()
done = False

countdown_minus = 0

tempArray = []
TTCdata = []



print(TTCdata)

def async_ttc(q):
	print("async")
	r = requests.get('http://webservices.nextbus.com/service/publicJSONFeed?command=predictions&a=ttc&r=89&s=5847')

	countdown_minus = math.floor(time.clock())

	parsed_json = json.loads(r.content)

	tempArray = []
	TTCdata = []

	for g in range(len(parsed_json["predictions"]["direction"]["prediction"])):
		
		total_seconds = int(parsed_json["predictions"]["direction"]["prediction"][g]["seconds"])
		
		tempArray.append(total_seconds)

	TTCdata.append(["89 South", tempArray])
	
	
	
	r = requests.get('http://webservices.nextbus.com/service/publicJSONFeed?command=predictions&a=ttc&r=41&s=5847')
	parsed_json = json.loads(r.content)
	tempArray = []
	
	for g in range(len(parsed_json["predictions"]["direction"]["prediction"])):
		
		total_seconds = int(parsed_json["predictions"]["direction"]["prediction"][g]["seconds"])
		
		tempArray.append(total_seconds)

	TTCdata.append(["41 South", tempArray])
	
	
	q.put(TTCdata)
	q.put(countdown_minus)


q = Queue.Queue()

myfont = pygame.font.SysFont('arial', 30)



firstValFont = pygame.font.SysFont('arial', 40)
firstValFont.set_bold(True)
firstValFont.set_italic(True)


busfont = pygame.font.SysFont('arial', 30)
busfont.set_bold(True)
busfont.set_underline(True)

local_countdown_number = 0;

t = threading.Thread(target=async_ttc, args = (q,))
t.daemon = True
t.start()

def local_countdown():
	val = math.floor(time.clock() - countdown_minus)
	return val
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
			t = threading.Thread(target=async_ttc, args = (q,))
			t.daemon = True
			t.start()
			#print("a press")
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			done = True
	
	if pygame.mouse.get_pressed()[0]:
		#print ("You have opened a chest!")
		t = threading.Thread(target=async_ttc, args = (q,))
		t.daemon = True
		t.start()
	
	if local_countdown() > 59:
		t = threading.Thread(target=async_ttc, args = (q,))
		t.daemon = True
		t.start()
	
	screen.fill((250,250,250)) 
	
	#print(math.floor(local_countdown()))
	local_countdown_number = math.floor(time.clock())
	
	if not q.empty():
		TTCdata = q.get()
		countdown_minus = q.get()
    
	for t in range(len(TTCdata)):
		y = 40+(t*140)
		pygame.draw.rect(screen, (240, 240, 240), pygame.Rect(29, y-11, 743, 123))
		pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(30, y-10, 740, 120))
		screen.blit(busfont.render(TTCdata[t][0], False, (0, 0, 0)),(50,y))
		first = True;
		
		for k in range(len(TTCdata[t][1])):
			
			total_seconds = TTCdata[t][1][k] - local_countdown()
			
			timer_minutes = int(math.floor(total_seconds/60))
			timer_seconds = int((total_seconds - timer_minutes*60))
			
			if first:
				screen.blit(firstValFont.render(str(timer_minutes)+":"+str(timer_seconds), False, (80, 80, 80)),(100,y+50))
				first = False
			else:
				screen.blit(myfont.render(str(timer_minutes)+":"+str(timer_seconds), False, (80, 80, 80)),(200+(110*k),y+50))
	
	pygame.display.update()



	
	
	

	
	
	
	
	

