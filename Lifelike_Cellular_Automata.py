import pygame as pg
import sys,random,math
from pygame.locals import *
pg.init()

#Colours
RED, YELLOW = (231, 76, 60), (247, 201, 72)        # red, gold
GREEN = (96, 190, 140)                             # green
TEXT, MUTED, PANEL = (240, 242, 248), (150, 160, 190), (40, 46, 78)
DARK_TEXT = (24, 28, 46)
WHITE, BLACK, BLUE = (255, 255, 255), (0, 0, 0), (0, 0, 255)  
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (128,128,128)
BG = (47, 80, 80)

size = width, height = 1280,720 # screen size
colour = (10, 0, 0) # background colour


screen = pg.display.set_mode(size, pg.SCALED | pg.RESIZABLE)
clock = pg.time.Clock()

# colour stuff 
def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def lighten(c, t=0.2):
    return mix(c, (255, 255, 255), t)
def darken(c, t=0.2):
    return mix(c, (0, 0, 0), t)

class Button(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, text,colour = (255, 255, 0),alpha = 255):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.x =x
        self.y = y
        self.colour = colour
        self.alpha = alpha

    def draw(self, screen, font_size=40):
        #pg.draw.rect(screen,self.colour, self.rect)
        surface = pg.Surface(self.rect.size)
        surface.fill(self.colour)
        surface.set_alpha(self.alpha)
        screen.blit(surface, self.rect.topleft)
        font = pg.font.SysFont(None, font_size)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    
    def is_clicked(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse_x, mouse_y) and pg.mouse.get_pressed()[0]
    def is_hovered(self):
        return self.rect.collidepoint(pg.mouse.get_pos())
    
    def change_text(self,text):
        self.text = text

class Slider(pg.sprite.Sprite): 
    def __init__(self, position: tuple[int, int], width: int,length, colour: tuple[int, int, int] = (255, 0, 0)):
        super().__init__()
        self.length = length 
        self.width = width
        self.colour = colour
        self.dragging = False
        
        self.x, self.y = position
        self.pos = pg.math.Vector2(self.x, self.y)
        
        self.image = pg.Surface((self.width, self.length))
        self.image.fill((200, 200, 200)) # Grey track
        self.rect = self.image.get_rect(topleft=self.pos)
        self.radius = (self.length *1.5) // 2
        self.sliderpos = pg.math.Vector2(self.x , self.y + (self.length // 2))
        self.sliderrect = pg.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.sliderrect.center = (int(self.sliderpos.x), int(self.sliderpos.y))
               
    def move_slider(self, mouse_pos: tuple[int, int]):
        mouse_x = mouse_pos[0]
        if self.x <= mouse_x <= (self.x + self.width):
            self.sliderpos.x = mouse_x
            self.sliderrect.center = (int(self.sliderpos.x), int(self.sliderpos.y))

    def scroll(self,scroll):
        if self.x <= self.sliderpos.x <= (self.x + self.width):
            self.sliderpos.x += scroll
            
            if self.sliderpos.x > (self.x+self.width):
                self.sliderpos.x = self.width + self.x
            elif self.sliderpos.x < (self.x):
                self.sliderpos.x = self.x
            
            self.sliderrect.center = (int(self.sliderpos.x), int(self.sliderpos.y))
    def draw_slider(self, surface: pg.Surface):
        pg.draw.circle(surface, self.colour, (int(self.sliderpos.x), int(self.sliderpos.y)), self.radius)
 
    def is_hovered(self):
        return self.sliderrect.collidepoint(pg.mouse.get_pos())
    
    def percentage(self):
        return int((self.sliderpos.x-self.x)/(self.width)*100)

class Node(pg.sprite.Sprite):
    def __init__(self,x,y,size,node_x,node_y,colour=(255,255,255)):
        super().__init__()
        self.x = node_x
        self.y = node_y
        self.size = size
        self.colour = colour
        self.state = 0
        self.image = pg.Surface((size,size))
        self.image.fill(self.colour)
        self.pos = pg.math.Vector2(x,y)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.next_colour = self.colour
        self.survival = self.state
        
    def start(self):
        self.state = random.randint(0,1)
        self.survival = self.state
        states = [BLACK,WHITE]
        self.colour = states[self.state]
        self.next_colour = self.colour
        self.image.fill(self.colour)
    def next_state(self,inputs: list,parameters: tuple):
        spawn_rules,survive_rules = parameters
        if self.state == 0: #spawn
            for num in spawn_rules:
                if sum(inputs) == num:
                    self.survival = 1
                    self.next_colour = WHITE
                    break
                else:
                    self.survival = 0
                    self.next_colour = BLACK
        elif self.state == 1: # survive
            for num in survive_rules:
                if sum(inputs) == num:
                    self.survival = 1
                    self.next_colour = WHITE
                    break
                else:
                    self.survival = 0
                    self.next_colour = BLACK

    def change_state(self,state= None):
        if state is None:
            if self.state == 0:
                self.survival = 1
                self.next_colour = WHITE
            elif self.state == 1:
                self.survival = 0
                self.next_colour = BLACK       
        else:
            self.survival = state
            if state == 0:
                self.next_colour = BLACK
            elif state == 1:
                self.next_colour = WHITE
        
        self.update()

    def update(self):
        self.state = self.survival
        self.colour = self.next_colour
        self.image.fill(self.colour)

class Graph():
    def __init__(self,node_size,graph_x,graph_y):
        self.size = graph_x * graph_y
        self.x = graph_x
        self.y = graph_y
        self.node_size = node_size
        self.nodes = []
        for y in range(graph_y):
            nodes = []
            for x in range(graph_x):
                nodes.append(Node(x * self.node_size,y * self.node_size ,self.node_size,x,y))
            self.nodes.append(nodes)
    def start(self):
        for nodes in self.nodes:
            for node in nodes:
                node.start()
    def update(self,survival_group,spawn_group):
        survive = []
        spawn = []
        for box in survival_group:
            if box.state == 1:
                survive.append(int(box.label))
        if len(survive) == 0: survive.append(0)
        for box in spawn_group:
            if box.state == 1:
                spawn.append(int(box.label))  
        if len(spawn) == 0: spawn.append(0)
                    
        for nodes in self.nodes:
            for node in nodes:
                column = node.x
                row = node.y
                #inputs = [up,down,left,rigth,upleft,upright,downleft,downright]
                """
                Grid-neighbour traversal algorithm
                """
                directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
                states = []
                for deltar, deltac in directions:
                    new_row, new_column = row + deltar, column + deltac # update new rows
                    if 0 <= new_row < self.y and 0 <= new_column < self.x: # check if in bounds
                        states.append(self.nodes[new_row][new_column].state)
                node.next_state(states,(spawn,survive))           
        for nodes in self.nodes:
            for node in nodes:
                node.update()

class Checkbox(Button):
    def __init__(self,x,y,side_length,label= None):
        super().__init__(x,y,side_length,side_length,label)
        self.state = 0
        self.colour = RED
        self.label = label
        self.alpha = 50
        
    def draw(self, screen):
        #pg.draw.rect(screen, self.colour, self.rect)
        surface = pg.Surface(self.rect.size)
        surface.fill(self.colour)
        surface.set_alpha(self.alpha)
        screen.blit(surface, self.rect.topleft)
        
        if self.label is not None:
            font = pg.font.SysFont(None, 30)
            text_surf = font.render(self.text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=self.rect.center) 
            screen.blit(text_surf, text_rect)
        
    def is_clicked(self):
        if super().is_clicked():
            if self.state == 0:
                self.state = 1
                self.colour = GREEN
                return True
            elif self.state == 1:
                self.state = 0
                self.colour = RED
        else: 
            return False
    
    def change_state(self,state):
        self.state = state
        if self.state == 0:
                self.colour = RED
        elif self.state == 1:
                self.colour = GREEN           

_font_cache = {}
def get_font(size, weight="semibold"):
    """Bundled Poppins if present, otherwise pygame's default font."""
    key = (size, weight)
    if key not in _font_cache:
        fname = "Poppins-SemiBold.ttf" if weight == "semibold" else "Poppins-Medium.ttf"
        try:
            _font_cache[key] = pg.font.Font(os.path.join(FONT_DIR, fname), size)
        except Exception:
            _font_cache[key] = pg.font.Font(None, int(size * 1.2))
    return _font_cache[key]

def draw_text(surf, text, font, colour, center=None, topleft=None, midleft=None, shadow=None):
    img = font.render(text, True, colour)
    rect = img.get_rect()
    if center is not None: rect.center = center
    elif midleft is not None: rect.midleft = midleft
    elif topleft is not None: rect.topleft = topleft
    if shadow is not None: 
        surf.blit(font.render(text, True, shadow), rect.move(2, 4))
    surf.blit(img, rect)
    return rect

class Button2(pg.sprite.Sprite):
    def __init__(self, x:int, y:int, width:int, height:int, text:str | None,colour = YELLOW,alpha = 255):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.x =x
        self.y = y
        self.colour = colour
        self.alpha = alpha

    def draw(self, screen, font_size=26):
        surf = pg.Surface(self.rect.size, pg.SRCALPHA)
        local = surf.get_rect()
        if self.is_hovered():
            pg.draw.rect(surf, self.colour, local, border_radius=14)
            text_col = DARK_TEXT
        else:
            pg.draw.rect(surf, PANEL, local, border_radius=14)
            pg.draw.rect(surf, self.colour, local, width=2, border_radius=14)
            text_col = TEXT
        draw_text(surf, self.text, get_font(font_size), text_col, center=local.center)
        surf.set_alpha(self.alpha)
        screen.blit(surf, self.rect.topleft)

    def is_clicked(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse_x, mouse_y) and pg.mouse.get_pressed()[0]
    def is_hovered(self):
        return self.rect.collidepoint(pg.mouse.get_pos())
    
    def change_text(self,text):
        self.text = text

class Checkbox2(Button2):
    # one-of-three selector: selected = filled accent, unselected = muted
    def __init__(self,x,y,length,label= None,text_offset=(0,0), text_colour=None,text_size=22,colour=YELLOW):
        super().__init__(x,y,length,length,label,colour)
        self.state = 0
        self.label = label
        self.offset = pg.Vector2(text_offset)
        self.text_col = text_colour
        self.text_size = text_size
        self.alpha = 50
        
    def draw(self, screen):
        if self.state == 1:
            fill, text_col = YELLOW, DARK_TEXT
        else:
            fill = lighten(PANEL, 0.08) if self.is_hovered() else PANEL
            text_col = TEXT if self.is_hovered() else MUTED
        #pg.draw.rect(screen, fill, self.rect, border_radius=12)
        surf = pg.Surface(self.rect.size, pg.SRCALPHA)
        local = surf.get_rect()                      # same size, but positioned at (0, 0)
        pg.draw.rect(surf, fill, local, border_radius=12)
        if self.state == 0:
            pg.draw.rect(surf, lighten(PANEL, 0.12), local, width=1, border_radius=12)
        if self.label is not None:
            if self.text_col is not None: text_col = self.text_col
            draw_text(surf, self.text, get_font(self.text_size), text_col,
                    center=local.move(self.offset).center)
        surf.set_alpha(self.alpha)
        screen.blit(surf, self.rect.topleft)
        
    def is_clicked(self):
        if super().is_clicked():
            if self.state == 0:
                self.state = 1
                return True
            elif self.state == 1:
                self.state = 0
        else: 
            return False

    def change_state(self,state):
        self.state = state
        if self.state == 0:
                self.colour = RED
        elif self.state == 1:
                self.colour = GREEN      

def main():
    #UI
    start = Button2(width-200,20,150,50,"Restart",GREEN)
    stop = Button2(width-200,80,150,50,"Stop",GREEN)
    
    size_slider = Slider((width-150,250),100,20,GREEN)
    
    clear = Button2(50,20,100,50,"Clear",GREEN)
    edit = Button2(50,80,100,50,"Edit",GREEN)

    # presets
    presets = [
        Button2(50,height -250,200,50,"Game of Life",GREEN),
        Button2(50,height -170,200,50,"Day and Night",GREEN),
        Button2(50,height -90,200,50,"Maze",GREEN)
    ]
    #survival boxes
    survival_group = [Checkbox2(width-250,450,30,"1"),
                      Checkbox2(width-250 + 50,450,30,"2"),
                      Checkbox2(width-250 + 100,450,30,"3"),
                      Checkbox2(width-250+150,450,30,"4"),
                      Checkbox2(width-250,450+40,30,"5"),
                      Checkbox2(width-250 + 50,450+40,30,"6"),
                      Checkbox2(width-250+100,450+40,30,"7"),
                      Checkbox2(width-250 + 150,450+40,30,"8")
                      ]
    spawn_group = [Checkbox2(width-250,450-150,30,"1"),
                      Checkbox2(width-250 + 50,450-150,30,"2"),
                      Checkbox2(width-250 + 100,450-150,30,"3"),
                      Checkbox2(width-250+150,450-150,30,"4"),
                      Checkbox2(width-250,450+40-150,30,"5"),
                      Checkbox2(width-250 + 50,450+40-150,30,"6"),
                      Checkbox2(width-250+100,450+40-150,30,"7"),
                      Checkbox2(width-250 + 150,450+40-150,30,"8")
                      ]

    #conway's game of life ruleset
    spawn_group[2].change_state(1)
    survival_group[2].change_state(1)
    survival_group[1].change_state(1)

    pg.display.set_caption("Cellular Automata")

    graph = Graph(1,50,50) 
    graph.start() 

    startx,starty = 400,100

    #camera drag vars
    camera_pos = pg.math.Vector2(0, 0)
    drag_start = False
    start_mouse_pos = pg.math.Vector2(0, 0)
    mouse_drag = pg.math.Vector2(0, 0) 
    total_offset = pg.math.Vector2(0,0)
    
    fullscreen_cooldown = 0 
    update_cooldown = 10
    update = True
    
    edit_mode = False
    
    world = pg.Surface((graph.x,graph.y))
    scale = 5

    press_on_ui = False
    ui_elements = [start, stop, clear, edit, size_slider] + survival_group + spawn_group + presets
    
    while True:
        screen.fill(BG)
        world.fill(BG)    

        #drag
        total_offset = camera_pos + mouse_drag
        #scaling 

        scale = 5 + math.ceil(size_slider.percentage()*0.02*5)

 
        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()
            if (pg.key.get_pressed()[pg.K_f] or pg.key.get_pressed()[pg.K_ESCAPE]) and fullscreen_cooldown > 30:
                pg.display.toggle_fullscreen()
                fullscreen_cooldown = 0
            
            if event.type == pg.MOUSEBUTTONDOWN:  
                if event.button == 1: # prevent srag on ui
                    press_on_ui = any(e.is_hovered() for e in ui_elements)
                if event.button == 1 and start.is_hovered(): #start
                        graph.start()
                        edit_mode = False
                        edit.change_text("Edit")
                        
                elif event.button == 1 and stop.is_hovered(): #stop
                        if update: 
                            update = False
                            stop.change_text("Continue")
                            
                        else: 
                            update = True
                            stop.change_text("Stop")
                            edit_mode = False
                            edit.change_text("Edit")
                
                elif event.button == 1 and clear.is_hovered(): #clear
                    for y in range(graph.y):
                        for x in range(graph.x):
                            if graph.nodes[y][x].state == 1:
                                graph.nodes[y][x].change_state()
                                update = False
                                stop.change_text("Continue")
                #presets
                elif event.button == 1 and not update and any(p.is_hovered() for p in presets): #clear
                        if presets[0].is_hovered(): #Conways
                            for i in range(len(spawn_group)):
                                if i == 2:
                                    spawn_group[i].change_state(1)
                                else:
                                    spawn_group[i].change_state(0)
                            for i in range(len(survival_group)):
                                if i == 2 or i == 1:
                                    survival_group[i].change_state(1)
                                else:
                                    survival_group[i].change_state(0) 
                        if presets[1].is_hovered(): #Day and Night
                            for i in range(len(spawn_group)):
                                if i in [2,5,6,7]:
                                    spawn_group[i].change_state(1)
                                else:
                                    spawn_group[i].change_state(0)
                            for i in range(len(survival_group)):
                                if i in [2,3,5,6,7]:
                                    survival_group[i].change_state(1)
                                else:
                                    survival_group[i].change_state(0)    
                        if presets[2].is_hovered(): #Maze

                            for i in range(len(spawn_group)):
                                if i in [2]:
                                    spawn_group[i].change_state(1)
                                else:
                                    spawn_group[i].change_state(0)
                            for i in range(len(survival_group)):
                                if i in [0,1,2,3,4]:
                                    survival_group[i].change_state(1)
                                else:
                                    survival_group[i].change_state(0)                                            

                elif event.button == 1 and size_slider.is_hovered(): #slider
                    size_slider.dragging = True
                
                elif not update:    
                    if event.button == 1 and edit.is_hovered(): #edit
                            if edit_mode: 
                                edit_mode = False
                                edit.change_text("Edit")
                            else: 
                                edit_mode = True
                                edit.change_text("Stop")
                    elif event.button == 1 and any(box.is_hovered() for box in survival_group):
                        for box in survival_group:
                            box.is_clicked()
                    elif event.button == 1 and any(box.is_hovered() for box in spawn_group):
                        for box in spawn_group:
                            box.is_clicked()
                    
            if event.type == pg.MOUSEBUTTONUP:
                press_on_ui = False
                size_slider.dragging = False

            if event.type == pg.MOUSEWHEEL:
                y = 1 if event.precise_y > 0 else -1                
                size_slider.scroll(10* y)
        
        mouse = pg.mouse.get_pressed()
        #drag code 
        if edit_mode and not update and not press_on_ui:#Draw code
            mx, my = pg.mouse.get_pos()
            cell_w = scale * 100 / graph.x          # on-screen size of one cell
            cell_h = scale * 100 / graph.y
            col = int((mx - (startx - total_offset.x)) // cell_w)
            row = int((my - (starty - total_offset.y)) // cell_h)
        
            if 0 <= col < graph.x and 0 <= row < graph.y:
                if mouse[0]:
                    graph.nodes[row][col].change_state(1)
                elif mouse[2]:
                    graph.nodes[row][col].change_state(0)
        
        if mouse[0] and not press_on_ui and not (edit_mode and not update): 
                if not drag_start:
                    drag_start = True
                    start_mouse_pos = pg.math.Vector2(pg.mouse.get_pos())
                else:
                    current_mouse_pos = pg.math.Vector2(pg.mouse.get_pos())
                    mouse_drag = start_mouse_pos - current_mouse_pos           
        else:
                if drag_start:
                    camera_pos += mouse_drag
                    mouse_drag = pg.math.Vector2(0, 0)
                    drag_start = False
            
        if update:
            if update_cooldown <= 0:
                graph.update(survival_group,spawn_group)
                update_cooldown = 10
            else: update_cooldown -= 1
        
                #size slider
        if size_slider.dragging:
            size_slider.move_slider(pg.mouse.get_pos())

        
        #node draw
        for nodes in graph.nodes:
            for node in nodes:
                world.blit(node.image, (node.rect.x , node.rect.y ))
                
        
        new_width = max(1,int(scale * 100))
        new_height = max(1,int(scale * 100))
        world_scaled = pg.transform.scale(world,(new_width,new_height))
        
        screen.blit(world_scaled,(startx- total_offset.x,starty- total_offset.y))
        
        #button show
        if update: alpha = 128
        else:   alpha = 255
        edit.alpha = alpha
        for box in survival_group:
            box.alpha = alpha
            box.draw(screen)
        for box in spawn_group:
            box.alpha = alpha
            box.draw(screen)

        draw_text(screen, "Spawn if neighbours =", get_font(20), MUTED,
                topleft=(spawn_group[0].rect.x, spawn_group[0].rect.y - 32))
        draw_text(screen, "Survive if neighbours =", get_font(20), MUTED,
                topleft=(survival_group[0].rect.x, survival_group[0].rect.y - 32))
        
        '''    
        start.draw(screen,30)
        stop.draw(screen,30)
        '''
        buttons = [start,stop,clear,edit] + presets
        
        for button in buttons:
            button.draw(screen,30)

        #screen.blit(start, (start.x + start.width // 2 - start.get_width() // 2, start.y + start.height // 2 - start.get_height() // 2))
        #screen.blit(size_slider.image,size_slider.rect)
        #size_slider.draw_slider(screen)
        fullscreen_cooldown +=1
        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 