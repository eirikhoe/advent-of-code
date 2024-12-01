from pathlib import Path
import math


def sim_battle(boss, player):
    boss_hp = boss["HP"]
    player_hp = player["HP"]
    boss_damage = max(1, player["Damage"] - boss["Armor"])
    player_damage = max(1, boss["Damage"] - player["Armor"])

    boss_life = math.ceil(boss_hp / boss_damage)
    player_life = math.ceil(player_hp / player_damage)

    if player_life >= boss_life:
        player_hp -= (boss_life - 1) * player_damage
        return (True, player_hp)
    else:
        boss_hp -= player_life * boss_damage
        return (False, boss_hp)


def optimize_equpment(equipment, boss, player, win_goal=True):
    stats = ["Cost", "Damage", "Armor"]
    weapons = equipment["Weapons"]
    armor = equipment["Armor"]
    rings = equipment["Rings"]

    compare = dict()
    compare[True] = lambda x, y: x < y
    compare[False] = lambda x, y: x > y

    armor["Nothing"] = dict(zip(stats, [0] * len(stats)))
    rings["Nothing"] = dict(zip(stats, [0] * len(stats)))

    ring_names = list(rings.keys())
    n_rings = len(ring_names)
    optimal_cost = None
    for w_name in weapons:
        w = weapons[w_name]
        for a_name in armor:
            a = armor[a_name]
            for i in range(n_rings):
                r_name_1 = ring_names[i]
                r1 = rings[r_name_1]
                for j in range(i, n_rings):
                    r_name_2 = ring_names[j]
                    r2 = rings[r_name_2]
                    if (i == j) and (r_name_1 != "Nothing"):
                        continue
                    cost = w["Cost"] + a["Cost"] + r1["Cost"] + r2["Cost"]
                    player["Damage"] = (
                        w["Damage"] + a["Damage"] + r1["Damage"] + r2["Damage"]
                    )
                    player["Armor"] = (
                        w["Armor"] + a["Armor"] + r1["Armor"] + r2["Armor"]
                    )
                    won = sim_battle(boss, player)[0]
                    if won != win_goal:
                        continue
                    if (optimal_cost is None) or compare[win_goal](cost, optimal_cost):
                        optimal_cost = cost
    return optimal_cost


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    data = data.split("\n")
    table = []
    for row in data:
        if row:
            r = row.split()
            table.append(r[-4:])
            table[-1][0] = " ".join(r[:-3])
            for i in range(1, len(table[-1])):
                try:
                    table[-1][i] = int(table[-1][i])
                except ValueError:
                    pass
    equipment = dict()
    for row in table:
        if isinstance(row[1], str):
            cat_name = row[0][:-1]
            stats = row[1:]
            equipment[cat_name] = dict()
        else:
            equipment[cat_name][row[0]] = dict(zip(stats, row[1:]))

    boss = {"HP": 103, "Damage": 9, "Armor": 2}
    player = {"HP": 100, "Damage": 0, "Armor": 0}

    print("Part 1")
    min_win_cost = optimize_equpment(equipment, boss, player, True)
    print(
        "The least amount of gold you can spend and still win the "
        + f"fight is {min_win_cost}"
    )
    print()

    print("Part 2")
    max_lose_cost = optimize_equpment(equipment, boss, player, False)
    print(
        "The most amount of gold you can spend and still lose the "
        + f"fight is {max_lose_cost}"
    )


if __name__ == "__main__":
    main()
