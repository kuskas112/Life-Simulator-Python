import pygame
import random
import time

# Задание цветов
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
blue = (0, 0, 255)

references = {}


# Отобразить все цвета
def PrintAllCells():
    for row in range(len(field)):
        for column in range(len(field[row])):
            # Если на данной клетке кто то стоял
            if (column, row) in references:
                # И если этот список не пуст
                if len(references[(column, row)]) > 0:
                    # Закрашивание клетки цветом последнего сутпившего
                    field[row][column].color = references[(column, row)][-1].color
                # Иначе закрашивание белым
                else:
                    field[row][column].color = white
            else:
                field[row][column].color = white
            field[row][column].PrintCell()


def AddRow():
    field.append([0] * 100)
    for x in range(100):
        field[-1][x] = Cell(x, len(field) - 1, white)


def AddColumn():
    for x in range(len(field)):
        field[x].append(Cell(len(field[x]), x, white))


# Функции создания организмов
def CreatePredator():
    i = random.randint(0, 99)
    j = random.randint(0, 99)
    obj = Predator(i, j)
    obj.Randomise()
    predators.append(obj)


def CreateGrassFeeding():
    i = random.randint(0, 99)
    j = random.randint(0, 99)
    obj = GrassFeeding(i, j)
    obj.Randomise()
    grassFeedings.append(obj)


def CreateOmnivore():
    i = random.randint(0, 99)
    j = random.randint(0, 99)
    obj = Omnivore(i, j)
    obj.Randomise()
    omnivores.append(obj)


def CreateGoodPlant():
    i = random.randint(0, 99)
    j = random.randint(0, 99)
    obj = GoodPlant(i, j)
    obj.age = random.randint(1, 20)
    obj.mass = obj.age
    obj.maxAge = random.randint(25, 45)
    goodPlants.append(obj)
    references[(j, i)] = [obj]


def CreateBadPlant():
    i = random.randint(0, 99)
    j = random.randint(0, 99)
    obj = BadPlant(i, j)
    obj.age = random.randint(1, 20)
    obj.mass = obj.age
    obj.maxAge = random.randint(25, 45)
    badPlants.append(obj)
    references[(j, i)] = [obj]


def MoveAnimals():
    for animal in animals:
        y1 = animal.location[1]
        x1 = animal.location[0]
        animal.Move()
        y = animal.location[1]
        x = animal.location[0]
        if (x1, y1) in references:
            if y1 != y or x1 != x:
                if animal in references[(x1, y1)]:
                    references[(x1, y1)].remove(animal)
        if (x, y) in references:
            if animal not in references[(x, y)]:
                references[(x, y)].append(animal)
                survived = Survive(references[(x, y)])
                for creature in references[(x, y)]:
                    if creature not in survived:
                        references[(x, y)].remove(creature)
                        KillCreature(creature)
        else:
            references[(x, y)] = [animal]


def KillCreature(creature):
    if isinstance(creature, Predator):
        predators.remove(creature)
        animals.remove(creature)
    elif isinstance(creature, GrassFeeding):
        grassFeedings.remove(creature)
        animals.remove(creature)
    elif isinstance(creature, Omnivore):
        omnivores.remove(creature)
        animals.remove(creature)
    elif isinstance(creature, GoodPlant):
        goodPlants.remove(creature)
    elif isinstance(creature, BadPlant):
        badPlants.remove(creature)


def BornCreature(creature):
    creature.age = 0
    creature.mass = 0
    creature.maxAge = random.randint(25, 45)
    if isinstance(creature, Predator):
        creature.hunger = 0
        creature.gender = random.choice(['m', 'f'])
        creature.agression = random.randint(1,20)
        predators.append(creature)
        animals.append(creature)
    elif isinstance(creature, GrassFeeding):
        creature.hunger = 0
        creature.gender = random.choice(['m', 'f'])
        grassFeedings.append(creature)
        animals.append(creature)
    elif isinstance(creature, Omnivore):
        creature.hunger = 0
        creature.gender = random.choice(['m', 'f'])
        creature.agression = random.randint(1, 20)
        omnivores.append(creature)
        animals.append(creature)
    elif isinstance(creature, GoodPlant):
        goodPlants.append(creature)
    elif isinstance(creature, BadPlant):
        badPlants.append(creature)

def OldAge():
    for cell in references.keys():
        for creature in references[cell]:
            # Животное стареет на единицу
            creature.age += 1
            # Животное прибавляет в весе
            creature.mass += 1
            # Масса и голод не должны быть больше 20
            creature.mass = min(creature.mass, 20)
            if 'Plant' not in creature.name():
                # Животное голодает
                creature.hunger += 2
                creature.hunger = min(creature.hunger, 20)
            if creature.age >= creature.maxAge:
                KillCreature(creature)
                references[cell].remove(creature)


def Survive(list):
    creaturesOnCell = {
        'Predator': [],
        'GrassFeeding': [],
        'Omnivore': [],
        'GoodPlant': [],
        'BadPlant': [],
    }
    # Нахождение всех животных на клетке
    # Помещение их в словарь
    plants = creaturesOnCell['GoodPlant'] + creaturesOnCell['BadPlant']
    for animal in list:
        creaturesOnCell[animal.name()].append(animal)
    if len(creaturesOnCell['Predator']) > 0:
        # Поиск агрессивных хищников, готовых к нападению
        agressivePreds = []
        for pred in creaturesOnCell['Predator']:
            if pred.hunger >= 10:
                agressivePreds.append(pred)
        # Битва агрессивных хищников между собой, пока не останется 1 или 0
        while len(agressivePreds) > 1:
            strongestPred = None
            # Поиск сильнейшего хищника
            for pred in agressivePreds:
                if not strongestPred or pred.GetPower() > strongestPred.GetPower():
                    strongestPred = pred
            # Битва сильнейшего хишника с первым слабее его
            if strongestPred:
                for pred in agressivePreds:
                    if pred is not strongestPred:
                        # Погибщий хищник удаляется
                        # Сильнейший хищник уталяет голод,
                        # съев менее сильного
                        strongestPred.hunger -= pred.mass
                        creaturesOnCell['Predator'].remove(pred)
                        agressivePreds.remove(pred)
                        strongestPred.hunger = max(strongestPred.hunger, 0)
                        # Если сильнейший хищник наелся,
                        # значит он больше не агрессивен
                        if strongestPred.hunger < 5:
                            agressivePreds.remove(strongestPred)
                            break
        # Если в клетке есть травоядные, оставшийся сильнейший хищник
        # попытается в первую очередь съесть их
        if len(agressivePreds) > 0:
            pred = agressivePreds[0]
            if len(creaturesOnCell['GrassFeeding']) > 0:
                # Случайное травоядное - жертва хищника
                victim = random.choice(creaturesOnCell['GrassFeeding'])
                # Шанс победы хищника зависит от голода
                chance = pred.hunger * 5
                if random.randint(1, 100) <= chance:
                    # Травоядное съедено
                    pred.hunger -= victim.mass
                    creaturesOnCell['GrassFeeding'].remove(victim)
                    # Голод не может быть отрицательным
                    pred.hunger = max(pred.hunger, 0)
                    if pred.hunger <= 5:
                        # Если хищник наелся, он больше не аггресивен
                        agressivePreds.pop(0)
        # Если в клетке остался голодный хищник,
        # который не смог поймать травоядное,
        # он попытается напасть на всеядное
        if len(agressivePreds) > 0:
            pred = agressivePreds[0]
            if len(creaturesOnCell['Omnivore']) > 0:
                victim = random.choice(creaturesOnCell['Omnivore'])
                if pred.GetPower() > victim.GetPower():
                    # Хищник победил
                    pred.hunger -= victim.mass
                    creaturesOnCell['Omnivore'].remove(victim)
                    # Голод не может быть отрицательным
                    pred.hunger = max(pred.hunger, 0)
                    if pred.hunger <= 5:
                        # Если хищник наелся, он больше не аггресивен
                        agressivePreds.pop(0)
                else:
                    # Всеядное победило
                    victim.hunger -= pred.mass
                    victim.hunger = max(victim.hunger, 0)
                    creaturesOnCell['Predator'].remove(pred)
                    agressivePreds.pop(0)
    if len(creaturesOnCell['Omnivore']) > 0:
        agressiveOmnivores = []
        # Поиск агрессивных (голодных) всеядных
        for omni in creaturesOnCell['Omnivore']:
            if omni.hunger > 10:
                agressiveOmnivores.append(omni)
        # Первым делом всеядное попытается
        # уталить голод растениями
        for omni in agressiveOmnivores:
            if len(plants) > 0:
                plant = random.choice(plants)
                if plant.name() == "GoodPlant":
                    # удалось съесть питательное растение
                    omni.hunger -= plant.age
                    plants.remove(plant)
                    omni.hunger = max(omni.hunger, 0)
                    if omni.hunger < 5:
                        agressiveOmnivores.remove(omni)
                elif plant.name() == "BadPlant":
                    # Съедено ядовитое растение
                    if random.randint(1, 2) == 2:
                        # Всядное погибло
                        creaturesOnCell['Omnivore'].remove(omni)
                        plants.remove(plant)

            else:
                break
        # Во вторую очередь всеядные нападут на травоядных
        for omni in agressiveOmnivores:
            if len(creaturesOnCell['GrassFeeding']) > 0:
                # Случайное травоядное - жертва всеядного
                victim = random.choice(creaturesOnCell['GrassFeeding'])
                # Шанс победы всеядного зависит от голода
                chance = omni.hunger * 5
                if random.randint(1, 100) <= chance:
                    # Травоядное съедено
                    omni.hunger -= victim.mass
                    creaturesOnCell['GrassFeeding'].remove(victim)
                    # Голод не может быть отрицательным
                    omni.hunger = max(omni.hunger, 0)
                    if omni.hunger <= 5:
                        # Если всеядное наелось, оно больше не аггресивно
                        agressiveOmnivores.remove(omni)
            else:
                break

        # В последнюю очередь травоядные нападут на хищников
        for omni in agressiveOmnivores:
            if len(creaturesOnCell['Predator']) > 0:
                victim = random.choice(creaturesOnCell['Predator'])
                if omni.GetPower() > victim.GetPower():
                    # Всеядное победило
                    omni.hunger -= victim.mass
                    creaturesOnCell['Predator'].remove(victim)
                    # Голод не может быть отрицательным
                    if omni.hunger < 0:
                        omni.hunger = 0
                    if omni.hunger <= 5:
                        agressiveOmnivores.remove(omni)
                else:
                    # Хищник победил
                    victim.hunger -= omni.mass
                    if victim.hunger < 0:
                        victim.hunger = 0
                    creaturesOnCell['Omnivore'].remove(omni)
            else:
                break
    if len(creaturesOnCell['GrassFeeding']) > 0:
        # Поиск голодных травоядных
        hungerGrassFeeding = []
        for grass in creaturesOnCell['GrassFeeding']:
            if grass.hunger >= 10:
                hungerGrassFeeding.append(grass)
        for grass in hungerGrassFeeding:
            if len(plants) > 0:
                plant = random.choice(plants)
                # Удалось съесть питательное растение
                if plant.name() == "GoodPlant":
                    grass.hunger -= plant.age
                    grass.hunger = max(grass.hunger, 0)
                    plants.remove(plant)
                    if grass.hunger < 5:
                        hungerGrassFeeding.remove(grass)
                else:
                    if random.choice(1, 2) == 2:
                        # Съедено ядовитое растение
                        creaturesOnCell['GrassFeeding'].remove(grass)
                        plants.remove(plant)
            else:
                break

    survivedCreatures = creaturesOnCell['Predator'] + \
                        creaturesOnCell['GrassFeeding'] + \
                        creaturesOnCell['Omnivore'] + \
                        plants
    return survivedCreatures


def Multiply():
    newBornes = []
    for cell in references.keys():
        adultAnimals = {
            ('Predator', 'm'): [],
            ('Predator', 'f'): [],
            ('GrassFeeding', 'm'): [],
            ('GrassFeeding', 'f'): [],
            ('Omnivore', 'm'): [],
            ('Omnivore', 'f'): [],
        }
        plants = []
        for creature in references[cell]:
            if creature.name() != 'GoodPlant' and creature.name() != 'BadPlant':
                # Добавление животного в список размножающихся
                if creature.age >= 10:
                    adultAnimals[(creature.name(), creature.gender)].append(creature)
            else:
                # Добавление растений в группу для размножения
                plants.append(creature)

        for key in adultAnimals.keys():
            name = key[0]
            while len(adultAnimals[name, 'm']) > 0 and len(adultAnimals[name, 'f']) > 0:
                animal1 = random.choice(adultAnimals[name, 'm'])
                animal2 = random.choice(adultAnimals[name, 'f'])
                x = animal1.location[0]
                y = animal1.location[1]
                # выбор локации для рождения
                newBornLocation = [
                    (x + 1, y),
                    (x, y + 1),
                    (x - 1, y),
                    (x, y - 1),
                    (x + 1, y + 1),
                    (x - 1, y - 1),
                ]
                # Если на клетке кто то стоит
                # то она не подходит для рождения
                badLocactions = []
                for loc in newBornLocation:
                    if loc in references:
                        if len(references[loc]) > 0:
                            badLocactions.append(loc)
                for x in badLocactions:
                    newBornLocation.remove(x)
                if len(newBornLocation) > 0:
                    newBornLocation = random.choice(newBornLocation)
                    if isinstance(animal1, Predator):
                        creature = Predator(
                            newBornLocation[0],
                            newBornLocation[1]
                        )
                        BornCreature(creature)
                        newBornes.append(creature)
                    elif isinstance(animal1, GrassFeeding):
                        creature = GrassFeeding(
                            newBornLocation[0],
                            newBornLocation[1]
                        )
                        BornCreature(creature)
                        newBornes.append(creature)
                    elif isinstance(animal1, Omnivore):
                        creature = Omnivore(
                            newBornLocation[0],
                            newBornLocation[1]
                        )
                        BornCreature(creature)
                        newBornes.append(creature)
                    adultAnimals[name, 'm'].remove(animal1)
                    adultAnimals[name, 'f'].remove(animal2)
        for plant in plants:
            if random.randint(1, 10) == 10:
                plant.age -= 1
                x = plant.location[0]
                y = plant.location[1]
                newBornLocation = [
                    (x + 1, y),
                    (x, y + 1),
                    (x - 1, y),
                    (x, y - 1),
                    (x + 1, y + 1),
                    (x - 1, y - 1),
                ]
                badLocactions = []
                for loc in newBornLocation:
                    if loc in references:
                        if len(references[loc]) > 0:
                            badLocactions.append(loc)
                for x in badLocactions:
                    newBornLocation.remove(x)
                if len(newBornLocation) > 0:
                    newBornLocation = random.choice(newBornLocation)
                    if plant.name() == 'GoodPlant':
                        creature = GoodPlant(
                            newBornLocation[0],
                            newBornLocation[1]
                        )
                        BornCreature(creature)
                        newBornes.append(creature)
                    elif plant.name() == 'BadPlant':
                        creature = BadPlant(
                            newBornLocation[0],
                            newBornLocation[1]
                        )
                        BornCreature(creature)
                        newBornes.append(creature)
    for creature in newBornes:
        if (creature.location[0], creature.location[1]) in references:
            references[(creature.location[0], creature.location[1])].append(creature)
        else:
            references[(creature.location[0], creature.location[1])] = [creature]


# Родительский класс для животных
class Animal:
    def __init__(self, x, y):
        self.location = [x, y]

    # Задание случайных характеристик
    def Randomise(self):
        self.age = random.randint(1, 20)
        self.maxAge = random.randint(25, 45)
        self.mass = random.randint(1, 20)
        self.hunger = random.randint(1, 20)
        self.agression = random.randint(1, 20)
        self.gender = random.choice(['m', 'f'])

        # Метод для передвижения

    def Move(self):
        decision = random.randint(0, 1)
        # шанс 1/2 остаться на месте
        if decision == 0:
            return
        else:
            # выбор одного из 8 возможных направлений
            # направления считаются от верхнего по часовой стрелке
            direction = random.randint(1, 8)
            match direction:
                case 1:
                    self.location[1] += 1
                case 2:
                    self.location[0] += 1
                    self.location[1] += 1
                case 3:
                    self.location[0] += 1
                case 4:
                    self.location[0] += 1
                    self.location[1] -= 1
                case 5:
                    self.location[1] -= 1
                case 6:
                    self.location[0] -= 1
                    self.location[1] -= 1
                case 7:
                    self.location[0] -= 1
                case 8:
                    self.location[0] -= 1
                    self.location[1] += 1
            if self.location[1] < 0:
                self.location[1] = len(field) - 1
            if self.location[0] < 0:
                self.location[0] = len(field[self.location[1]]) - 1
            while self.location[1] >= len(field):
                AddRow()
            while self.location[0] >= len(field[self.location[1]]):
                AddColumn()


# Классы организмов
class Predator(Animal):
    color = red

    def GetPower(self):
        return self.hunger + self.mass + self.agression

    def name(self):
        return "Predator"


class GrassFeeding(Animal):
    color = orange

    def name(self):
        return "GrassFeeding"


class Omnivore(Animal):
    color = blue

    def GetPower(self):
        return self.hunger + self.mass + self.agression

    def name(self):
        return "Omnivore"


class GoodPlant:
    color = green
    age = None
    mass = age
    maxAge = None

    def __init__(self, x, y):
        self.location = [x, y]

    def name(self):
        return "GoodPlant"


class BadPlant:
    color = black
    age = None
    mass = age
    maxAge = None

    def __init__(self, x, y):
        self.location = [x, y]

    def name(self):
        return "BadPlant"


# Класс одной клетки
class Cell:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    # Закрашивание одной клетки
    def PrintCell(self):
        row = self.y
        column = self.x
        color = self.color
        pygame.draw.rect(screen, color, [(cell_size + 1) * column + 1, (cell_size + 1) * row + 1, cell_size, cell_size])


# Инициализация Pygame
pygame.init()

# Создание экрана
# Размеры экрана берутся с учетом линий между клетками
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# Создание поля из 100 на 100 клеток
cell_size = 6
field = [[0 for x in range(100)] for y in range(100)]

# Отрисовка поля
for row in range(100):
    color = white
    for column in range(100):
        field[column][row] = Cell(column, row, color)
        pygame.draw.rect(screen, color, [(cell_size + 1) * column + 1, (cell_size + 1) * row + 1, cell_size, cell_size])

# Списки для организмов
predators = []
grassFeedings = []
omnivores = []
goodPlants = []
badPlants = []

# Создание организмов
for x in range(1000):
    CreatePredator()
    CreateGrassFeeding()
    CreateOmnivore()

for x in range(10):
    CreateGoodPlant()
    CreateBadPlant()

# Список всех животных
animals = predators + grassFeedings + omnivores

while True:
    # Отображение всех клеток
    PrintAllCells()
    # Обновление экрана
    pygame.display.flip()
    # Остановка на единицу времени (0.3 сек)
    k = 0
    for x in references.values():
        k+=len(x)
    if k == 0:
        pygame.quit()
        quit()
    MoveAnimals()
    OldAge()
    Multiply()
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # выход из игры при нажатии на крестик
            pygame.quit()
            quit()
