import random
import json
import os
import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, Completer, Completion
from colorama import Fore

rolls = {}


def main():
    print(Fore.WHITE)
    log("App starting up...")
    load_rolls()
    show_header()
    show_leaderboard()
    player1, player2 = get_players()
    log(f"{player1} has logged in.")
    play_game(player1, player2)
    log("Game Over.")


def show_header():
    print(Fore.MAGENTA)
    print("-------------------------")
    print("Rock Paper Scissors v1")
    print("-------------------------")
    print(Fore.WHITE)


def show_leaderboard():
    leaders = load_leaders()

    sorted_names = list(leaders.items())
    sorted_names.sort(key=lambda l: l[1], reverse=True)

    print()
    print("LEADERS: ")
    for name, wins in sorted_names[0:5]:
        print(f"{wins:,}  ----  {name}")
    print("-------------------------")
    print()


def get_players():
    p1 = input("Player 1, what is your name? ")
    p2 = "Computer"
    return p1, p2


def play_game(player_1, player_2):
    log(f"New game starting between {player_1} and {player_2}.")
    wins = {
        player_1: 0,
        player_2: 0
    }

    roll_names = list(rolls.keys())

    while not find_winner(wins, wins.keys()):
        roll1 = get_roll(player_1, roll_names)
        roll2 = random.choice(roll_names)

        if not roll1:
            print(Fore.LIGHTRED_EX + "Can't play that. Try again")
            print(Fore.WHITE)
            continue

        log(f"Round: {player_1} rolled {roll1} and {player_2} rolls {roll2}")
        print(Fore.YELLOW + f"{player_1} rolled {roll1}")
        print(Fore.LIGHTBLUE_EX + f"{player_2} rolls {roll2}")
        print(Fore.WHITE)

        winner = check_for_winning_throw(player_1, player_2, roll1, roll2)

        if winner is None:
            msg = "This round was a tie"
            print(msg)
            print()
            log(msg)

        else:
            msg = f"This round's winner was {winner}"
            fore = Fore.GREEN if winner == player_1 else Fore.LIGHTRED_EX
            print(fore + msg+Fore.WHITE)
            print()
            log(msg)
            wins[winner] += 1

            msg = f"Score is {player_1}: {wins[player_1]} and {player_2}: {wins[player_2]}"
            print(msg)
            print()
            log(msg)
    overall_winner = find_winner(wins, wins.keys())
    fore = Fore.GREEN if overall_winner == player_1 else Fore.LIGHTRED_EX
    msg = f"{overall_winner} wins the game!!"
    print()
    print(fore +msg + Fore.WHITE)
    print()
    log(msg)
    record_win(overall_winner)


def game_winner(player_1, player_2, rounds, wins_p1):
    overall_winner = None
    # if wins_p1 >= rounds:
    #     overall_winner = player_1
    # else:
    #     overall_winner = player_2
    #

    print(f"{overall_winner} wins the game")
    print()


def get_roll(player_name, roll_names):
    print(f"Available rolls: {', '.join(roll_names)}")
    # for index, r in enumerate(roll_names, start=1):
    #     print(f"{index}. {r}")

    word_comp = PlayComplete()
    roll = prompt(f"{player_name}, what is your roll: ", completer=word_comp)

    # text = input(f"{player_name}, what number will you roll? ")
    # selected_index = int(text) - 1

    if not roll or roll not in roll_names:
        print(f"Sorry {player_name}, {roll} is not a valid play!")
        print()
        return None

    return roll

# def get_roll(player_name, roll_names):
#     print("Available rolls:")
#     for index, r in enumerate(roll_names, start=1):
#         print(f"{index}. {r}")
#
#     text = input(f"{player_name}, what number will you roll? ")
#     selected_index = int(text) - 1
#
#     if selected_index < 0 or selected_index >= len(roll_names):
#         print(f"Sorry {player_name}, {text} is not a valid play!")
#         print()
#         return None
#
#     return roll_names[selected_index]


def check_for_winning_throw(player_1, player_2, roll1, roll2):
    winner = None
    if roll1 == roll2:
        print("The play was a tie")

    outcome = rolls.get(roll1, {})
    if roll2 in outcome.get('defeats'):
        return player_1
    elif roll2 in outcome.get('defeated_by'):
        return player_2
    return winner


def find_winner(wins, names):
    best_of = 3
    for name in names:
        if wins.get(name, 0) >= best_of:
            return name

    return None


def load_rolls():
    global rolls

    folder = os.path.dirname(__file__)
    file = os.path.join(folder, 'rolls.json')

    # fin = open(filename, 'r', encoding='utf-8')
    #  rolls = json.load(fin)
    # fin.close()

    with open(file, 'r', encoding='utf-8') as fin:
        rolls = json.load(fin)

    log(f"Loaded rolls: {list(rolls.keys())} from {os.path.basename(file)}")


def load_leaders():
    folder = os.path.dirname(__file__)
    file = os.path.join(folder, 'leaderboard.json')

    if not os.path.exists(file):
        return {}

    with open(file, 'r', encoding='utf-8') as fin:
        return json.load(fin)


def record_win(winner_name):
    leaders = load_leaders()

    if winner_name in leaders:
        leaders[winner_name] += 1
    else:
        leaders[winner_name] = 1

    folder = os.path.dirname(__file__)
    file = os.path.join(folder, 'leaderboard.json')

    with open(file, 'w', encoding='utf-8') as fout:
        json.dump(leaders, fout)


def log(msg):
    folder = os.path.dirname(__file__)
    file = os.path.join(folder, 'rps.log')

    with open(file, "a", encoding="utf-8") as fout:
        fout.write(f"[{datetime.datetime.now().strftime('%c')}] ")
        fout.write(msg)
        fout.write("\n")


class PlayComplete(Completer):

    def get_completions(self, document, complete_event) :
        roll_names = list(rolls.keys())
        word = document.get_word_before_cursor()
        complete_all = not word if not word.strip() else word == "."
        completions = []

        for roll in roll_names:
            if complete_all or word in roll:
                completions.append(
                    Completion(roll,
                               start_position=-len(word),
                               style="fg:white bg:darkgreen",
                               selected_style="fg:yellow bg:green"
                               ))

        return completions

if __name__ == '__main__':
    main()
