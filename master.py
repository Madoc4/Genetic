import pygame
from species import Species 
from nutrients import Nutrient
from button import Button
import random

# TO-DO: if there is no food or water pathfinding breaks

def create_species(count, generation, screen_width, screen_height):
    species_list = []

    for i in range(count):
        new_species = Species(i + 1, 0, generation, screen_width, screen_height)
        species_list.append(new_species)

    return species_list

def create_nutrients(count, screen_width, screen_height):
    nutrients = []

    food = [
        Nutrient(random.randint(0, screen_width), random.randint(0, screen_height), 'food')
        for _ in range(count)
    ]

    water = [
        Nutrient(random.randint(0, screen_width), random.randint(0, screen_height), 'water')
        for _ in range(count)
    ]

    nutrients += food + water

    return nutrients

def main():
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    FPS = 30
    frames = 0
    generation = 1
    running = True

    initial_count = 10
    species = create_species(initial_count, generation, SCREEN_WIDTH, SCREEN_HEIGHT)
    master = species[:]

    nutrients = create_nutrients(20, SCREEN_WIDTH, SCREEN_HEIGHT)

    gen_button = Button(f'Generation {generation}', SCREEN_WIDTH-100, 10, 'freesansbold.ttf', 15, (255, 255, 255), False)
    num_species = Button(f'Num species: {len(species)}', SCREEN_WIDTH/2 - 50, 10, 'freesansbold.ttf', 15, (255, 255, 255), False)
    quit_button = Button('Quit', 0, 0, 'freesansbold.ttf', 15, (255, 255, 255), True)
    buttons = [gen_button, num_species, quit_button]
    species_by_gen = {}
    species_by_gen[generation] = master

    alive_at_end = {1: initial_count}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if button.check_click(mouse_pos):
                    if button.text == 'Quit':
                        running = False

        SCREEN.fill((255, 255, 255))

        if generation not in species_by_gen:
            species_by_gen[generation] = []

        for nutrient in nutrients:
            if nutrient.consumed:
                nutrients.remove(nutrient)
            nutrient.draw(SCREEN)

        for s1 in species:
            if s1.dead:
                species.remove(s1)
                num_species.text=f'Num species: {len(species)}'
                num_species.render_text()

            for s2 in species:
                if s2.dead:
                    species.remove(s2)
                    num_species.text=f'Num species: {len(species)}'
                    num_species.render_text()

                if s1.size > s2.size*2:
                    s1.hunt(s2, generation)

                elif s1 != s2:
                    child = s1.crossover(s2, generation, frames)
                    if child:
                        species.append(child)
                        master.append(child)
                        species_by_gen[generation].append(child)

            s1.decision([nutrient for nutrient in nutrients if nutrient.type == 'food'],
                        [nutrient for nutrient in nutrients if nutrient.type == 'water'])
            s1.update()
            s1.draw(SCREEN)

        if len(nutrients) < 5:
            generation += 1
            gen_button.text = f'Generation {generation}'
            gen_button.render_text()
            alive_at_end[generation] = len(species)
            for s in species:
                s.age += 1
            nutrients += create_nutrients(20 - len(nutrients), SCREEN_WIDTH, SCREEN_HEIGHT)

        if len(species) == 0:
            alive_at_end[generation] = 0
            dead_button = Button('All species died', SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 - 50, 'freesansbold.ttf', 15, (255, 255, 255), False)
            num_species.text = f'Num species: {len(species)}'
            num_species.render_text()
            dead_button.draw(SCREEN)

        for button in buttons:
            button.draw(SCREEN)
            if button.text == 'Quit':
                button.check_hover(pygame.mouse.get_pos(), SCREEN)
        pygame.display.flip()
        clock.tick(FPS)
        frames += 1


    with open('species_history.txt', 'w') as f:
        f.write(f'Total generations: {max(species_by_gen)} \n\n')
        for g in species_by_gen:
            f.write(f'Generation {g}:\n')
            for s in species_by_gen[g]:
                if s.gen == g:
                    f.write(f'{s}\n')
            f.write('\n\n')
    
    with open('population_by_gen.txt', 'w') as f:
        for g in alive_at_end:
            f.write(f'Generation {g}: {alive_at_end[g]}\n')
    pygame.quit()

if __name__ == "__main__":
    main()
