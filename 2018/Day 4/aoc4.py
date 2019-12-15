from pathlib import Path
import numpy as np
import re
from datetime import datetime
from datetime import timedelta
def main():
    data_folder = Path(".").resolve()
    find_coords = re.compile(r"\[(.*)\] (.*)")
    data = data_folder.joinpath("input.txt").read_text()
    messages =[[datetime.strptime(message[0],'%Y-%m-%d %H:%M'), message[1]] for message in find_coords.findall(data)]
    messages.sort(key= lambda x: x[0])
    
    guards = dict()
    start_shift = re.compile(r"Guard #(\d+) begins shift")
    sleep = re.compile(r"falls asleep")
    wakes = re.compile(r"wakes up")
    for message in messages:
        new_shift = start_shift.match(message[1])
        if message[0].hour == 23:
                date = message[0].date()+timedelta(days=1)
                minute = 0
        else:
                date = message[0].date()
                minute = message[0].minute

        if new_shift:
            guard_id = new_shift.groups()[0]
            if guard_id not in guards:
                guards[guard_id] = dict()
            
            guards[guard_id][date] = np.zeros(60,dtype=int)
        elif sleep.match(message[1]):
            guards[guard_id][date][minute:] = 1
        elif wakes.match(message[1]):
            guards[guard_id][date][minute:] = 0
        else:
            print(message)
            raise RuntimeError('Unknown message')
    
    sleepiest_guard_one = None
    most_minutes_asleep = 0
    freq_minute = 0
    sleepiest_guard_two = None
    for guard_id in guards:
        sleep_grid = np.zeros((0,60),dtype=int)
        for shift in guards[guard_id]:
            sleep_grid = np.concatenate([sleep_grid,guards[guard_id][shift].reshape((-1,60))],axis=0)

        minutes_slept = 0
        for shifts in guards[guard_id]:
            minutes_slept += np.sum(guards[guard_id][shifts])
    
        print(f"Guard #{guard_id} minutes slept: {minutes_slept}")
        print("0"*10+"1"*10+"2"*10+"3"*10+"4"*10+"5"*10)
        print("0123456789"*6)
        print("\n".join(
                [
                    "".join([str(d) for d in row])
                    .replace("0", ".")
                    .replace("1", "#")
                    for row in sleep_grid
                ]
            )
        )
        sleep_per_minute = np.sum(sleep_grid,axis=0)
        print("".join([str(d)[-1] for d in sleep_per_minute]))
        print("".join([str(d)[0] if d > 9 else " " for d in sleep_per_minute]))
        
        print()

        if minutes_slept > most_minutes_asleep:
            sleepiest_guard_one = guard_id
            most_minutes_asleep = minutes_slept
            sleepiest_minute_one = np.argmax(sleep_per_minute)
        
        if max(sleep_per_minute) > freq_minute:
            freq_minute = max(sleep_per_minute)
            sleepiest_guard_two = guard_id
            sleepiest_minute_two = np.argmax(sleep_per_minute)


    print(f"The sleepiest guard is #{sleepiest_guard_one} with {most_minutes_asleep} minutes slept")
    print(f"He slept the most in minute {sleepiest_minute_one}")
    print(f"Thus the answer to Part 1 is {int(sleepiest_guard_one)*sleepiest_minute_one}")
    print()
    print(f"The guard who is most asleep on the same minute is #{sleepiest_guard_two}")
    print(f"He was asleep {freq_minute} times in minute {sleepiest_minute_two}")
    print(f"Thus the answer to Part 2 is {int(sleepiest_guard_two)*sleepiest_minute_two}")
    

if __name__ == "__main__":
    main()