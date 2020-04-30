from pathlib import Path
from collections import defaultdict
import re
import numpy as np
data_folder = Path(".").resolve()

reg_bot = re.compile(r"bot (\d+) gives low to ((?:bot|output) \d+) and high to ((?:bot|output) \d+)")
reg_val = re.compile(r"value (\d+) goes to bot (\d+)")


class Bot:
    def __init__(self,low=None,high=None,values=None):
        self.low = low
        self.high = high
        if values is None:
            values = []

        self.values = values
        self.comparisons = []

    def has_compared(self,values):
        for comparison in self.comparisons:
            if (min(values) == min(comparison)) and (max(values) == max(comparison)):
                return True
        return False

class Factory:

    def __init__(self,data):
        self.bots = defaultdict(Bot)
        self.bins = defaultdict(list)

        for line in data.split('\n'):
            m = reg_bot.match(line)
            if m is not None:
                name = m.group(1)
                low = m.group(2)
                high = m.group(3)
                self.bots[name].low = low
                self.bots[name].high = high
            else:
                m = reg_val.match(line)
                if m is not None:
                    name = m.group(2)
                    value = int(m.group(1))
                    self.bots[name].values.append(value)

    def follow_instructions(self):
        has_two_values = True
        while has_two_values:
            has_two_values = False
            for curr_bot_nr in self.bots:
                bot = self.bots[curr_bot_nr]
                if len(bot.values) == 2:
                    bot.comparisons.append(bot.values.copy())
                    has_two_values = True
                    bot.values.sort()
                    if bot.high.startswith("output"):
                        bin_nr = bot.high[7:]
                        self.bins[bin_nr].append(bot.values.pop())
                    elif bot.high.startswith("bot"):
                        bot_nr = bot.high[4:]
                        self.bots[bot_nr].values.append(bot.values.pop())
                    
                    if bot.low.startswith("output"):
                        bin_nr = bot.low[7:]
                        self.bins[bin_nr].append(bot.values.pop())
                    elif bot.low.startswith("bot"):
                        bot_nr = bot.low[4:]
                        self.bots[bot_nr].values.append(bot.values.pop())
    
    def find_comparison_bot(self,values):
        for bot_nr in self.bots:
            if self.bots[bot_nr].has_compared(values):
                return bot_nr
        return None


def main():
    data = data_folder.joinpath("input.txt").read_text()
    f = Factory(data)
    f.follow_instructions()
    first_chip = 17
    second_chip = 61
    bot_nr = f.find_comparison_bot([first_chip,second_chip])

    for bin_nr in f.bins:
        print(bin_nr,f.bins[bin_nr])

    print("Part 1")
    print(f"Bot number {bot_nr} is responsible for comparing value-{first_chip} and value-{second_chip} microchips")
    print()

    print("Part 2")
    product = 1
    for bin_nr in ["0","1","2"]:
        product *= f.bins[bin_nr][0]
    print(f"If you multiply together the values of one chip in each of outputs 0, 1, and 2 you get {product}")

if __name__ == "__main__":
    main()
