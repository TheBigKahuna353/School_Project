#import Ai
import Get_camera
import cv2
import pygame
import numpy
import UI
import database as db

#get the camera device
#camera = Get_camera.Camera('http://10.1.120.174:8080/video')
#camera = Get_camera.Camera('http://10.1.115.12:8080/video')
#camera = Get_camera.Camera(0)

#initialize pygame
pygame.init()


#rotate a cv2 image
def cv2_rotate(img):
    w,h = img.shape[:2]
    Matrix = cv2.getRotationMatrix2D((w//2,h//2), 90, 1.0)
    return cv2.warpAffine(img, Matrix, (w,h))    

#resize a cv2 image
def cv2_scale(img,size):
    w,h = img.shape[:2]
    print(w,h,w*size[0],size[1]*h)
    return cv2.resize(img,(int(w*size[0]),int(h*size[1])))

#flip a cv2 image horizontally
def cv2_flip(img):
    return cv2.flip(img,0)

#convert a cv2 image to pygame
def cv2_to_pygame(img):
    return pygame.pixelcopy.make_surface(img)

#when the scan button gets pressed
def Scan_button(button):
    app.current_screen = app.Camera_screen
    #camera.Start()

#when the history button gets pressed
def History_button(button):
    pass
#start hunt button pressed
def Start_hunt_button(button):
    app.current_screen = app.All_hunts
    
def Question_button(button):
    app.current_screen = app.Question

#the main menu button on the camera screen gets pressed
def Camera_main_menu_button(button):
    app.current_screen = app.Main_menu

#class for the app
class App:
    #setup variables
    def __init__(self):
        #sys vars
        self.running = True
        self.click = False
        self.hold = False
        self.startHold = None
        self.size = (300,500)
        self.screen = pygame.display.set_mode(self.size)        
        self.clock = pygame.time.Clock()
        self.current_screen = self.Main_menu
        self.sys_font = pygame.font.Font(pygame.font.match_font('Calibri'), 40)
        
        #hunt specefic vars
        self.hunt_id = None
        self.all_questions = []
        self.current_question = 0
        
        #BUTTONS
        button_theme = {
            'outline': True,
            'curve': 0.4,
            'background_color': (255, 0, 0)
        }
        button_theme_new = button_theme.copy()
        button_theme_new.update({'dont_generate': True})
        #buttons for Main menu
        self.Main_menu_buttons = [
            UI.Button(
                self.size[0]//2 - 100, 100 + dy*100, 200, 40,
                    button_theme_new) for dy in range(3)]
        #set text and actions to main menu buttons
        self.Main_menu_buttons[0].Update_text("history")
        self.Main_menu_buttons[1].Update_text("Hunt")
        self.Main_menu_buttons[2].Update_text("Scan")
        self.Main_menu_buttons[0].on_click = History_button
        self.Main_menu_buttons[1].on_click = Start_hunt_button
        self.Main_menu_buttons[2].on_click = Scan_button
        button_theme_new = button_theme.copy()
        button_theme_new.update({'on_click': Question_button, 'text': 'Question'})
        self.current_question_button = UI.Button(
            self.size[0]//2 - 100, 400, 200, 40, button_theme_new)
        #create the buttons on camera screen
        surf = pygame.Surface((30,30), pygame.SRCALPHA)
        for y in range(3):
            pygame.draw.line(surf,(255,255,255),(0,5 + y*10),(30,5 + y*10), 1)
        button_theme_new = button_theme.copy()
        button_theme_new.update({'image': surf, 'enlarge': True, 'on_click': Camera_main_menu_button})
        self.Camera_menu_button = UI.Button(self.size[0] - 60,self.size[1] - 60,
                                            param_options=button_theme_new)
        surf = pygame.Surface((30,30),pygame.SRCALPHA)
        surf2 = pygame.Surface((40,40),pygame.SRCALPHA)
        pygame.draw.circle(surf,(255,255,255),(15,15),15,2)
        pygame.draw.circle(surf2, (255,255,255), (20,20), 20,2)
        button_theme_new = button_theme.copy()
        button_theme_new.update({'image': surf, 'hover_image': surf2 })       
        self.Camera_settings_button = UI.Button(self.size[0]//4-20, self.size[1] - 60,
                                                param_options=button_theme_new) 
        surf = pygame.Surface((60,60),pygame.SRCALPHA)
        surf2 = pygame.Surface((60,60),pygame.SRCALPHA)
        pygame.draw.circle(surf, (255,255,255),(30,30),30,4)
        pygame.draw.circle(surf2, (255,255,255),(30,30),30,8)
        self.Camera_take_photo_button = UI.Button(self.size[0]//2 - 30,self.size[1] - 90,
                                                  param_options=button_theme_new)
        
        #Settings
        self.settings_check_boxes = [UI.CheckBox(200,150 + 50*i,40,button_theme) for i in range(3)]
        
        #all hunts
        self.hunt_names = db.get_all_hunts() + [['Cancel']]
        self.hunt_names_buttons = [UI.Button(50, 100 + 50*i,200, 40, {
                                             'background_color': (255,0,0),
                                             'outline': True,
                                             'text': self.hunt_names[i][0],
                                             'curve': 0.4}
                                             ) for i in range(len(self.hunt_names))]
        
        
    #the main gam loop
    def Loop(self):
        while self.running:
            self.clock.tick(60)
            self.current_screen()
            pygame.display.update()
            self.Events()
    
    #the camera screen of the program
    def Camera_screen(self):
        self.screen.fill((0,0,0))
        #self.screen.blit(cv2_to_pygame(cv2_flip(cv2_scale(camera.frame,(0.5,0.5)))), (0,0))
        self.Camera_take_photo_button.update()
        self.Camera_menu_button.update()
        if self.Camera_settings_button.update():
            self.current_screen = self.Settings
    
    #the main meny screen of the program
    def Main_menu(self):
        self.screen.fill((255,255,255))
        for button in self.Main_menu_buttons:
            button.update()
        if self.hunt_id is not None:
            self.current_question_button.update()
    
    #screen that shows all available scav hunts
    def All_hunts(self):
        self.screen.fill((255,255,255))
        for i, button in enumerate(self.hunt_names_buttons):
            if button.update():
                if i < len(self.hunt_names_buttons) -1:
                    self.all_questions = db.get_questions(i)
                    self.hunt_id = i
                self.current_screen = self.Main_menu
    
    #check for events
    def Events(self):
        self.click = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False   
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
                self.startHold = pygame.time.get_ticks()
            elif e.type == pygame.MOUSEBUTTONUP:
                self.hold = False
                self.startHold = None
        
        #if the user holds down the mousebutton for 0.1s, it is classified as holding, not clicking
        if self.startHold:
            if pygame.time.get_ticks() - self.startHold > 100:
                self.hold = True
                self.startHold = None

    #settings screen
    def Settings(self):
        self.screen.fill((255,255,255))
        obj = self.sys_font.render("Settings",True, (0,0,0))
        self.screen.blit(obj,(150-obj.get_width()//2,50))
        settings = ["setting 1", "setting 2", "setting 3"]
        for i, text in enumerate(settings):
            obj = self.sys_font.render(text,True, (0,0,0))
            self.screen.blit(obj,(20,150 + 50*i))    
        for checkbox in self.settings_check_boxes:
            checkbox.update()
    
    #screen that shows the current question for hunt
    def Question(self):
        self.screen.fill((255, 255, 255))
        obj = self.sys_font.render(self.all_questions[self.current_question], True, (0,0,0))
        self.screen.blit(obj, (100,100))


#start the app if this is the main script      
if __name__ == "__main__":
    app = App()
    app.Loop()

#when finished, close pygame and stop getting camera
pygame.quit()
#camera.running = False

