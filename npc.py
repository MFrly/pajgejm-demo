from settings import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()  # Stejný sprite jako hráč
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-160, -160)  # Hitbox pro přesnější kolize
        self.interacting = False  # Flag pro interakci
    
    def interact(self):
        print("Ahoj, jak se máš? Mám pro tebe otázku!")
        answer = input("Kolik je 1+1? ")
        if answer.strip() == "2":
            print("Správně! Dobrá práce!")
        else:
            print("Špatně, zkus to příště!")
    
    def update(self, dt):
        pass  # NPC zatím nemá pohyb, ale můžeš sem později přidat logiku
