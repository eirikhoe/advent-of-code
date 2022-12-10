from pathlib import Path

data_folder = Path(".").resolve()


class Device:
    def __init__(self, data):
        data = data.strip().split("\n")
        regs = ["X"]
        self.reg = dict(zip(regs, [1] * len(regs)))
        self.instrs = []
        for line in data:
            line = line.split(" ")
            for j, val in enumerate(line):
                try:
                    line[j] = int(val)
                except:
                    pass
            self.instrs.append(line)
        self.screen_height = 6
        self.screen_width = 40

    def noop(self, _):
        pass

    def addx(self, instr):
        self.reg["X"] += instr[0]
        pass

    operations = {
        "noop": noop,
        "addx": addx,
    }
    operation_cycle = {
        "noop": 1,
        "addx": 2,
    }

    def operate(self, op_name, instr):
        op = Device.operations[op_name]
        op(self, instr)

    def _inc_cycle(self, cycle, value, interesting_cycle):
        cycle += 1
        if cycle in interesting_cycle:
            value += cycle * self.reg["X"]
        return cycle, value

    def is_pixel_on(self, cycle):
        hor_pos = (cycle - 1) % self.screen_width
        return abs(self.reg["X"] - hor_pos) <= 1

    def draw_screen(self):
        cycle = 0
        for reg_name in self.reg:
            self.reg[reg_name] = 1
        n_pixels = self.screen_width * self.screen_height
        screen = ["." for _ in range(n_pixels)]
        for instr in self.instrs:
            op_cycle = self.operation_cycle[instr[0]]
            for _ in range(op_cycle):
                cycle += 1
                screen[cycle - 1] = "#" if self.is_pixel_on(cycle) else "."
            self.operate(instr[0], instr[1:])
        for i in range(self.screen_height):
            print("".join(screen[(i * self.screen_width) : ((i + 1) * self.screen_width)]))

    def find_interesting_signal_strength_sum(self, interesting_cycle):
        for reg_name in self.reg:
            self.reg[reg_name] = 1
        value = 0
        cycle = 0
        for instr in self.instrs:
            op_cycle = self.operation_cycle[instr[0]]
            for _ in range(op_cycle):
                cycle, value = self._inc_cycle(cycle, value, interesting_cycle)
            self.operate(instr[0], instr[1:])

        return value


def main():
    data = data_folder.joinpath("input.txt").read_text()
    device = Device(data)

    print("Part 1")
    sum_signal_strength = device.find_interesting_signal_strength_sum(
        [20 + 40 * i for i in range(6)]
    )
    print(f"The sum of the six interesting signal strengths is {sum_signal_strength}")
    print()

    print("Part 2")
    print("The CRT screen shows the following image\n")
    device.draw_screen()
    print()


if __name__ == "__main__":
    main()
