import pygame
import pygame_gui

class PopUp:
    def __init__(self, win, clock, manager, id):
        self.win = win
        self.clock = clock
        self.manager = manager
        self.entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(25, 200, 450, 50),
            manager=self.manager,
            object_id=id
        )
        self.response = None

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#popup_entry":
                self.response = self.entry.get_text()
            self.manager.process_events(event)

        self.manager.update(self.clock.tick(60) / 1000)
        self.manager.draw_ui(self.win)
        pygame.display.update()
        return self.response
