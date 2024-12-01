from pathlib import Path
from collections import deque
import copy
import math

data_folder = Path(".").resolve()


class Conjuction_module:
    def __init__(self, name, output_modules, input_modules):
        self.remembered = {input_module: 0 for input_module in input_modules}
        self.output_modules = output_modules
        self.name = name

    def process(self, input_module, pulse):
        self.remembered[input_module] = pulse
        pulse_sent = 1 - min([val for _, val in self.remembered.items()])
        outputs = [(self.name, out, pulse_sent) for out in self.output_modules]
        return outputs


class Flipflop_module:
    def __init__(self, name, output_modules):
        self.on = False
        self.output_modules = output_modules
        self.name = name

    def process(self, _, pulse):
        if pulse == 1:
            return []
        self.on = not self.on
        pulse_sent = int(self.on)
        outputs = [(self.name, out, pulse_sent) for out in self.output_modules]
        return outputs


class Broadcast_module:
    def __init__(self, name, output_modules):
        self.output_modules = output_modules
        self.name = name

    def process(self, _, pulse):
        outputs = [(self.name, out, pulse) for out in self.output_modules]
        return outputs


def parse_data(data):
    modules = dict()
    for line in data.split("\n"):
        name, destinations_str = line.split(" -> ")

        if name[0] in ["%", "&"]:
            module_type = name[0]
            name = name[1:]
        else:
            module_type = None
        destinations = destinations_str.split(", ")
        modules[name] = (module_type, destinations, [])
    for name in modules:
        inputs = modules[name][1]
        for input in inputs:
            if input in modules:
                modules[input][2].append(name)
    for name in modules:
        if modules[name][0] is None:
            modules[name] = Broadcast_module(name, modules[name][1])
        elif modules[name][0] == "%":
            modules[name] = Flipflop_module(name, modules[name][1])
        elif modules[name][0] == "&":
            modules[name] = Conjuction_module(name, modules[name][1], modules[name][2])
    return modules


def get_pulse_str(sender, receiver, pulse):
    pulse_type = "high" if bool(pulse) else "low"
    s = f"{sender} -{pulse_type}-> {receiver}"
    return s


def press_button(modules):
    queue = deque([("button", "broadcaster", 0)])
    count = [0, 0]
    gf_high_count = 0
    final_signal_low = False
    while len(queue) > 0:
        sender, receiver, pulse = queue.popleft()
        if receiver == "gf":
            final_signal_low = pulse == 0
            if pulse == 1:
                gf_high_count += 1
        count[pulse] += 1
        if receiver in modules:
            output_pulses = modules[receiver].process(sender, pulse)
            queue.extend(output_pulses)
    return count, (gf_high_count, final_signal_low)


def count_pulses(modules, n_button_presses):
    count = [0, 0]
    for _ in range(n_button_presses):
        additional, _ = press_button(modules)
        count = [count[i] + additional[i] for i in range(2)]
    return count[0] * count[1]


def find_connected(name, modules, called):
    connected = set([name])
    if name in called:
        return set()
    if name not in modules:
        return connected
    called.append(name)
    for out in modules[name].output_modules:
        connected = connected.union(find_connected(out, modules, called))
    return connected


def get_state(modules):
    names = sorted(list(modules.keys()))
    state = []
    for name in names:
        if isinstance(modules[name], Broadcast_module):
            continue
        elif isinstance(modules[name], Flipflop_module):
            state.append(int(modules[name].on))
        elif isinstance(modules[name], Conjuction_module):
            inputs = sorted(list(modules[name].remembered.keys()))
            for input in inputs:
                state.append(modules[name].remembered[input])
    state = tuple(state)
    return state


def run_til_repeat_state(modules):
    seen = dict()
    i = 0
    state = get_state(modules)
    while state not in seen:
        _, gf_state = press_button(modules)
        seen[state] = (i, gf_state)
        i += 1
        state = get_state(modules)
    return seen, i, seen[state][0]


def divide_into_subsets(modules):
    names = modules["broadcaster"].output_modules
    subsets = []
    for name in names:
        subsets.append(find_connected(name, modules, []))
    return subsets


def find_button_presses_to_low_rx_signal(modules):
    # Divide into the four subsets
    subsets = divide_into_subsets(modules)
    cycle_lengths = []
    for i, subset in enumerate(subsets):
        subset_name = modules["broadcaster"].output_modules[i]
        print(f"Subsystem {subset_name}")
        subsystem = dict()
        for name in [*list(subset), "broadcaster"]:
            if name in modules:
                subsystem[name] = copy.deepcopy(modules[name])
            if name == "gf":
                inputs = list(subsystem[name].remembered.keys())
                for input in inputs:
                    if input not in subset:
                        del subsystem[name].remembered[input]
        # Run each subsystem until a repeat state
        seen, i, repeat_state = run_til_repeat_state(subsystem)
        cycle_length = i - repeat_state
        print(
            f"The subsystem returned to state {repeat_state} "
            f"with cycle length {i-repeat_state}."
        )
        for state in seen:
            # Check if gf always receives at least one low signal
            # after a potential high one
            assert seen[state][1][1] is True
            n_high = seen[state][1][0]
            if n_high == 0:
                continue
            # Check that the state before the high signal is produced
            # is -2 % cycle length
            cycle_index = seen[state][0] - repeat_state
            assert (cycle_index - cycle_length) == -2
            # This means the high signal is produced on the button
            # press from state -2 modulo the cycle length
            print(
                f"The subsystem sends {n_high} high signal(s) to gf "
                f"after {seen[state][0]+1} button presses.\n"
                "This is from state -2 modulo the cycle length."
            )
        print()
        cycle_lengths.append(cycle_length)
    return math.lcm(*cycle_lengths)


def check_subset_independence(subsets):
    n = len(subsets)
    for i in range(n - 1):
        for j in range(i + 1, n):
            assert subsets[i].intersection(subsets[j]) == {"gf", "rx"}


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    modules = parse_data(data)

    print("Part 1")
    pulse_product = count_pulses(copy.deepcopy(modules), 1000)
    print(
        "The product of the total number of high and low pulses sent "
        f"is {pulse_product}."
    )
    print()

    print("Part 2")
    # From analysis of the input you realize that the output_modules of
    # broadcaster make up four independent subsystems that all connect to the
    # conjugation module gf which determines the signal to rx.
    # Thus the low signal requires all the four subsystems to send a high
    # signal to gf
    subsets = divide_into_subsets(modules)
    check_subset_independence(subsets)

    # More analysis shows that for all four subsystems:
    # - The state eventually returns to the state after the first button press
    # - The only high signal happens on button press from state -2 modulo this
    #   cycle length
    # - At least one final low signal is sent to gf on every button press.
    #
    # Thus the first low signal to rx must happen on the button press from state -2
    # modulo all four cycle lengths, i.e. the lowest common multiple of all cycle
    # lengths - 2. However we need to include the initial button press to get to
    # the cycle, and the final button press to generate the signal, so the answer
    # is the lowest common multiple of the cycle lengths.
    n_button_presses = find_button_presses_to_low_rx_signal(modules)
    print(
        f"You must press the button {n_button_presses} times to send a "
        "single low signal to the module rx for the first time."
    )


if __name__ == "__main__":
    main()
