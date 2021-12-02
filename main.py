# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# import pygame
# from game import Game
#
# SCREEN_WIDTH = 640
# SCREEN_HEIGHT = 480
#
# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#     pygame.display.set_caption("Matematyka")
#     #Loop until the user clicks the close button.
#     done = False
#     # Used to manage how fast the screen updates
#     clock = pygame.time.Clock()
#     game = Game()
#     # -------- Main Program Loop -----------
#     while not done:
#         # --- Process events (keystrokes, mouse clicks, etc)
#         done = game.process_events()
#         # --- Game logic should go here
#         game.run_logic()
#         # --- Draw the current frame
#         game.display_frame(screen)
#         # --- Limit to 30 frames per second
#         clock.tick(30)
#
#     pygame.quit()
#
# #if __name__ == '__main__':
# #    main()
