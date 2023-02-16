import pygame
import requests
from io import BytesIO
import openai
openai.api_key = "API Key"

pygame.init()

# Set up the display
display_width = 800
display_height = 600
display_surface = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("History Game")

# Set up the API request
model_engine = "image-alpha-001"
prompt = (
    "The Mona Lisa\n"
    "A portrait painting by Leonardo da Vinci.\n"
    "Considered one of the most famous paintings in the world."
)
response = openai.Image.create(model=model_engine, prompt=prompt, n=1)

# Get the image from the API response
if "data" in response and response["data"] is not None:
    image_url = response["data"][0]["url"]
    image_data = requests.get(image_url).content
    image = pygame.image.load(BytesIO(image_data))
else:
    print(f"Failed to get image from API. Response: {response}")

# Display the image
display_surface.blit(image, (0, 0))
pygame.display.update()

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
