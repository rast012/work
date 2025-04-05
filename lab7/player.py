import pygame
import os

# Initialize pygame mixer and pygame
pygame.mixer.init()
pygame.init()

# Screen dimensions
pygame.display.set_caption("Music Player")
BACKGROUND_IMAGE = pygame.image.load("player.png")
WIDTH, HEIGHT = BACKGROUND_IMAGE.get_size()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Folder containing music files
tracks = []
MUSIC_FOLDER = "/home/rustem/Projects/work/lab7/"  # Change to your music folder path
for f in os.listdir(MUSIC_FOLDER):
    if f.endswith(".mp3"): 
        tracks.append(f)
current_track = 0

# Function to play music
def play_music():
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, tracks[current_track]))
    pygame.mixer.music.play()
    print(f"Playing: {tracks[current_track]}")

# Load first track if available
if tracks:
    play_music()
else:
    print("No music files found!")

# Main loop
running = True
while running:
    screen.blit(BACKGROUND_IMAGE, (0, 0))  # Draw background
    pygame.display.update()  # Refresh screen
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  
                if not pygame.mixer.music.get_busy():
                    play_music()
            elif event.key == pygame.K_DOWN: 
                pygame.mixer.music.stop()
                print("Stopped")
            elif event.key == pygame.K_RIGHT:  
                current_track = (current_track + 1) % len(tracks)
                play_music()
            elif event.key == pygame.K_LEFT:  
                current_track = (current_track - 1) % len(tracks)
                play_music()

pygame.quit()
