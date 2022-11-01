import pygame, sys
from brickout.game import Brickout

if __name__ == "__main__":
    # Start the game
    brickout = Brickout("SPLASH")
    brickout.run()

    # Closing the game
    pygame.quit()
    sys.exit()