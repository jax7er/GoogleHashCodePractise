# imports
import os


# class defs
class Compiled:
    def __init__(self, name, compile_time, replicate_time, dependencies):
        self.name = name
        self.compile_time = compile_time
        self.replicate_time = replicate_time
        self.dependencies = dependencies

    def weight(self):
        return sum(d.weight() for d in self.dependencies) \
               + self.compile_time / self.replicate_time


class Target:
    def __init__(self, compiled, deadline, goal_points):
        self.compiled = compiled
        self.deadline = deadline
        self.goal_points = goal_points

    def weight(self):
        return self.goal_points * self.deadline \
               * self.compiled.weight()


# functions
def read_in(in_file_name):
    delimiter = " "
    lines = []

    with open(in_file_name, "r") as read_f:
        for line in read_f:
            elements = line.replace("\n", "").split(delimiter)
            lines.append(elements)

    num_files, num_targets, num_servers = [int(x) for x in lines.pop(0)]

    compiled = {}

    while num_files > 0:
        name, compile_time, replicate_time = lines.pop(0)

        dependencies = [compiled[s] for s in lines.pop(0)[1:]]

        compiled[name] = Compiled(name, int(compile_time), int(replicate_time), dependencies)

        num_files -= 1

    targets = {}

    while num_targets > 1:
        name, deadline, goal_points = lines.pop(0)

        targets[name] = Target(compiled[name], int(deadline), int(goal_points))

        num_targets -= 1

    return compiled, targets, num_servers


def write_out(in_file_name, compilations):
    out_file_name = in_file_name.replace(".in", ".out")

    with open(out_file_name, "w") as write_f:
        write_f.write(f"{len(compilations)}\n")

        for c in compilations:
            write_f.write(f"{c[0]} {c[1]}\n")


# main script
in_file_names = [s for s in os.listdir(".") if s.endswith(".in")]

total_score = 0

for in_file_name in in_file_names:
    compiled, targets, num_servers = read_in(in_file_name)

    server_compiling = [False] * num_servers

    targets_sorted = sorted(list(targets.values()), key=lambda t: t.weight(), reverse=True)

    for t in targets_sorted:
        print(t.compiled.name, t.deadline, t.goal_points, t.weight())

    compilations = []

    for s_i in range(num_servers):
        if len(targets_sorted) > 0:
            compilations.append([targets_sorted.pop(0).compiled.name, s_i])

            server_compiling[s_i] = True

    write_out(in_file_name, compilations)

    score = 0

    total_score += score

print(f"total score: {total_score}")
