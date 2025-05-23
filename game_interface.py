import pygame
import pygame_gui
import agent_interface

class Screen():
    backgrounds = [pygame.image.load(pic) for pic in ["images/background.png", "images/top.png", "images/left.png", "images/right.png"]]
    islands = [pygame.image.load(pic) for pic in ["images/health.png", "images/career.png", "images/hobbies.png"]]
    # progress_pg = pygame.image.load("images/progress.png")


class HomeScreen(Screen):
    def __init__(self):
        self.display = self.backgrounds[0]
        self.popup_status = False

    def generate_popup(self, win, clock, manager):
        entry = pygame_gui.elements.UITextEntryLine(relative_rect=((25, 350), (450,  50)), manager=manager,
                                                        object_id="#chat_box")
        self.popup_status = True

        while True:
            UI_REFRESH_RATE = clock.tick(60)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#chat_box":
                    input_text = entry.get_text()
                    entry.kill()
                    self.popup_on = False
                    return input_text
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    entry.kill()
                    self.popup_on = False
                    return
                manager.process_events(event)

            manager.update(UI_REFRESH_RATE)
            # win.fill("white")
            manager.draw_ui(win)
            pygame.display.update()

    def popup_on(self):
        return self.popup_status

    def update(self, win):
        """
        Detects key press and updates display to appropriate image.
        """
        keys = pygame.key.get_pressed()

        # illuminate island
        if keys[pygame.K_RIGHT]: # self.display == self.backgrounds[2]
            self.display = self.backgrounds[3]
        if keys[pygame.K_LEFT]: # self.display == self.backgrounds[3] and
            self.display = self.backgrounds[2]
        if keys[pygame.K_UP]:
            self.display = self.backgrounds[1]

        # enter island
        if keys[pygame.K_RETURN]:
            if self.display == self.backgrounds[1]: # top
                self.display = self.islands[0]
            if self.display == self.backgrounds[2]: # left
                self.display = self.islands[1]
            if self.display == self.backgrounds[3]: # right
                self.display = self.islands[2]

        if self.display not in self.backgrounds and keys[pygame.K_ESCAPE]:
            self.display = self.backgrounds[0]

        if keys[pygame.K_q]: # close manual
            pass

        if keys[pygame.K_p]: # view progress page:
            self.display = self.progress_pg

        win.blit(self.display, (0,0))


class UserInfo():
    def __init__(self):
        self.visits = 0
        self.data = ''

    def get_data(self, topic):
        """
        Returns the data for the topic of interest.
        """
        str_data = ''
        for key, val in self.data[topic]:
            str_data += 'My' + key + "data is:" + str(val)
        return str_data

class Figure():
    def __init__(self, image, x=50, y=50):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)

    def update(self, win, vel=10):
        """
        Moves a figure according to arrow keys pressed.
        Constrains figure to be within bounds of game board.
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

        win.blit(self.image, (self.x, self.y))

class User(Figure):
    def __init__(self):
        Figure.__init__(self, "images/beaver.png")
        UserInfo.__init__(self)

class Coach(Figure):
    coach_locations = {"health": (150, 0), "career": (150, 0), "hobbies": (150, 0)}

    def __init__(self, island):
        self.island = island
        image = 'images/' + island + '_coach.png'
        super().__init__(image, *self.coach_locations[island])

    def update_figure(self, win):
        win.blit(self.image, (self.x, self.y))

def first_visit(win, clock, manager):

    entry = pygame_gui.elements.UITextEntryLine(relative_rect=((25, 400), (450,  50)), manager=manager,
                                                     object_id="#health_survey_entry")

    welcome_pic = pygame.image.load("images/welcome.png")

    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#health_survey_entry":
                input_text = entry.get_text()
                if not input_text: # must fill out survey
                    pass
                else:
                    entry.kill()
                    return input_text
            manager.process_events(event)

        win.blit(welcome_pic, (100,100))
        manager.update(UI_REFRESH_RATE)
        # win.fill("white")
        manager.draw_ui(win)
        pygame.display.update()


def main():
    # initialize game objects
    pygame.init()
    WIDTH, HEIGHT = 500, 500
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Welcome to Coaching Island!")

    CLOCK = pygame.time.Clock()
    MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT))
    NEW_CLIENT = True


    # initialize background and figures
    screen = HomeScreen()

    user = User()
    health_coach = Coach("health")
    career_coach = Coach("career")
    hobbies_coach = Coach("hobbies")

    run = True
    while run:
        win.fill((0, 0, 0))
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        ############ UI Logic & Data Collection ############
        # background switches due to pressed keys
        screen.update(win)

        if NEW_CLIENT:
            survey_response = first_visit(win, CLOCK, MANAGER)
            screen.update(win)

            user.data = survey_response
            # summarize and update data for progress display
            summary = agent_interface.chat_request(agent_interface.summarize_prompt + user.data)
            print(f'{summary=}')
            user.data = summary

            NEW_CLIENT = False

        if screen.display in screen.islands:
            # figure out current coach in display
            if screen.display == screen.islands[0]: # health
                curr_coach = health_coach
                topic = "health"
            if screen.display == screen.islands[1]: # career
                curr_coach = career_coach
                topic = "career"
            if screen.display == screen.islands[2]: # hobbies
                curr_coach = hobbies_coach
                topic = "hobbies"
            print(f'{topic=}')
            # initialize convo

            curr_coach.update(win)
            pygame.display.update()

            # start session
            if not screen.popup_status:

                if user.visits == 0:
                    new_client = True
                else:
                    new_client = False

                intro = agent_interface.initialize_convo(topic, user.data, new_client)
                print(f'{intro=}')
                user.visits += 1
                agent_interface.vocalize_text(intro, topic)

            # listen to user
            user_input = screen.generate_popup(win, CLOCK, MANAGER)

            if user_input is not None: # user decides to ask
                response = agent_interface.chat_request(agent_interface.ATTITUDE_PROMPT + user_input)
                print(f'{response=}')
                agent_interface.vocalize_text(response, topic)

        pygame.display.update()

    pygame.quit()




if __name__ == "__main__":
    main()
