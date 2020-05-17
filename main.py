#import Ai
import Get_camera
import cv2
import pygame
import numpy
import UI
import cv2

#get the camera device
#camera = Get_camera.Camera()

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
def Scan_button():
    app.current_screen = app.Camera_screen
    camera.Start()

#when the history button gets pressed
def History_button():
    pass
#start hunt button pressed
def Start_hunt_button():
    pass
#the main menu button on the camera screen gets pressed
def Camera_main_menu_button():
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
        #buttons for Main menu
        self.Main_menu_buttons = [
            UI.Button(x = self.size[0]//2 - 100,y = 100 + dy*100,w=200,h=50,
                      surface=self.screen,background=(255,0,0),outline=True) for dy in range(3)]
        #set text and actions to main menu buttons
        self.Main_menu_buttons[0].text = "history"
        self.Main_menu_buttons[1].text = "Hunt"
        self.Main_menu_buttons[2].text = "Scan"
        self.Main_menu_buttons[0].action = History_button
        self.Main_menu_buttons[1].action = Start_hunt_button
        self.Main_menu_buttons[2].action = Scan_button
        #create the button on camera screen
        surf = pygame.Surface((30,30))
        for y in range(3):
            pygame.draw.line(surf,(255,255,255),(0,5 + y*10),(30,5 + y*10), 1)
        self.Camera_menu_button = UI.Button(x=self.size[0] - 60,y=self.size[1] - 60,
                                            image=surf,enlarge=True, surface=self.screen,
                                            action=Camera_main_menu_button)
        
        

    def Loop(self):
        while self.running:
            self.clock.tick(60)
            self.current_screen()
            
            
            pygame.display.update()
            self.Events()
    
    def Camera_screen(self):
        self.screen.fill((0,0,0))
        self.screen.blit(cv2_to_pygame(cv2_flip(cv2_scale(camera.frame,(0.5,0.3)))))
        pygame.draw.circle(self.screen,(255,255,255),(self.size[0]//2,self.size[1] - 50),30,4)
        self.Camera_menu_button.update(pygame.mouse.get_pos(), self.click)
    
    def Main_menu(self):
        self.screen.fill((255,255,255))
        for button in self.Main_menu_buttons:
            button.update(pygame.mouse.get_pos(),self.click)
    
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
        
        if self.startHold:
            if pygame.time.get_ticks() - self.startHold > 100:
                self.hold = True
                self.startHold = None
                
if __name__ == "__main__":
    app = App()
    app.Loop()

pygame.quit()
camera.running = False