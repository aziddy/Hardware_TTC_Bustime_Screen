import pygame
import requests
import json
import math
import threading
import queue
import time

pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.font.init()
done = False


r = requests.get('http://webservices.nextbus.com/service/publicJSONFeed?command=predictions&a=ttc&r=89&s=5847')

parsed_json = json.loads(r.content)

TTCdata = []

#print(parsed_json["predictions"]["direction"]["title"])



tempArray = []

for g in range(len(parsed_json["predictions"]["direction"]["prediction"])):
	
	tempArray.append([int(parsed_json["predictions"]["direction"]["prediction"][g]["minutes"]), (int(parsed_json["predictions"]["direction"]["prediction"][g]["seconds"]) - int(parsed_json["predictions"]["direction"]["prediction"][g]["minutes"])*60)])

TTCdata.append([parsed_json["predictions"]["direction"]["title"],tempArray])

print(TTCdata)


txt = "aaaa"

def client_side_countdown():
	print("ayyy")
	
def async_ttc(q):
	print("async")
	r = requests.get('http://webservices.nextbus.com/service/publicJSONFeed?command=predictions&a=ttc&r=89&s=5847')

	parsed_json = json.loads(r.content)
	TTCdata = []

	tempArray = []

	for g in range(len(parsed_json["predictions"]["direction"]["prediction"])):
		
		tempArray.append([int(parsed_json["predictions"]["direction"]["prediction"][g]["minutes"]), (int(parsed_json["predictions"]["direction"]["prediction"][g]["seconds"]) - int(parsed_json["predictions"]["direction"]["prediction"][g]["minutes"])*60)])

	TTCdata.append([parsed_json["predictions"]["direction"]["title"],tempArray])
	q.put(TTCdata)


q = queue.Queue()

myfont = pygame.font.SysFont('Impact', 30)

local_countdown_number = 0;

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
			t = threading.Thread(target=async_ttc, args = (q,))
			t.daemon = True
			t.start()
			print("a press")
			
			
	
	screen.fill((0,0,0)) 
	
	print(math.floor(time.clock()))
	local_countdown_number = math.floor(time.clock())
	
	if not q.empty():
		TTCdata = q.get()
    
	for t in range(len(TTCdata)):
		for k in range(len(TTCdata[t][1])):
			screen.blit(myfont.render(str(TTCdata[t][1][k][0])+":"+str(TTCdata[t][1][k][1]), False, (255, 0, 0)),(100+(70*k),100))
    
	#screen.blit(myfont.render('ello', False, (255, 0, 0)),(100,100))
	pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(30, 30, 60, 60))
	screen.blit(myfont.render(txt, False, (255, 0, 0)),(170,180))
	
	pygame.display.update()

	
	
	

	
	
	
	
	

