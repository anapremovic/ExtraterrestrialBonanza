import pygame

SCREEN_TITLE = 'Extraterrestrial Bonanza'
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
WHITE_COLOUR = (255, 255, 255)
PURPLE_COLOUR = (139, 0, 139)

# music
pygame.mixer.init()
pygame.mixer.music.load('Pixies Cecilia Ann-[AudioTrimmer.com].mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

# initialize and import a font for displaying text
pygame.font.init()
font = pygame.font.Font('ARCADECLASSIC.TTF', 75)
font_0 = pygame.font.Font('ARCADECLASSIC.TTF', 40)
font_1 = pygame.font.Font('ARCADECLASSIC.TTF', 90)
font_2 = pygame.font.Font('ARCADECLASSIC.TTF', 25)
font_3 = pygame.font.Font('ARCADECLASSIC.TTF', 17)

class Game:

    TICK_RATE = 60

    title_text_1 = font_1.render('Extraterrestrial', True, PURPLE_COLOUR)
    title_text_2 = font_1.render('Bonanza', True, PURPLE_COLOUR)
    instructions_1 = font_2.render('Beat 15  Levels to  win', True, PURPLE_COLOUR)
    instructions_2 = font_2.render('Press Enter to continue', True, PURPLE_COLOUR)

    did_win_entire_game = False
    
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.game_starts = False
        
        # Create the game window of the specified size, and set it to white
        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(WHITE_COLOUR)
        pygame.display.set_caption(title)

        # background image
        background_image = pygame.image.load(image_path)
        # scale it to the window size
        self.image = pygame.transform.scale(background_image, (width, height))
        
        # draw title screen
        self.game_screen.blit(self.image, (0, 0))
        
        self.game_screen.blit(self.title_text_1, (113, 175))
        self.game_screen.blit(self.title_text_2, (300, 235))
        self.game_screen.blit(self.instructions_1, (344, 310))
        self.game_screen.blit(self.instructions_2, (325, 375))
    
    def run_game_loop(self, level, level_speed):

        is_game_over = False
        did_win = False
        user_quits = False
        y_direction = 0
        x_direction = 0

        player = PlayerCharacter('player.png', 50, 275, 50, 50)

        alien_1 = Enemy('alien.png', 525, 500, 50, 50)
        alien_1.SPEED *= level_speed
        
        star = GameObject('goal.png', 920, 275, 50, 50)
        
        if level > 2:
            top_ship = Enemy('enemy_ship.png', 750, 125, 50, 50)

            laser_1 = Laser('laser.png', 750, top_ship.y_pos, 20, 10)
            laser_1.SPEED *= level_speed

        if level > 5:
            alien_2 = Enemy('alien.png', 300, 50, 50, 50)
            alien_2.SPEED *= level_speed

        if level > 9:
            bottom_ship = Enemy('enemy_ship.png', 750, 325, 50, 50)

            laser_2 = Laser('laser.png', 750, bottom_ship.y_pos, 20, 10)
            laser_2.SPEED *= level_speed
        
        # GAME LOOP
        while not is_game_over:

            # checks for all the events in the game
            for event in pygame.event.get():
                            
                # allows the user to quit the game using the x button
                if event.type == pygame.QUIT:
                    user_quits = True
                    is_game_over = True

                # detect movement in pygame and set direction
                elif event.type == pygame.KEYDOWN:

                    self.game_starts = True
                    
                    if event.key == pygame.K_UP:
                        y_direction = 1
                    elif event.key == pygame.K_DOWN:
                        y_direction = -1
                    elif event.key == pygame.K_RIGHT:
                        x_direction = 1
                    elif event.key == pygame.K_LEFT:
                        x_direction = -1

                # detect movement stopping
                # whenever a key goes up, if that key is an arrow key, stop moving
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        y_direction = 0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        x_direction = 0
        
            ############################ DRAW CHARACTERS AND BACKGROUND ############################
            
            if self.game_starts:
                # draw background
                self.game_screen.fill(WHITE_COLOUR)
                self.game_screen.blit(self.image, (0, 0))
                
                # draw the goal
                star.draw(self.game_screen)

                # update player's position and draw them at the position
                player.move(x_direction, y_direction, self.width, self.height, 0)
                player.draw(self.game_screen)

                # update enemy movement and draw them
                alien_1.move(20, self.height)
                alien_1.draw(self.game_screen)

                # level 6 and higher, add the second alien
                if level > 5:
                    alien_2.move(20, self.height)
                    alien_2.draw(self.game_screen)

                # initially, the enemy ship uses the whole screen
                top_ship_max = self.height
                
                # once the second enemy ship appears, make the top ship only move on its half
                # draw the enemy second ship and its laser
                if level > 9:
                    top_ship_max = 300
                    
                    bottom_ship.move(300, self.height)
                    bottom_ship.draw(self.game_screen)
                    
                    laser_2.move(bottom_ship.y_pos)
                    laser_2.draw(self.game_screen)

                # level 3 and higher, draw the first enemy ship and its laser
                if level > 2:
                    top_ship.move(20, top_ship_max)
                    top_ship.draw(self.game_screen)

                    laser_1.move(top_ship.y_pos)
                    laser_1.draw(self.game_screen)
                
                # display what level the user is on
                level_text = font_0.render('Level ' + str(level), True, PURPLE_COLOUR)
                self.game_screen.blit(level_text, (15, 555))  
            
            ############################ END GAME LOGIC ############################

            # detect enemy variables
            d_top_ship = False
            d_laser_1 = False
            d_alien_2 = False
            d_bottom_ship = False
            d_laser_2 = False
            
            if level > 2:
                d_top_ship = player.detect_collision(top_ship)
                d_laser_1 = player.detect_collision(laser_1)
            if level > 5:
                d_alien_2 = player.detect_collision(alien_2)
            if level > 9:
                d_bottom_ship = player.detect_collision(bottom_ship)
                d_laser_2 = player.detect_collision(laser_2)
            
            # if the player collides with an enemy or the star, exit out of game loop
            if player.detect_collision(alien_1) or d_top_ship or d_laser_1 or d_alien_2 or d_bottom_ship or d_laser_2:
                is_game_over = True
                did_win = False

                # if player collides with enemy, display game over text
                lose_text = font.render('GAME OVER', True, PURPLE_COLOUR)
                self.game_screen.blit(lose_text, (325, 260))
                pygame.display.update()
                clock.tick(0.75)
                break
            elif player.detect_collision(star):
                is_game_over = True
                did_win = True
                
                # if player collides with star, display level complete text
                win_text = font.render('Level Complete', True, PURPLE_COLOUR)
                self.game_screen.blit(win_text, (225, 260))
                pygame.display.update()
                clock.tick(0.75)
                break
            
            # Update all graphics
            pygame.display.update()
            # Cause the clock to tick and render the next frame
            clock.tick(self.TICK_RATE)

        if user_quits:
            return
        
        # if user beats level 15, display winner screen with credits
        if level > 14:
            did_exit = False

            end_text_1 = font_1.render('You Win', True, PURPLE_COLOUR)
            end_text_2 = font_2.render('Congratulations!', True, PURPLE_COLOUR)
            end_instructions = font_2.render('Press  esc  to  exit', True, PURPLE_COLOUR)
            credit1 = font_2.render('Developed  by  Ana  Premovic', True, PURPLE_COLOUR)
            credit2 = font_2.render('All assets  by  Ansimuz  via  Itch io', True, PURPLE_COLOUR)
            credit3 = font_2.render('Song credit to Cecilia  Ann  by  Pixies', True, PURPLE_COLOUR)
            
            self.game_screen.blit(self.image, (0, 0))
            self.game_screen.blit(end_text_1, (335, 225))
            self.game_screen.blit(end_text_2, (385, 300))
            self.game_screen.blit(end_instructions, (390, 365))
            self.game_screen.blit(credit1, (330, 525))
            self.game_screen.blit(credit2, (285, 545))
            self.game_screen.blit(credit3, (265, 565))

            pygame.display.update()
            clock.tick(0.75)

            while not did_exit:
                for event in pygame.event.get():       
                    if event.type == pygame.QUIT:
                        did_exit = True
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        did_exit = True
            return 
               
        # use recursion to keep running until game over or player beats level 15
        if did_win:
            self.run_game_loop(level + 1, level_speed + 0.225)
        else:
            self.run_game_loop(1, 1)

class GameObject:

    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width, height))
        
        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

class PlayerCharacter(GameObject):

    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
    
    def move(self, x_direc, y_direc, max_width, max_height, min_pos):

        # move right, left, up, down

        if x_direc > 0:
            self.x_pos += self.SPEED
        elif x_direc < 0:
            self.x_pos -= self.SPEED
        
        # reverse it so positive = up and negative = down
        if y_direc > 0:
            self.y_pos -= self.SPEED
        elif y_direc < 0:
            self.y_pos += self.SPEED

        # don't let the player go out of bounds
        # include the character's height + extra 10 for some padding
        if self.x_pos >= max_width - 70:
            self.x_pos = max_width - 70
        elif self.x_pos <= min_pos + 10:
            self.x_pos = min_pos + 10
        
        if self.y_pos >= max_height - 70:
            self.y_pos = max_height - 70
        elif self.y_pos <= min_pos + 10:
            self.y_pos = min_pos + 10
    
    def detect_collision(self, other):
        # below the other sprite
        if self.y_pos > other.y_pos + other.height:
            return False
        # above the other sprite
        elif self.y_pos + self.height < other.y_pos:
            return False

        # to the right of the other sprite
        if self.x_pos > other.x_pos + other.width:
            return False
        # to the left of the other sprite
        elif self.x_pos + self.width < other.x_pos:
            return False

        # if none of the above return False, then it is touching
        return True
            
class Enemy(GameObject):

    SPEED = 2.5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, min_height, max_height):
        # reverse it so positive = up and negative = down
        if self.y_pos <= min_height:
            # turn speed positive (to face down)
            self.SPEED = abs(self.SPEED)
        elif self.y_pos >= max_height - 70:
            # turn speed negative (to face up)
            self.SPEED = -abs(self.SPEED)
        self.y_pos += self.SPEED

class Laser(GameObject):

    SPEED = 4

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, space_ship_y_pos):
        if(self.x_pos <= 0):
            self.x_pos = 750
            self.y_pos = space_ship_y_pos
        # move left off the screen
        self.x_pos -= self.SPEED
    
# RUN THE GAME

pygame.init()

new_game = Game('space.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1, 1)

pygame.quit()
exit()
























    

