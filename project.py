import sys
import json
import pygame
import argparse
from argparse import ArgumentParser

figures= []

def html_to_rgb(arg):
    if len(arg) != 7:
        raise ValueError("HTML color code has wrong length")
    return tuple(int(arg[i:i+2], 16) for i in (1, 3 ,5))
	
    
def get_color(arg):				#return tuple with RGB color
	 
	if (arg[0]=='(' and arg[-1]==')'):
		return tuple(map(lambda x: int(x), arg[1:-1].split(",")))
	if (arg[0]=='#'):
		return html_to_rgb(arg)
	else:
		return html_to_rgb(palette[arg])

		

class Screen:
    def __init__(self, height, width, fg_color, bg_color):  
		self.height = height
		self.width = width
		self.fg_color = fg_color
		self.bg_color = bg_color
	
    def prepare_screen(self):
		global win
		win = pygame.display.set_mode((self.width, self.height))
		win.fill(self.bg_color)
		
		
def process_screen(json_dict):
	try:
		width = json_dict['width']
		height = json_dict['height']
		fg_color = get_color(json_dict['fg_color'])
		bg_color = get_color(json_dict['bg_color'])

	except KeyError:
		print("Invalid key in screen")	
		sys.exit()
		
	global screen 
	screen = Screen(height, width, fg_color, bg_color)


class Point:   
    def __init__(self, point_dict):
		self.x = point_dict['x']
		self.y = point_dict['y']
		      
    def draw(self):
		global win
		pygame.draw.line(win, screen.fg_color, (self.x, self.y), (self.x, self.y))
		
		
class Polygon:
    def __init__(self, arg_dict):
		self.color = get_color(arg_dict['color'])
		self.points = arg_dict['points']
        
    def draw(self):
        pygame.draw.polygon(win, self.color, self.points, 0)
		
	

class Rectangle:
	def __init__(self, arg_dict):
		self.x = arg_dict['x']
		self.y = arg_dict['y']
		self.width = arg_dict['width']
		self.height = arg_dict['height']
		
	def draw(self):
		pygame.draw.rect(win, screen.fg_color, (self.x, self.y, self.width, self.height), 0)
		
		

class Circle:
	def __init__(self, arg_dict):
		self.x = arg_dict['x']
		self.y = arg_dict['y']
		self.radius = arg_dict['radius']
		self.color = get_color(arg_dict['color'])
		
	def draw(self):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 0)
		
		

class Square:
	def __init__(self, arg_dict):
		self.x = arg_dict['x']
		self.y = arg_dict['y']
		self.size = arg_dict['size']
		self.color = get_color(arg_dict['color'])
		
	def draw(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), 0)
		
		
		
	
def process_figures(json_dict):
	try: 
		for figure in json_dict:
			if figure['type'] == 'point':
				figures.append(Point(figure))
			if figure['type'] == 'polygon':
				figures.append(Polygon(figure))
			if figure['type'] == 'rectangle':
				figures.append(Rectangle(figure))
			if figure['type'] == 'square':
				figures.append(Square(figure))
			if figure['type'] == 'circle':
				figures.append(Circle(figure))
			
	except KeyError:
		print("Invalid figure type")	
		sys.exit(1)
		
	
	
def parse_json_file(fname):   
		global json_file
		try:
			with open(fname, 'r') as json_file:
				json_data = json.load(json_file)
				for key, value in json_data.items():			
					if key == 'Screen': 
						screen_dict = value 
					elif key == 'Figures':
						fig = value
					elif key == 'Palette':
						global palette
						palette = value
					else:
						raise NameError()
						
				process_screen(screen_dict)
				process_figures(fig)
				return file
				
		except IOError:
			print('Error on opening file')
			sys.exit()
		except KeyKError:
			print("Invalid key in json file")	
			sys.exit()  
		except json.JSONDecodeError:
			print("Invalid JSON file")

	
def main():
	
	parser = ArgumentParser()
	parser.add_argument('input', help= 'input file name')
	parser.add_argument('-o', '--output', default=argparse.SUPPRESS, help= 'specify output file name to save result')			

	if (len(sys.argv) < 2 or len(sys.argv) >4):
		parser.print_help()
		return
	
	else:			
		parse_json_file(sys.argv[1])
		screen.prepare_screen()
		
		for figure in figures:
			figure.draw()
			
			
		pygame.display.flip() 
		raw_input("Press Enter to continue...")
		

		if (len(sys.argv) == 4):
			pygame.image.save(win, sys.argv[3])
		
		json_file.close()
      
	    	
		
if __name__ == "__main__":
    main()
