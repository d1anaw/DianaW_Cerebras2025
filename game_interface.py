import pygame
import agent_interface

class Background():
    backgrounds = [pygame.image.load(pic) for pic in ["images/background.png", "images/top.png", "images/left.png", "images/right.png"]]
    islands = [pygame.image.load(pic) for pic in ["images/health.png", "images/career.png"]] # "images/hobbies.png"

    def __init__(self):
        self.display = self.backgrounds[0]
        self.pic = "background"

    def switch_bg(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]: # self.display == self.backgrounds[2]
            self.display = self.backgrounds[3]
        if keys[pygame.K_LEFT]: # self.display == self.backgrounds[3] and
            self.display = self.backgrounds[2]
        if keys[pygame.K_UP]:
            self.display = self.backgrounds[1]

        if keys[pygame.K_RETURN]:
            if self.display == self.backgrounds[1]: # top
                self.display = self.islands[0]
            if self.display == self.backgrounds[2]: # left
                self.display = self.islands[1]
            # if self.display == self.backgrounds[3]: # right
            #     self.display = self.islands[2]

        if self.display not in self.backgrounds and keys[pygame.K_ESCAPE]:
            self.display = self.backgrounds[0]

        win.blit(background.display, (0,0))

def UserInterface():
    def __init__(self):
        pass



class UserInfo():
    def __init__(self):
        self.health = {
            "sleep_hours": None,
            "sports": None,
            "diet": None,
            "dietary_restrictions": None,
            "favorite_foods": None,
            "challenges": None
            }

        self.hobbies = {
            "hobbies": None,
            "free_time": None,
            "challenges": None
        }

        self.career = {
            "job": None,
            "commitment": None,
            "career_goals": None,
            "challenges": None
        }
        self.data = {"health": self.health, "career": self.career, "hobbies": self.hobbies}

    def get_data(self, topic):
        """
        Returns the data for the topic of interest.
        """
        return self.data[topic]


class Figure(UserInfo):
    def __init__(self, image):
        self.x = 50
        self.y = 50
        self.width = 40
        self.height = 60
        self.orientation = "right"
        self.image = pygame.image.load(image)
        # self.geometry = (self.x, self.y, self.width, self.height)

    def move_figure(self, vel=10):
        """
        Moves a figure.
        """
        keys = pygame.key.get_pressed()
        possible_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        # nonlocal x, y
        if keys[pygame.K_LEFT]:
            if (new := self.x - vel) >= 5:
                self.x = new
        if keys[pygame.K_RIGHT]:
            if (new := self.x + vel) <= 490:
                self.x = new
        if keys[pygame.K_UP]:
            if (new := self.y - vel) >= 5:
                self.y = new
        if keys[pygame.K_DOWN]:
            if (new := self.y + vel) <= 490:
                self.y = new

        win.blit(fig.image, (self.x, self.y))


if __name__ == "__main__":

    pygame.init()

    win = pygame.display.set_mode(
        (500, 500)
    )

    pygame.display.set_caption("Welcome to Coaching Island!")
    # user = Figure()
    background = Background()
    fig = Figure("images/beaver.png")

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # x, y = move_figure(x, y)
        win.fill((0, 0, 0))

        ############ UI Logic ############


        # background

        background.switch_bg()

        # move user
        fig.move_figure()


        ############ Data Collection ############



        ############ Coaching Logic ############

        pygame.display.update()





    pygame.quit()
