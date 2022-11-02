#Bren Jay Magtalas 2018-07503
import pygame
import sys
import os
import random
class SPG:
	def __init__(self,grid,tile,spacing):
		self.grid=grid
		self.tile=tile
		self.spacing=spacing
		tiles=[]
		tilecoord={}
		for y in range(grid[1]):
			for x in range(grid[0]):
				tiles.append((x,y))
		for y in range(grid[1]):
			for x in range(grid[0]):
				tilecoord[(x,y)]=(x*(tile+spacing)+spacing,y*(tile+spacing)+spacing)
		self.tiles=tiles #list of position
		self.tilecoord=tilecoord #dictionary with position and actual coords
		self.tilesdummy=[]#dummy tiles are for showing the solved state at the beginning and also getting the winning order of list of tiles
		self.tilecoorddummy={}
		for x in tiles:
			if x[0]!=0 and x[1]!=0 and x[0]!=grid[0]-1 and x[1]!=grid[1]-1:
				self.tilesdummy.append(x)
		for x,y in tilecoord.items():
			if x[0]!=0 and x[1]!=0 and x[0]!=grid[0]-1 and x[1]!=grid[1]-1:
				self.tilecoorddummy[x]=y
		self.tilenum=((grid[0]-2)*(grid[1]-2))
		self.wintiles=self.tilesdummy[:self.tilenum]
		self.font=pygame.font.Font('uni0553-webfont.ttf',60)
		pic=[]
		colors={1:(255,0,0),2:(255,255,0),3:(0,0,255),4:(0,128,0),5:(255,255,255),6:(255,165,0)}
		ctr=1
		for num in range(self.tilenum):#Assigning colors
			image=pygame.Surface((tile,tile))
			if ctr<=grid[1]-2:
				image.fill(colors[1])
			elif ctr<=(grid[1]-2)*2:
				image.fill(colors[2])
			elif ctr<=(grid[1]-2)*3:
				image.fill(colors[3])
			elif ctr<=(grid[1]-2)*4:
				image.fill(colors[4])
			elif ctr<=(grid[1]-2)*5:
				image.fill(colors[5])
			elif ctr<=(grid[1]-2)*6:
				image.fill(colors[6])
			text=self.font.render(str(num+1),2,(0,0,0))
			wtxt,htxt=text.get_size()
			image.blit(text,((tile-wtxt)/2,(tile-htxt)/2))
			pic+=[image]
			ctr+=1
		self.pic=pic
		self.indicator=True
		self.left=False
		self.right=False
		self.up=False
		self.down=False
		self.clicked=False
	def slide(self,Tile,Tile2):#my idea is to have a list that contains all the tiles and opentiles
	#the movement is actually just swapping of the index of the list of tiles
	#I also swap and store values in opentile to identify which tile is open
		if self.Tile not in self.opentile and Tile2 in self.opentile:
			self.tiles[self.tiles.index(Tile2)]=self.tiles[self.tiles.index(self.Tile)]
			self.tiles[self.tiles.index(self.Tile)]=self.opentile[self.opentile.index(Tile2)]
			self.opentile[self.opentile.index(Tile2)]=self.Tile
		elif Tile2 not in self.opentile and self.Tile in self.opentile:
			Tiletest=self.tiles[self.tiles.index(Tile2)]
			self.tiles[self.tiles.index(Tile2)]=self.opentile[self.opentile.index(self.Tile)]
			self.tiles[self.tiles.index(self.Tile)]=Tiletest
			self.opentile[self.opentile.index(self.Tile)]=Tile2
		elif self.Tile not in self.opentile and Tile2 not in self.opentile:
			Tiletest=self.tiles[self.tiles.index(Tile)]
			self.tiles[self.tiles.index(self.Tile)]=self.tiles[self.tiles.index(Tile2)]
			self.tiles[self.tiles.index(Tile2)]=Tiletest
		elif self.Tile in self.opentile and Tile2 in self.opentile:
			Tiletest=self.opentile[self.opentile.index(self.Tile)]
			self.opentile[self.opentile.index(self.Tile)]=self.opentile[self.opentile.index(Tile2)]
			self.opentile[self.opentile.index(Tile2)]=Tiletest
	def inGrid(self,Tile):
		return Tile[0]>=0 and Tile[0]<self.grid[0] and Tile[1]>=0 and Tile[1]<self.grid[1]
	def random(self):
		#randomize the tiles but i decided to exclued the last tile for convinence because if it happends that the 4
		#corner tiles are filled, the puzzle can't be moved
		tile=self.tiles[-1]
		self.tiles=self.tiles[:-1]
		random.shuffle(self.tiles)
		self.tiles.append(tile)
	def reload(self):
		genclick=pygame.mouse.get_pressed()
		self.mcoord=pygame.mouse.get_pos()
		if genclick[0]:
			x,y=self.mcoord[0]%(self.tile+self.spacing),self.mcoord[1]%(self.tile+self.spacing)#simplify the coordinates to easily tell if the clicked position is a tile
			if x>self.spacing and y>self.spacing:
				self.Tile=self.mcoord[0]//self.tile,self.mcoord[1]//self.tile#decompose the coordinate in actual elements that are in the list of tiles
				if self.inGrid(self.Tile):
					if self.Tile not in self.opentile:
						a=self.Tile[0]
						c=a-1
						d=a+1
						b=self.Tile[1]
						e=b-1
						f=b+1
						if a==0:#validations if the tile can be moved/ is beside an opentile
						#colums/rows can only be moved if the tile nearest to an opentile with no obstruction is selected
							self.left=False
						else:
							self.left=True
							while c>-1:
								if (c,self.Tile[1]) not in self.opentile:
									self.left=False
									c=-1
								c-=1
						if a==self.grid[0]-1:
							self.right=False
						else:
							self.right=True
							while d<self.grid[0]:
								if (d,self.Tile[1]) not in self.opentile:
									self.right=False
									d=self.grid[0]
								d+=1
						if b==0:
							self.up=False
						else:
							self.up=True
							while e>-1:
								if (self.Tile[0],e) not in self.opentile:
									self.up=False
									e=-1
								e-=1
						if b==self.grid[0]-1:
							self.down=False
						else:
							self.down=True
							while f<self.grid[0]:
								if (self.Tile[0],f) not in self.opentile:
									self.down=False
									f=self.grid[0]
								f+=1
						self.clicked=True
						clicked=self.clicked
						return(clicked)
	def show(self,screen,c):#the tiles that have colors are actually the elements of the list from index zero up to the index of the number of total colored tiles
		if self.indicator:
			for num in range(self.tilenum):
				x,y=self.tilecoorddummy[self.tilesdummy[num]]
				screen.blit(self.pic[num],(x,y))
				subfont=pygame.font.Font('uni0553-webfont.ttf',30)
				subtext=subfont.render('Press SPACE to start',2,(255,255,255))
				subwtxt,subhtxt=subtext.get_size()
				screen.blit(subtext,((c-subwtxt)/2,(60-subhtxt)/2))
		else:
			for num in range(self.tilenum):
				x,y=self.tilecoord[self.tiles[num]]
				screen.blit(self.pic[num],(x,y))
	def randomize(self):#opentiles are the elements of the list of tiles with index greater the number of total colored tiles
	#the indicator tells the show function if the tiles are already randomized
		self.random()
		self.indicator=False
		self.opentile=self.tiles[self.tilenum:]
	def events(self,event):
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_LEFT:#direction of movement
				if self.left:
					try:
						Tile2=self.mcoord[0]//self.tile-1,self.mcoord[1]//self.tile
						q=self.mcoord[0]//self.tile-1
						while q<self.grid[0]:
							self.slide(self.Tile,Tile2)
							Tile2=self.Tile
							q+=1
							self.Tile=q,self.mcoord[1]//self.tile
					except:
						lol=False
			elif event.key==pygame.K_RIGHT:
				if self.right:
					try:
						Tile2=self.mcoord[0]//self.tile+1,self.mcoord[1]//self.tile
						q=self.mcoord[0]//self.tile+1
						while q>=0:
							self.slide(self.Tile,Tile2)
							Tile2=self.Tile
							q-=1
							self.Tile=q,self.mcoord[1]//self.tile
					except:
						lol=False
			elif event.key==pygame.K_UP:
				if self.up:
					try:
						Tile2=self.mcoord[0]//self.tile,self.mcoord[1]//self.tile-1
						q=self.mcoord[1]//self.tile-1
						while q<self.grid[1]:
							self.slide(self.Tile,Tile2)
							Tile2=self.Tile
							q+=1
							self.Tile=self.mcoord[0]//self.tile,q
					except:
						lol=False
			elif event.key==pygame.K_DOWN:
				if self.down:
					try:
						Tile2=self.mcoord[0]//self.tile,self.mcoord[1]//self.tile+1
						q=self.mcoord[1]//self.tile+1
						while q>=0:
							self.slide(self.Tile,Tile2)
							Tile2=self.Tile
							q-=1
							self.Tile=self.mcoord[0]//self.tile,q
					except:
						lol=False
			self.win()
	def win(self):#winning condition
		if self.tiles[:self.tilenum]==self.wintiles:
			return(True)
pygame.init()#initialization
os.environ['SDL_VIDEO_CENTERED']='1'
pygame.display.set_caption('Sliding Puzzle Game')
mainscreen=pygame.display.set_mode((800,800))
while True:#startscreen
	mainscreen.fill((0,0,0))
	mainfont=pygame.font.Font('uni0553-webfont.ttf',60)
	maintext=mainfont.render('Start Game',2,(255,255,255))
	mainwtxt,mainhtxt=maintext.get_size()
	mainscreen.blit(maintext,((800-mainwtxt)/2,(800-mainhtxt)/2))
	pygame.display.flip()
	x=True
	while x:#gameguide
		for event in pygame.event.get():
				if event.type==pygame.KEYDOWN:
					x=False
					mainscreen.fill((0,0,0))
					mainfont=pygame.font.Font('uni0553-webfont.ttf',30)
					maintext=mainfont.render('How to play?',2,(255,255,255))
					mainwtxt,mainhtxt=maintext.get_size()
					mainscreen.blit(maintext,((800-mainwtxt)/2,(60-mainhtxt)/2))
					subtexts=mainfont.render('Click and hold the tile to select',2,(255,255,255))
					mainwtxts,mainhtxts=subtexts.get_size()
					subtexts1=mainfont.render('then specify the direction using arrow keys',2,(255,255,255))
					mainwtxt1,mainhtxt1=subtexts1.get_size()
					subtexts2=mainfont.render('to move the column/row to the nearest opentile',2,(255,255,255))
					mainwtxt2,mainhtxt2=subtexts2.get_size()
					mainscreen.blit(subtexts,((800-mainwtxts)/2,(475-mainhtxts)/2))
					mainscreen.blit(subtexts1,((800-mainwtxt1)/2,(575-mainhtxt1)/2))
					mainscreen.blit(subtexts2,((800-mainwtxt2)/2,(675-mainhtxt2)/2))
					pygame.display.flip()
					z=True			
	while z:#choosing grid size
		for event in pygame.event.get():
			if event.type==pygame.KEYDOWN:
				mainscreen.fill((0,0,0))
				main1font=pygame.font.Font('uni0553-webfont.ttf',60)
				main1image=pygame.Surface((800,200))
				main1image.fill((0,255,0))
				main1text=main1font.render('3 x 3',2,(255,255,255))
				main1wtxt,main1htxt=main1text.get_size()
				main1image.blit(main1text,((800-main1wtxt)/2,(200-main1htxt)/2))
				mainscreen.blit(main1image,(0,0))
				main2image=pygame.Surface((800,200))
				main2image.fill((255,255,0))
				main2text=main1font.render('4 x 4',2,(255,255,255))
				main2image.blit(main2text,((800-main1wtxt)/2,(200-main1htxt)/2))
				mainscreen.blit(main2image,(0,200))
				main3image=pygame.Surface((800,200))
				main3image.fill((0,0,255))
				main3text=main1font.render('5 x 5',2,(255,255,255))
				main3image.blit(main3text,((800-main1wtxt)/2,(200-main1htxt)/2))
				mainscreen.blit(main3image,(0,400))
				main4image=pygame.Surface((800,200))
				main4image.fill((255,0,0))
				main4text=main1font.render('6 x 6',2,(255,255,255))
				main4image.blit(main4text,((800-main1wtxt)/2,(200-main1htxt)/2))
				mainscreen.blit(main4image,(0,600))
				pygame.display.flip()
			maingenclick=pygame.mouse.get_pressed()
			mainmcoord=pygame.mouse.get_pos()
			if maingenclick[0]:
				mainx,mainy=mainmcoord[0],mainmcoord[1]
				if mainx>0 and mainx<800:
					if mainy>0 and mainy<200:
						a=5
						z=False
					elif mainy>200 and mainy<400:
						a=6
						z=False
					elif mainy>400 and mainy<600:
						a=7
						z=False
					elif mainy>600 and mainy<800:
						a=8
						z=False
	start=True
	w=False
	b=120
	c=a*b+((a+1)*3)
	screen=pygame.display.set_mode((c,c))
	game=SPG((a,a),b,3)
	while start:#main game
		screen.fill((0,0,0))
		game.show(screen,c)
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				sys.exit
			if w:	
				if game.reload():
					game.events(event)
			else:
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_SPACE:
						game.reload()
						game.randomize()
						w=True
		if game.win():
			p=True
			mainscreen=pygame.display.set_mode((800,800))
			while p:#winning screen
				screen.fill((0,0,0))
				mainfont=pygame.font.Font('uni0553-webfont.ttf',60)
				maintext=mainfont.render('You Won!',2,(255,255,255))
				mainwtxt,mainhtxt=maintext.get_size()
				screen.blit(maintext,((800-mainwtxt)/2,(800-mainhtxt)/2))
				subfont=pygame.font.Font('uni0553-webfont.ttf',30)
				subtext=subfont.render('Press any key to play again',2,(255,255,255))
				subwtxt,subhtxt=subtext.get_size()
				screen.blit(subtext,((800-subwtxt)/2,(60-subhtxt)/2))
				pygame.display.flip()
				for event in pygame.event.get():
					if event.type==pygame.KEYDOWN:
						start=False
						p=False


