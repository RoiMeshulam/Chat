import pickle
import socket
import threading
import time

import pygame
import sys
"""
This is a client class
"""
class Client:
    def __init__(self, ip, port, name):
        self.random_user = 0
        try:
            #INITING THE CLIENT
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.target_ip = ip
            self.target_port = int(port)
            self.name = name
            if len(name) == 0:
                name = f'random user{self.random_user}'
                self.random_user = self.random_user+1
            self.users = ['Arik','Roi','Amit']
            self.files = ['File.txt','Dog.png']
            self.oldmsg = []

        except:
            print("Couldn't connect to server")
            return
        print("Connected to Server")
        #an infinite loop to accept data from server all the time

        pygame.init()
        screen = pygame.display.set_mode([1260, 800])
        newmsg = ''
        starttime = time.time()
        endtime = time.time()
        #This is all the actions we can do on our chat
        while endtime-starttime < 8:
            endtime = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_x, click_y = pygame.mouse.get_pos()
                    #Private messege option
                    if privateWindow.collidepoint(click_x, click_y):
                        if not newmsg.__contains__(':'):
                            self.oldmsg.append("To use private messege please write 'NAME_TO_WHISPER':'TEXT'")
                            newmsg= ''
                            break
                        i = newmsg.index(':')
                        whispto = newmsg[0:i]
                        if not self.users.__contains__(whispto):
                            self.oldmsg.append("To use private messege please write 'NAME_TO_WHISPER':'TEXT'")
                            newmsg = ''
                            break
                        newmsg = newmsg[i+1:]
                        newmsg = f'p.{whispto}.{self.name}: {newmsg}'
                        newmsg = ''
                    #Download file request
                    if downloadWindow.collidepoint(click_x, click_y):
                        if newmsg[0:8] != 'filereq.' or not self.files.__contains__(newmsg[8:]):
                            self.oldmsg.append("To download please write filereq.'FILENAME'")
                            newmsg= ''
                            break
                        newmsg = ''

                    #A regular messege option
                    if sendWindow.collidepoint(click_x, click_y):
                        if len(newmsg) == 0:
                            break
                        newmsg = f'{self.name}: {newmsg}'
                        self.oldmsg.append(newmsg)
                        newmsg = ''
                #Typing new messege
                if event.type == pygame.KEYDOWN:
                    click_x, click_y = pygame.mouse.get_pos()
                    if msgWindow.collidepoint(click_x, click_y):
                        if event.key == pygame.K_BACKSPACE:
                            newmsg = newmsg[:-1]
                        else:
                            newmsg += event.unicode

            screen.fill((0, 0, 0))
            #Drawing the entire screen
            chatWindow = pygame.draw.rect(screen, (255, 255, 255), [0, 0, 1000, 675], 2)
            userWindow = pygame.draw.rect(screen, (255, 255, 255), [1000, 0, 250, 375], 2)
            fileWindow = pygame.draw.rect(screen, (255, 255, 255), [1000, 375, 250, 300], 2)
            msgWindow = pygame.draw.rect(screen, (255, 255, 255), [0, 675, 1000, 125], 2)
            privateWindow = pygame.draw.rect(screen, (200, 110, 0), [1010, 710, 75, 75])
            downloadWindow = pygame.draw.rect(screen, (200, 110, 0), [1090, 710, 75, 75])
            # downloadWindow2 = pygame.draw.rect(screen, (200, 110, 0), [1170, 710, 75, 75])
            sendWindow = pygame.draw.rect(screen, (0, 180, 40), [910, 710, 75, 75])
            #Now printing the messeges to the screen
            self.print_screen(screen,newmsg)

            pygame.display.flip()

    def print_screen(self,screen,newmsg):
        font = pygame.font.SysFont('Arial', 20, bold=True, )
        userstag = font.render('Users:', True, (255, 255, 255))
        filestag = font.render('Files:', True, (255, 255, 255))
        chat = font.render('Chat', True, (255, 255, 255))
        msg = font.render('Your messege here:', True, (255, 255, 255))
        outmsg = font.render(newmsg, True, (0, 0, 255))
        private = font.render('Private', True, (255, 255, 255))
        downloadFile = font.render('Download', True, (255, 255, 255))
        # downloadFile2 = font.render('<-Timed', True, (255, 255, 255))
        send = font.render('Send', True, (255, 255, 255))
        screen.blit(userstag, [1005, 0])
        screen.blit(filestag, [1005, 375])
        screen.blit(chat, [5, 0])
        screen.blit(msg, [5, 680])
        screen.blit(outmsg, [5, 710])
        screen.blit(private, [1015, 740])
        screen.blit(downloadFile, [1090, 740])
        # screen.blit(downloadFile2, [1180, 740])
        screen.blit(send, [917, 740])
        i = 0
        for u in self.users:
            user = font.render(u, True, (0, 0, 220))
            screen.blit(user, [1005, 25 + i])
            i = i + 25

        i = 0
        for f in self.files:
            file = font.render(f, True, (0, 0, 220))
            screen.blit(file, [1005, 400 + i])
            i = i + 25

        i = 0
        for m in self.oldmsg:
            if len(m) >= 12 and m[0:12] == 'Private From':
                postmsg = font.render(m, True, (220, 0, 0))
            else:
                postmsg = font.render(m, True, (0, 0, 220))
            screen.blit(postmsg, [5, 25 + i])
            i = i + 25