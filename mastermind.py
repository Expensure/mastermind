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


def feedback(guess, guess_me, kleur_aantal):
    """
    :param guess: Current guess
    :param guess_me: Secret code
    :return: Result of comparing guess and guess_me with pins.
    """
    temp_guess = [False, False, False, False]
    temp_guess_me = [False, False, False, False]
    blacks = 0
    whites = 0
    # Finds blacks and marks their index as used
    for i in range(kleur_aantal):
        if guess[i] == guess_me[i]:
            blacks += 1
            temp_guess[i] = True
            temp_guess_me[i] = True
    # Finds whites but skips the used indexes
    for i in range(kleur_aantal):  # guess index
        for j in range(kleur_aantal):  # code index
            if guess[j] == guess_me[i] and temp_guess_me[i] == False:
                whites += 1
                temp_guess[j] = True
                temp_guess_me[i] = True
    return blacks, whites


def guess_self(lst, guess_me, game, attempts):
    # Singleplayer game, creates a recursive algorithm that is finished when the random code has been guessed or the
    # amount of turns has passed.
    if game:
        if attempts == 10:
            return 'YOU LOSE, code was', guess_me

        else:
            guess = 'error'  # Om while-loop goed te laten verlopen

            while guess not in all_combinations:  # For loop zorgt ervoor dat er altijd een werkende input uitkomt
                guess = string_to_list(
                    input("geef " + str(kleur_aantal) + " letters aan elkaar, keuze uit " + hand_list))
                if guess not in all_combinations:  # Als input niet goed is, geeft aan speler aan dat het fout is
                    print("Foute input, probeer iets zoals 'RGBY' in te vullen")

            correct, existing = feedback(guess, guess_me, kleur_aantal)  # Laat de gok testen
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


def make_guess_me(all_combinations):
    guess_me = 'error'
    while guess_me not in all_combinations:  # For loop zorgt ervoor dat er altijd een werkende input uitkomt
        guessnonlist = input("Maak een code voor de cpu om te raden, geef " + str(
            4) + " letters aan elkaar, keuze uit " + "R,G,B of Y")
        guess_me = string_to_list(guessnonlist)
        if guess_me not in all_combinations:  # Als input niet goed is, geeft aan gebruiker door dat het fout is
            print("Foute input, probeer iets zoals 'RGBY' in te vullen")
    return guess_me


def simple_algorithm():
    # Bron: https://canvas.hu.nl/courses/22629/files/1520303/download?wrap=1
    # Eerst een geheime code maken voor de computer om te raden
    guess_me = make_guess_me(all_combinations)
    all_possibilities = all_combinations

    def compare_score(guess, guess_me, all_possibilities):
        """
        :param guess: Current random guess
        :param guess_me: Secret code
        :param all_possibilities: All possible codes
        :return: all_possibilities, but most codes have been removed because they are not the expected result.
        """
        new_temp_list = []
        print("Ik gokte:       ", guess)
        guess_result = feedback(guess, guess_me, kleur_aantal)
        for i in all_possibilities:
            others_result = feedback(i, guess_me, kleur_aantal)
            if others_result != guess_result:
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
            return results(guess, tries, all_possibilities)

    result = results('AAAA', 0, all_possibilities)
    return result


def narrow_down(result, guess_me, S):
    # Removes all from S that have
    wrong_lst = []
    for i in S:
        result_of_poss = feedback(i, guess_me, 4)
        if result_of_poss != result:
            wrong_lst.append(i)
    return wrong_lst


def make_guess(S):
    T_minor = []
    for i in S:
        T = [[[0, 0], 0], [[0, 1], 0], [[0, 2], 0], [[0, 3], 0], [[0, 4], 0], [[1, 0], 0], [[1, 1], 0],[[1, 2], 0], [[1, 3], 0], [[2, 0], 0], [[2, 1], 0], [[2, 2], 0], [[3, 0], 0], [[4, 0], 0]]
        for j in S:
            results = feedback(i,j,4)
            indexcounter = 0
            for result in T:
                if results == result[0]:
                    T[indexcounter][1] += 1
                indexcounter += 1
        T.sort(key=lambda result: result[1])
        T_minor += [[i, T[-1][1]]]
    T_minor.sort(key=lambda result: result[1])
    return T_minor[0][0]


def play_worstcase_algorithm():
    color_count = 4
    color_listy = ["R", "B", "G", "Y"]
    guess = ['R', 'R', 'B', 'B']
    S = (combination_list([x for x in color_listy], color_count))
    # print(len(S))
    S_minor = S
    guess_me = make_guess_me(S)
    attempt = 1
    while True:
        print("I guessed", guess)
        result = feedback(guess, guess_me, 4)
        if result == (4, 0):
            return f"Code was guessed in {attempt} attempts"
        S = narrow_down(result, guess_me, S)
        guess = make_guess(S)
        attempt+=1

# print(feedback(["R","R","R","R"], ["R","R","B","B"],4)) # Hoort (2,0) te geven
spelkeuze = int(input(
    "Wil je zelf spelen(0), simpelalgoritme(1), worstcase(2) of jasper's algoritme gebruiken? toets 0,1,2 of 3 in "))
if spelkeuze == 2:
    print(play_worstcase_algorithm())
else:
    kleur_div = int(input("Uit hoeveel kleuren kan er worden gekozen? Maximaal 10 invullen a.u.b "))
    kleur_aantal = int(input("Hoeveel kleuren moeten er geraden worden"))
    color_list = ["R", "B", "G", "Y", "O", "P", "Z", "W", "C", "M"]
    color_list = actual_color_list(color_list)
    print(color_list)
    hand_list = list_to_string(color_list)
    all_combinations = (combination_list([x for x in color_list], kleur_aantal))
    if spelkeuze == 0:
        guess_self(all_combinations, None, False, 0)
    elif spelkeuze == 1:
        random_code, attempts = simple_algorithm()
        print('The secret code:', random_code, 'has been found in ', attempts, 'attempts.')
