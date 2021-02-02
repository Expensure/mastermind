import random


def actual_color_list(colors):
    # Verkleint de totale lijst om een gelimiteerde hoeveelheid kleuren te gebruiken.
    lst = []
    for i in range(0, kleur_div):
        lst.append(colors[i])
    return lst


def combination_list(all_cols, color_amount):
    # Maakt alle mogelijke combinaties van de hoeveelheid letters en kleuren aan
    if color_amount == 0:
        return [[]]
    combinations = []
    for i in range(0, len(all_cols)):
        item = all_cols[i]
        for p in combination_list(all_cols, color_amount - 1):
            combinations.append([item] + p)
    return combinations


def list_to_string(lst):
    # Maakt van een lijst een string met komma's ertussen zodat er informatie gegeven kan worden
    string = ""
    for ele in lst:
        string += ele
        string += ', '
    return string


def string_to_list(string):
    # Maakt van een string een lijst zodat de lijst gebruikt kan worden samen met de combinatielijst
    lst = []
    lst[:0] = string
    return lst


def feedback(guess, guess_me):
    # Kijkt de resultaten van de gok van speler of computer na
    positionCorrect = 0
    colorCorrect = 0
    codeList = []
    codeList += guess_me
    for color in guess:
        for p in codeList:
            if color == p:
                colorCorrect += 1
                codeList.remove(p)
                break
    for i in range(len(guess_me)):
        if guess_me[i] == guess[i]:
            positionCorrect += 1
    colorCorrect -= positionCorrect
    return positionCorrect, colorCorrect


def guess_self(lst, guess_me, game, attempts):
    if game:
        if attempts == 10:
            return 'YOU LOSE, code was', guess_me

        else:
            guess = 'error'  # Om while-loop goed te laten verlopen

            while guess not in all_combinations:  # For loop zorgt ervoor dat er altijd een werkende input uitkomt
                guessnonlist = input("geef " + str(kleur_aantal) + " letters aan elkaar, keuze uit " + hand_list)
                guess = string_to_list(guessnonlist)
                if guess not in all_combinations:  # Als input niet goed is, geeft aan speler aan dat het fout is
                    print("Foute input, probeer iets zoals 'RGBY' in te vullen")

            correct, existing = feedback(guess, guess_me)  # Laat de gok testen
            print("Je hebt ", correct, " correct, en verder heb je", existing, "kleuren")

            if correct == 4:  # Winning condition
                print('')
                return 'YOU WIN!, de code was inderdaad', guess, '. Het kostte', attempts, 'pogingen'

            print("Dat was poging ", attempts)
            print('')
        attempts += 1
    else:
        guess_me = random.choice(lst)
        game = True
    return guess_self(lst, guess_me, game, attempts)


def simple_algorithm():
    # Bron: https://canvas.hu.nl/courses/22629/files/1520303/download?wrap=1
    # Eerst een geheime code maken voor de computer om te raden
    guess_me = 'error'
    while guess_me not in all_combinations:  # For loop zorgt ervoor dat er altijd een werkende input uitkomt
        guessnonlist = input("Maak een code voor de cpu om te raden, geef " + str(
            kleur_aantal) + " letters aan elkaar, keuze uit " + hand_list)
        guess_me = string_to_list(guessnonlist)
        if guess_me not in all_combinations:  # Als input niet goed is, geeft aan gebruiker door dat het fout is
            print("Foute input, probeer iets zoals 'RGBY' in te vullen")

    # Simpel algoritme door twee willekeurige gokken steeds te vergelijken
    temp_allcomb_list = all_combinations
    tries = 0
    while len(temp_allcomb_list) > 1:
        tries += 1
        random_code = random.choice(all_combinations)
        check1 = (feedback(random_code, guess_me))

        if check1 == (kleur_aantal, 0):
            return random_code, tries

        for i in range(len(temp_allcomb_list)):
            random_code2 = random.choice(all_combinations)

            check2 = (feedback(random_code, guess_me))

            if check1 != check2:
                temp_allcomb_list.remove(random_code2)


kleur_div = int(input("Uit hoeveel kleuren kan er worden gekozen? Maximaal 10 invullen a.u.b "))
kleur_aantal = int(input("Hoeveel kleuren moeten er geraden worden"))
color_list = ["R", "B", "G", "Y", "O", "P", "Z", "W", "C", "M"]
color_list = actual_color_list(color_list)
hand_list = list_to_string(color_list)
all_combinations = (combination_list([x for x in color_list], kleur_aantal))

spelkeuze = int(input("Wil je zelf spelen(0), of wil je dat de computer het algoritme gebruikt?(1), toets 0 of 1 in "))
if spelkeuze == 1:
    random_code, attempts = simple_algorithm()
    print('The secret code:', random_code, 'has been found in ', attempts, 'attempts.')
elif spelkeuze == 0:
    guess_self(all_combinations, None, False, 0)