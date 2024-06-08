from enum import Enum
from random import choice
from textwrap import dedent
from os import system, name as os_name


en_words = ("australopithecus", "platypus", "language", "nomination", "appearance", "interstellar",
            "keyboard", "assessment", "incredible", "programmer", "transcendence", "generator", "reactor",
            "calculator", "processor", "spaceship", "watchdog", "pokemon", "notebook", "electron", "inaccurate",
            "misspelled", "unaccountable", "circumcision", "transubstantiation", "electric guitar", "pellet",
            "puncture", "needle", "voyage", "frigid", "outskirts", "hangman", "alphabet", "carrier", "airport",
            "loudspeaker", "waterfall", "horology", "beginner", "ergonomic", "notebook", "agriculture", "screenshot",
            "screensaver", "doorbell", "sonata", "parallelogram", "telephone", "etruscan", "vivaldi", "democratic",
            "predecessor", "programming", "facility", "functionality", "stapler", "pencil", "space shuttle",
            "rainforest", "rythm")

es_words = ("ornitorrinco", "teclado", "calculadora", "idioma", "telecomunicaciones", "programador", "estacionario",
            "principiante", "paralelogramo", "relojes", "guitarra eléctrica", "camello", "cuaderno", "funcionalidad",
            "democracia", "montaña", "monitor", "pantalla", "pianista", "actividad paranormal", "violinista",
            "edificio", "calculadora", "procesador", "espectador", "electricidad", "ortopedia", "radiador", "sudadera",
            "estuario", "aceituna", "grapadora", "tiroteo", "teatro", "agente", "relojero", "heladero", "alfabeto",
            "electricidad", "permutar", "pareidolia", "supercomputadora", "paranormal", "montaña rusa",
            "transbordador espacial", "seguridad social", "raqueta eléctrica")


class Difficulty(Enum):
    EASY = 10
    MEDIUM = 5
    HARD = 3
    VERYHARD = 1


class Language(Enum):
    ENGLISH = en_words
    SPANISH = es_words


# Clears the console on Windows and Linux/Mac.
def __clear_console():
    system("cls") if os_name == "nt" else system("clear")


# Allows the user to select a dificulty based on the amount of mistakes
def __difficulty_selection():
    __clear_console()
    selection = 0
    difficulty = None

    while selection not in [1, 2, 3, 4]:
        __clear_console()
        menu = dedent(f'''
            1. Easy.
            2. Medium.
            3. Hard.
            4. Very hard.

            Select a difficulty: ''').lstrip()

        selection = int(input(menu))

        difficulty = {
            1: Difficulty.EASY,
            2: Difficulty.MEDIUM,
            3: Difficulty.HARD,
            4: Difficulty.VERYHARD,
        }

    return difficulty[selection]


# Lets the user select the language for the word to be guessed
def __language_selection():
    __clear_console()
    selection = 0
    language = 0

    while selection not in [1, 2]:
        __clear_console()
        menu = dedent(f'''
            1. English.
            2. Spanish.

            Select a language: ''').lstrip()

        selection = int(input(menu))

        language = {
            1: Language.ENGLISH,
            2: Language.SPANISH,
        }

    return language[selection]


# Allows the player to pick a random word from the word banks or input one.
# If the user decides to input a word, another player guess it (duh).
def game_mode():
    word_to_guess = ""
    mode = 0
    difficulty = Difficulty.EASY    # default difficulty is easy
    language = Language.SPANISH     # default language is Spanish

    while mode not in [1, 2, 3, 4]:
        __clear_console()
        menu = dedent(f'''
            1. Random Word.
            2. Word given by user.
            3. Choose dificulty. ({difficulty.name})
            4. Change word language. ({language.name})

            Select a game mode: ''').lstrip()

        mode = int(input(menu))

        if mode == 1:
            word_to_guess = choice(language.value)
        elif mode == 2:
            word_to_guess = str(input("Input a word: "))    # won't even check for null inputs
        elif mode == 3:
            difficulty = __difficulty_selection()
            mode = 0    # keeps loop from breaking
            continue
        elif mode == 4:
            language = __language_selection()
            mode = 0
            continue

    return word_to_guess, difficulty


# Game loop
# Supports single words or words separated by spaces, i.e. "space shuttle".
def game(word, difficulty):
    __clear_console()

    guessed_letters = [' ']
    mistakes = 0
    guessed = False

    print(' '.join("_" if i != ' ' else ' ' for i in word))

    while not guessed and mistakes < difficulty.value:
        guess = str(input("Guess a letter: ")).lower()
        __clear_console()

        if guess not in guessed_letters:
            guessed_letters.append(guess)

        # mistakes only increase when a guessed letter is not in the word
        if guess not in word:
            mistakes += 1

        # prints each character if it has already been guessed out of all those in "word"
        print(' '.join([i if i in guessed_letters else '_' for i in word]))
        print('[' + ' '.join(guessed_letters) + "  ]")

        if word == ''.join([i if i in guessed_letters else '_' for i in word]):
            guessed = True

    # waits until the user presses enter
    input("\nYOU GUESSED THE WORD! (press enter to exit)" if guessed else "\nYOU LOST! (press enter to exit)")


# FIXME:
# - store words in a separate file (nah)
def main() -> None:
    try:
        word, difficulty = game_mode()
        game(word, difficulty)

    # these errors are raised when pressing ^Z, ^C or inputting any invalid character.
    except (EOFError, KeyboardInterrupt, ValueError):
        pass

    __clear_console()

# Ignoring errors go brrrrr
if __name__ == '__main__':
    main()
