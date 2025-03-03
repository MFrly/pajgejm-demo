from settings import *
from player import Player
from npc import NPC  # Importujeme NPC z nového souboru
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
import pygame_gui

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        # GUI
        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.text_entry = None  # Pole pro vstup hráče
        self.dialog_box = None  # Pop-up okno pro text NPC
        self.submit_button = None
        self.popup_active = False

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()  # Skupina pro NPC

        self.setup()

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                npc_position = (obj.x, obj.y + 150)  # NPC se objeví 150 pixelů pod hráčem
                self.npc = NPC(npc_position, (self.all_sprites, self.npc_sprites))

    def check_npc_interaction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and not self.popup_active:  # Pokud hráč zmáčkne "E" a okno není aktivní
            for npc in self.npc_sprites:
                if self.player.hitbox_rect.colliderect(npc.hitbox_rect):  # Použití hitboxů pro přesnější detekci
                    self.create_dialog()

    def create_dialog(self):
        self.popup_active = True
        self.dialog_box = pygame_gui.elements.UITextBox("Ahoj! Mám pro tebe otázku: Kolik je 1+1?", pygame.Rect((WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 100), (300, 60)), self.manager)
        self.text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2), (200, 50)), manager=self.manager)
        self.submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH//2 - 50, WINDOW_HEIGHT//2 + 60), (100, 40)), text='Odeslat', manager=self.manager)

    def handle_popup(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.submit_button:
            answer = self.text_entry.get_text()
            if answer.strip() == "2":
                print("Správně! Dobrá práce!")
            else:
                print("Špatně, zkus to příště!")
            self.popup_active = False
            self.text_entry.kill()
            self.submit_button.kill()
            self.dialog_box.kill()

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.manager.process_events(event)
                if self.popup_active:
                    self.handle_popup(event)

            self.check_npc_interaction()  # Kontrola interakce s NPC
            self.all_sprites.update(dt)
            self.manager.update(dt)

            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            self.manager.draw_ui(self.display_surface)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
