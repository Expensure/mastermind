import random
import ast

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
    blacks = 0
    whites = 0
    used = []
    for i in range(kleur_aantal):
        used.append(False)
    # Finds blacks and marks their index as used
    for i in range(kleur_aantal):
        if guess[i] == guess_me[i]:
            blacks += 1
            used[i] = True

    # Finds whites but skips the used indexes
    for i in range(kleur_aantal):  # guess index
        for j in range(kleur_aantal):  # code index
            if not used[j] and guess[j] == guess_me[i]:
                whites += 1
                used[j] = True
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


def worst_case_algorithm(all_possibilities):
    # Source: YET ANOTHER MASTERMIND STRATEGY by Barteld Kooi

    def get_worst_dict():
        worst_dict = {}
        for i in all_possibilities:
            worst_dict[f"{i}"] = []
            for j in all_possibilities:
                result = feedback(i, j, 4)  # Compares every possible code with all others
                worst_dict[f"{i}"].append(result)  # Adds result of that comparison to that code in dict
        return worst_dict

    def get_all_highest(worstdict):
        all_highest = []
        for key in worstdict:  # For every code
            unilist = []
            countlist = []
            q = worstdict[key]  # Check results
            for i in q:  # Every result of the comparisons
                if i not in unilist:  # If this result hasn't been spotted yet, add it
                    unilist.append(i)
            for i in unilist:
                countlist.append(q.count(i))  # Add this result to the count, to see which comes
            highest = max(countlist)
            all_highest.append([key, unilist[countlist.index(highest)], highest])  # Adds the code, with which result is most frequent.
        return all_highest

    def results():
        all_high = get_all_highest(get_worst_dict())
        all_count = []

        for i in all_high:
            all_count.append(i[2])
        lowest = min(all_count)
        options = []
        for i in all_high:
            if i[2] <= lowest:
                options.append(i)
        return ast.literal_eval(options[0][0])
    return results()


def own_algorithm():
    return None


def play(spelkeuze):
    def comprised_simple(guess,  all_possibilities, feedbacks):
        def feedback(guess, guess_me, kleur_aantal):
            """
            :param guess: Current guess
            :param guess_me: Secret code
            :return: Result of comparing guess and guess_me with pins.
            """
            blacks = 0
            whites = 0
            used = []
            for i in range(kleur_aantal):
                used.append(False)
            # Finds blacks and marks their index as used
            for i in range(kleur_aantal):
                if guess[i] == guess_me[i]:
                    blacks += 1
                    used[i] = True

            # Finds whites but skips the used indexes
            for i in range(kleur_aantal):  # guess index
                for j in range(kleur_aantal):  # code index
                    if not used[j] and guess[j] == guess_me[i]:
                        whites += 1
                        used[j] = True
            return blacks, whites

        """
        :param guess: Current random guess
        :param all_possibilities: All possible codes
        :return: all_possibilities, but most codes have been removed because they are not the expected result.
        """
        print(len(all_possibilities), " left before")
        new_list = []
        for i in all_possibilities:
            print(feedback(guess, i, 4))
            print(feedbacks)
            if feedback(guess, i,4) == feedbacks:
                new_list.append(i)
        print(len(new_list), " left after")
        return new_list

    kleur_aantal = 4
    color_list = ["R", "B", "G", "Y"]
    all_combinations = (combination_list([x for x in color_list], kleur_aantal))
    guess_me = ['R','R','R','R'] #make_guess_me(all_combinations)
    n = 0
    feedback= 0, 0

    while True:
        #print(n)
        if spelkeuze == 2:
            if n!=0:
                all_combinations = comprised_simple(guessyay, all_combinations, feedback)
            else:
                n+=1
            guessyay = worst_case_algorithm(all_combinations)


spelkeuze = int(input(
    "Wil je zelf spelen(0), simpelalgoritme(1), worstcase(2) of jasper's algoritme gebruiken? toets 0,1,2 of 3 in "))
if spelkeuze == 2 or spelkeuze == 3:
    play(spelkeuze)
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


