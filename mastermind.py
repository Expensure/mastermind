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
    # Maakt van een string een lijst zodat de lijst vergeleken kan worden met de combinatielijst
    lst = []
    lst[:0] = string
    return lst


def feedback(guess, guess_me):
    blacks = 0
    whites = 0
    used = [False, False, False, False]

    # search only blacks and mark as "used" black elements
    for i in range(4):
        if guess[i] == guess_me[i]:
            blacks += 1
            used[i] = True

    # search only whites (but skip "used" elements)
    # and mark as "used" every white element in code
    # so it can't be used twice
    for i in range(4):  # guess index
        for j in range(4):  # code index
            if not used[j] and guess[j] == guess_me[i]:
                whites += 1
                used[j] = True

    wrongs = len(guess_me) - (blacks + whites)
    return blacks, whites, wrongs


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

            correct, existing, wrong = feedback(guess, guess_me)  # Laat de gok testen
            print("Je hebt ", correct, " correct, en verder heb je", existing, "kleuren")

            if correct == len(guess_me):  # Winning condition
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
    all_possibilities = all_combinations

    def compare_score(guess, guess_me, all_possibilities):
        new_temp_list = []
        guess_result = feedback(guess, guess_me)
        for i in all_possibilities:
            print (guess)
            print(i)
            others_result = feedback(i, guess_me)
            print(others_result)
            if others_result == guess_result:
                new_temp_list.append(i)
        return new_temp_list

    # Simpel algoritme door resultaat van de gok te vergelijken met alle andere mogelijkheden
    def results(guess, tries, all_possibilities):
        if guess == guess_me:
            return guess, tries
        else:
            guess = random.choice(all_possibilities)
            all_possibilities = compare_score(guess, guess_me, all_possibilities)
            tries += 1
            print(guess)
            print(all_possibilities)
            return results(guess, tries, all_possibilities)

    result = results('AAAA', 0, all_possibilities)
    return result


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
