import pygame
import random
import math

class Species(pygame.sprite.Sprite):
    def __init__(self, num, time, generation, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.number = num
        self.size = random.randint(5, 20)
        self.starting_size = self.size
        self.speed = 2 * math.sqrt(22-self.size) 
        self.food_requirement = self.size * 5
        self.food = self.food_requirement + 350
        self.water_requirement = self.size * 5
        self.water = self.water_requirement + 350
        self.health = 100
        self.gen = generation
        self.age = 1
        self.birthdate = time
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.parents = []
        if self.gen % 10 == 0:
            self.color = (255,0,0)
        elif self.gen % 10 == 1:
            self.color = (255,128,0)
        elif self.gen % 10 == 2:
            self.color = (255,255,0)
        elif self.gen % 10 == 3:
            self.color = (128,255,0)
        elif self.gen % 10 == 4:
            self.color = (0,255,0)
        elif self.gen % 10 == 5:
            self.color = (0,255,128)
        elif self.gen % 10 == 6:
            self.color = (0,255,255)
        elif self.gen % 10 == 7:
            self.color = (0,128,255)
        elif self.gen % 10 == 8:
            self.color = (0,0,255)
        elif self.gen % 10 == 9:
            self.color = (128,0,255)
        reproducing = False
        self.moving = False
        self.target = None
        self.eating = False
        self.dest = ''
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.dead = False
        self.last_reproduce = 3
        self.last_hunt = -1
        self.mutation_prob = .1
        self.death_reason = ''

   
    def hunt(self, other, generation):
        if math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2) < 25 and generation > self.last_hunt + 2:
            self.size += other.size/2
            self.food += 400
            print('hunt')
            # keeps same speed for now
            other.dead = True
            other.death_reason='hunted'

    def mutate(self, child):
        attribute_to_mutate = random.choice(["speed", "food_requirement", "water_requirement"])
        mutation_amount = random.uniform(-5, 5)
        setattr(child, attribute_to_mutate, getattr(child, attribute_to_mutate) + mutation_amount)

    
    def can_reproduce(self, generation):
        return self.age > self.last_reproduce and self.food > self.food_requirement and self.water > self.water_requirement

    def crossover(self, partner, generation, frames):
        if self.can_reproduce(generation) and partner.can_reproduce(generation):
            if math.sqrt((self.x - partner.x) ** 2 + (self.y - partner.y) ** 2) < 50:
                self.last_reproduce, partner.last_reproduce = generation, generation
                child = Species(self.number + 1, frames, generation, 1, 1)
                child.x, child.y = (self.x + partner.x) / 2, (self.y + partner.y) / 2
                child.parents = [self, partner]

                child.size = (self.size * 0.6 + partner.size * 0.4)
                child.size = min(child.size, 20)  

                child.speed = (self.speed + partner.speed) / 2
                child.food_requirement = (self.food_requirement + partner.food_requirement) / 2
                child.water_requirement = (self.water_requirement + partner.water_requirement) / 2
                child.color = tuple(int((a + b) / 2) for a, b in zip(self.color, partner.color))

                if random.random() < self.mutation_prob:
                    self.mutate(child)
                return child

        return None


    
    def decision(self, food, water):
            closest_food = None
            closest_food_dist = math.inf
            closest_water = None
            closest_water_dist = math.inf

            for pos in food:
                dist = math.sqrt((self.x - pos.x) ** 2 + (self.y - pos.y) ** 2)
                if dist < closest_food_dist:
                    closest_food = pos
                    closest_food_dist = dist

            for pos in water:
                dist = math.sqrt((self.x - pos.x) ** 2 + (self.y - pos.y) ** 2)
                if dist < closest_water_dist:
                    closest_water = pos
                    closest_water_dist = dist

            if self.food < self.water:
                self.dest = 'food'
                self.target = closest_food
            else:
                self.dest = 'water'
                self.target = closest_water

            self.move()



    def move(self):
        if not self.dead and self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 5:  
                step = min(self.speed, distance) / distance
                self.x += dx * step
                self.y += dy * step
                self.rect.x, self.rect.y = self.x, self.y
            else:
                self.moving = False
                self.action()


    def action(self):
        if self.dest == 'food':
            self.food += 150
            self.size += 0.25
        elif self.dest == 'water':
            self.water += 150
            self.size += 0.25 
        self.food_requirement += 2
        self.water_requirement += 2

        self.target.consumed = True
        self.target = None
        self.dest = 'idle'

    def update(self):
        self.food -= .05 * self.size 
        self.water -= .05 * self.size  

        if self.food <= self.food_requirement or self.water <= self.water_requirement:
            self.health -= 0.5

        if self.health <= 0:
            self.dead = True
            self.death_reason='starvation'
        else:
            if self.moving:
                self.move()
            elif self.eating:
                self.action()

    def draw(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, self.color, self.rect)


    def __repr__(self):
        return f'Species with starting size {self.starting_size} and ending size {self.size}. Generation {self.gen}. Lived {self.age} generations. Died: {self.dead}. {self.death_reason}'
    

    def __str__(self):
        return f'Species with starting size {self.starting_size} and ending size {self.size}. Generation {self.gen}. Lived {self.age} generations. Died: {self.dead}. {self.death_reason}'
