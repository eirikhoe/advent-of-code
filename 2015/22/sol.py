from collections import deque
from copy import deepcopy


class State:
    def __init__(
        self,
        boss_hp,
        boss_damage,
        hp,
        mana,
        armor=0,
        poison_timer=0,
        shield_timer=0,
        recharge_timer=0,
    ):
        self.boss_hp = boss_hp
        self.hp = hp
        self.armor = armor
        self.mana = mana
        self.timer = {
            "Poison": poison_timer,
            "Shield": shield_timer,
            "Recharge": recharge_timer,
        }
        self.lose = False
        self.win = False
        self.boss_damage = boss_damage
        self.mana_used = 0

    damage = {
        "Magic Missile": 4,
        "Drain": 2,
        "Poison": 3,
    }

    drain_heal = 2
    recharge_mana = 101
    shield_armor = 7

    duration = {"Shield": 6, "Poison": 6, "Recharge": 5}

    cost = {
        "Magic Missile": 53,
        "Drain": 73,
        "Shield": 113,
        "Poison": 173,
        "Recharge": 229,
    }

    def magic_missile(self):
        self.boss_hp -= State.damage["Magic Missile"]

    def drain(self):
        self.boss_hp -= State.damage["Drain"]
        self.hp += State.drain_heal

    def shield(self):
        self.armor += State.shield_armor
        self.timer["Shield"] = State.duration["Shield"]

    def shield_eff(self):
        if self.timer["Shield"] <= 1:
            self.armor -= State.shield_armor

    def poison(self):
        self.timer["Poison"] = State.duration["Poison"]

    def poison_eff(self):
        self.boss_hp -= State.damage["Poison"]

    def recharge(self):
        self.timer["Recharge"] = State.duration["Recharge"]

    def recharge_eff(self):
        self.mana += State.recharge_mana

    effect = {
        "Shield": shield_eff,
        "Poison": poison_eff,
        "Recharge": recharge_eff,
    }
    attack = {
        "Magic Missile": magic_missile,
        "Drain": drain,
        "Shield": shield,
        "Poison": poison,
        "Recharge": recharge,
    }

    def resolve_effects(self):
        for s in self.timer:
            if self.timer[s] > 0:
                State.effect[s](self)
                self.timer[s] -= 1

    def do_turn(self, spell, hard=False):
        if hard:
            self.hp -= 1

            if self.hp <= 0:
                self.lose = True
                return

        self.resolve_effects()

        if self.boss_hp <= 0:
            self.win = True
            return

        if self.mana < State.cost[spell]:
            self.lose = True
            return

        if (spell in self.timer) and (self.timer[spell] > 0):
            self.lose = True
            return
        else:
            State.attack[spell](self)
            self.mana -= State.cost[spell]
            self.mana_used += State.cost[spell]

        if self.boss_hp <= 0:
            self.win = True
            return

        self.resolve_effects()

        if self.boss_hp <= 0:
            self.win = True
            return

        self.hp -= max(self.boss_damage - self.armor, 1)

        if self.hp <= 0:
            self.lose = True

    def display(self):
        print(f"HP - {self.hp}")
        print(f"Armor - {self.armor}")
        print(f"Mana - {self.mana}")
        print(f"Mana used - {self.mana_used}")
        print(f"Boss HP - {self.boss_hp}")
        for timer in self.timer:
            print(f"{timer} timer - {self.timer[timer]}")
        if self.win:
            print("The player won!")
        if self.lose:
            print("The player lost!")
        print()
        return


def find_lowest_mana(initial_state, hard=False):
    actions = ["Magic Missile", "Drain", "Shield", "Poison", "Recharge"]
    states = deque([initial_state])
    lowest_used_mana = None
    while len(states) > 0:
        state = states.pop()
        for action in actions:
            new_state = deepcopy(state)
            new_state.do_turn(action, hard)
            if new_state.win:
                if (lowest_used_mana is None) or (
                    new_state.mana_used < lowest_used_mana
                ):
                    lowest_used_mana = new_state.mana_used
            elif new_state.lose:
                pass
            elif (lowest_used_mana is None) or (new_state.mana_used < lowest_used_mana):
                states.appendleft(new_state)
    return lowest_used_mana


def main():
    state = State(58, 9, 50, 500)

    print("Part 1")
    lowest_used_mana = find_lowest_mana(state)
    print(
        "The least amount of mana you can spend and still win the "
        + f"fight on normal is {lowest_used_mana}"
    )
    print()

    print("Part 2")
    lowest_used_mana = find_lowest_mana(state, True)
    print(
        "The least amount of mana you can spend and still win the "
        + f"fight on hard is {lowest_used_mana}"
    )


if __name__ == "__main__":
    main()
