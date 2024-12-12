from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    reports = [[int(d) for d in line.split()] for line in data.split("\n")]
    return reports


def count_safe_reports(reports, dampen=False):
    count = 0
    for report in reports:
        safe, fail_ind = is_report_safe(report)
        count += safe
        if safe or (not dampen):
            continue
        for j in range(fail_ind + 2):
            new_report = report[:j] + report[j + 1 :]
            safe, _ = is_report_safe(new_report)
            if safe:
                count += 1
                break
    return count


def is_report_safe(report):
    safe = True
    for i, _ in enumerate(report[:-1]):
        jump = report[i + 1] - report[i]
        if i == 0:
            is_increasing = jump > 0
        if is_unsafe(jump, is_increasing):
            safe = False
            break
    return safe, i


def is_unsafe(jump, is_increasing):
    return (jump == 0) or (abs(jump) > 3) or (is_increasing == (jump < 0))


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    reports = parse_data(data)

    print("Part 1")
    n_safe_reports = count_safe_reports(reports)
    print(f"{n_safe_reports} reports are safe.")
    print()

    print("Part 2")
    n_safe_reports = count_safe_reports(reports, dampen=True)
    print(f"{n_safe_reports} reports are safe with the problem dampener active.")
    print()


if __name__ == "__main__":
    main()
