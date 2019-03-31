#!/usr/bin/env python
#__*__ coding: utf-8 __*__

import pygame,sys,time,random
from pygame.locals import *
import QL

redColour = pygame.Color(255,0,0)
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
greenColour = pygame.Color(0,255,0)
greyColour = pygame.Color(200,200,200)

def show_text(screen, pos, text, color, font_bold = False, font_size = 60, font_italic = False):

    cur_font = pygame.font.SysFont("宋体", font_size)
    cur_font.set_bold(font_bold)
    cur_font.set_italic(font_italic)
    text_fmt = cur_font.render(text, 1, color)
    screen.blit(text_fmt, pos)

def paint_background(playSurface, tabu_table, raspberryPosition, block_width):
	playSurface.fill(whiteColour)

	for position in tabu_table:
		pygame.draw.rect(playSurface, blackColour,
						 Rect(position[0] * block_width, position[1] * block_width, block_width, block_width))
	pygame.draw.rect(playSurface, redColour,
					 Rect(raspberryPosition[0] * block_width, raspberryPosition[1] * block_width, block_width,
						  block_width))


def main():

	block_width = 40
	tabu_table = [[3, idx] for idx in range(0,5)] + [[7, idx] for idx in range(4,10)]
	snakePosition = [0,0]
	# snakeSegments = [[5,5],[4,5],[3,5]]
	raspberryPosition = [9, 9]

	height = 10
	weight = 10

	pygame.init()
	playSurface = pygame.display.set_mode((weight*block_width, height*block_width))
	fpsClock = pygame.time.Clock()
	pygame.display.set_caption('Snake HEGSNS')

	a_starobj = QL.Q_brain()
	while True:
		paint_background(playSurface, tabu_table, raspberryPosition, block_width)
		pygame.draw.rect(playSurface, greenColour, Rect(snakePosition[0] * block_width, snakePosition[1] * block_width, block_width, block_width))
		show_text(playSurface, (50, 50), 'Calculating... ', (255, 0, 0))
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

		# Q learning
		while True:
			a_starobj.__init__(tabu_table, 0.99, 0.9)
			print('Training ...')
			a_starobj.training(snakePosition, raspberryPosition, 500)
			if a_starobj.exist_route(snakePosition, raspberryPosition):
				route = a_starobj.__route__()
				print('route useful')
				break
			print('route invalid')

		paint_background(playSurface, tabu_table, raspberryPosition, block_width)
		pygame.draw.rect(playSurface, greenColour, Rect(snakePosition[0] * block_width, snakePosition[1] * block_width, block_width, block_width))
		pygame.display.flip()

		# draw route
		for idx in range(len(route)):
			if idx == 0 or idx == len(route)-1:
				continue
			position = route[idx]
			pygame.draw.rect(playSurface, greyColour, Rect(position[0] * block_width, position[1] * block_width, block_width, block_width))
		pygame.display.flip()

		for loc_idx in range(1, len(route)):
			snakePosition_last = [x for x in route[loc_idx-1]]
			snakePosition = [x for x in route[loc_idx]]
			# 刷新pygame显示层
			pygame.draw.rect(playSurface, whiteColour, Rect(snakePosition_last[0] * block_width, snakePosition_last[1] * block_width, block_width,
								  block_width))
			pygame.draw.rect(playSurface, greenColour, Rect(snakePosition[0] * block_width, snakePosition[1] * block_width, block_width,
								  block_width))
			pygame.display.flip()
			fpsClock.tick(5)

		a_starobj.clear_history()

		while True:
			x = random.randrange(0, 9)
			y = random.randrange(0, 9)
			if [x, y] not in tabu_table:
				break
		raspberryPosition = [int(x), int(y)]

	return


if __name__ == "__main__":
	main()