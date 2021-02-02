import random


def Game(ColorString):
    Colors = ["R", "B", "G", "Y", "O", "P", "Z", "W", "C", "M"]
    ActualColorList = []
    for i in range(0, int(ColorString)):
        ActualColorList.append(Colors[i])
    return ActualColorList


def Guessing():
    ColorString = input("Met hoeveel kleuren wilt u spelen? ")
    CodeLength = input("Hoe lang moet de code zijn? ")
    ColorList = Game(ColorString)
    Guesses = 0
    Choice = int(input("Wilt u dat de computer raadt(antwoord met 1), of dat u zelf de code raadt(antwoord met 0)?"))
    if Choice == 0:
        Guessthiscode = []
        for i in range(0, int(CodeLength)):
            n = random.randint(0, len(ColorList) - 1)
            Guessthiscode.append(ColorList[n])
        print(Guessthiscode)
        while Guesses <= 10:
            RoundSummary = []
            InputList = []
            PreInput = input(
                "Maak een gok voor een code met " + CodeLength + " letters, gebruik de letters " + str(ColorList))
            for i in PreInput:
                InputList.append(i)
            if len(InputList) != len(CodeLength):
                print("Error: De code bestaat uit " + CodeLength + " letters, en niet uit " + str(len(InputList)))
            print(InputList)

            tempCode = Guessthiscode
            for i in range(0,len(InputList)):  # Als een item in de lijst op dezelfde plaats staat in de codelijst, staat er een X.
                for j in tempCode:
                    if i == j and list.index(i) == list.index(j):
                        RoundSummary.append("X")
                        InputList.pop(i), tempCode.pop(i)
                    elif i==j:
                        RoundSummary.append("O")
                        tempCode.pop(j)
                    else:
                        RoundSummary.append("-")

            if RoundSummary == ["X", "X", "X", "X"]:
                print("Gefeliciteerd, u heeft gewonnen.")
                return None
            else:
                print(str(RoundSummary))
            if Guesses == 10:
                print("Game Over, de code was " + str(Guessthiscode))
                return None
            Guesses += 1

    elif Choice == 1:

        def feedback(code, codeGuess):
            positionCorrect = 0
            colorCorrect = 0
            codeList = []
            codeList += codeGuess
            for color in code:
                for p in codeList:
                    if color == p:
                        colorCorrect += 1
                        codeList.remove(p)
                        break
            for i in range(len(codeGuess)):
                if codeGuess[i] == code[i]:
                    positionCorrect += 1
            colorCorrect -= positionCorrect
            return positionCorrect, colorCorrect

        import CodeCheck as CodeCheck

        def combinationList(ActualColorList, CodeLength):
            combinations: []
            for color1 in ActualColorList:
                if CodeLength > 1:
                    for color2 in ActualColorList:
                        if CodeLength > 2:
                            for color3 in ActualColorList:
                                if CodeLength > 3:
                                    for color4 in ActualColorList:
                                        if CodeLength > 4:
                                            for color5 in ActualColorList:
                                                if CodeLength > 5:
                                                    for color6 in ActualColorList:
                                                        if CodeLength > 6:
                                                            for color7 in ActualColorList:
                                                                if CodeLength > 7:
                                                                    for color8 in ActualColorList:
                                                                        combinations.append(
                                                                            [color1, color2, color3, color4, color5,
                                                                             color6, color7, color8])
                                                                        break
                                                                else:
                                                                    combinations.append(
                                                                        [color1, color2, color3, color4, color5, color6,
                                                                         color7])
                                                                break
                                                        else:
                                                            combinations.append(
                                                                [color1, color2, color3, color4, color5, color6])
                                                        break
                                                else:
                                                    combinations.append([color1, color2, color3, color4, color5])
                                                break
                                        else:
                                            combinations.append([color1, color2, color3, color4])
                                        break
                                else:
                                    combinations.append([color1, color2, color3])
                                    break
                        else:
                            combinations.append([color1, color2])
                            break
                else:
                    combinations.append([color1])
                    break
            return sorted(combinations)

        def SimpleAlgorithm(possibleCode, gameTurn, codeGuess):  # A Simple Strategy
            newPossibleCode = []
            newPossibleCode += combinationList()
            if gameTurn > 0:
                newPossibleCode.remove(codeGuess)
                for possibleCode in possibleCode:
                    check = CodeCheck.feedback(codeGuess, possibleCode)
                    if check != feedback:
                        if possibleCode in newPossibleCode:
                            newPossibleCode.remove(possibleCode)
            return newPossibleCode


Guessing()
