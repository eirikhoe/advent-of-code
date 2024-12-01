from pathlib import Path
from collections import deque
from copy import deepcopy


def get_decks(data):
    lines = data.split("\n")
    i = 0
    decks = {}
    while i < len(lines):
        player_id = int(lines[i][-2])
        decks[player_id] = deque()
        i += 1
        while i < len(lines) and lines[i]:
            decks[player_id].append(int(lines[i]))
            i += 1
        i += 1
    return decks


def _get_deck_size(decks):
    n_cards = [0, 0]
    for player_id in decks:
        n_cards[player_id - 1] = len(decks[player_id])
    return n_cards


def _make_game_id(decks):
    return tuple(list(decks[1]) + [-1] + list(decks[2]))


def play(decks, recursive=False):
    played = set()
    winner = 1
    cards = [0, 0]
    n_cards = _get_deck_size(decks)
    game_id = _make_game_id(decks)
    while min(n_cards) > 0:
        played.add(game_id)

        for player_id in decks:
            cards[player_id - 1] = decks[player_id].popleft()

        if (not recursive) or (cards[0] >= n_cards[0]) or (cards[1] >= n_cards[1]):
            if cards[0] > cards[1]:
                winner = 1
            else:
                winner = 2
        else:
            rec_decks = dict()
            for player_id in decks:
                rec_deck = deepcopy(list(decks[player_id]))
                rec_decks[player_id] = deque(rec_deck[: cards[player_id - 1]])

            winner, _ = play(rec_decks, True)

        cards = [cards[winner - 1], cards[winner % 2]]
        decks[winner].extend(cards)
        n_cards = _get_deck_size(decks)

        game_id = _make_game_id(decks)
        if game_id in played:
            winner = 1
            break

    return winner, decks


def get_score(decks, winner):
    score = 0
    n_cards = len(decks[winner])
    mult = n_cards
    for card in decks[winner]:
        score += card * mult
        mult -= 1
    return score


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()
    decks = get_decks(data)

    for i, rec in enumerate([False, True]):
        winner, final_decks = play(deepcopy(decks), rec)
        score = get_score(final_decks, winner)

        print(f"Problem {i+1}")
        print(f"In the game of {'Recursive ' if rec else ''}Combat ")
        print(f"the winning player's score was {score}")
        if i == 0:
            print()


if __name__ == "__main__":
    main()
