# imports
import os


# class defs
class REFACTOR_class:
    def __init__(self):
        pass

    def weight(self):
        return self

    def fun_name(self):
        return self


# functions
def read_in(in_file_name):
    delimiter = " "
    inputs = []

    with open(in_file_name, "r") as read_f:
        for line in read_f:
            elements = line.replace("\n", "").split(delimiter)

            # convert numeric input
            elements = [float(e) if e.count(".") <= 1 and e.replace(".", "").isnumeric() else e for e in elements]
            elements = [int(e) if type(e) is float and e.is_integer() else e for e in elements]

            for e in elements:
                print(type(e), e)

            inputs.append(elements)

    return inputs


def write_out(in_file_name, out_data):
    out_file_name = in_file_name.replace(".in", ".out")

    with open(out_file_name, "w") as write_f:
        for elements in out_data:
            write_f.write(" ".join(str(e) for e in elements) + "\n")


# main script
in_file_names = [s for s in os.listdir(".") if s.endswith(".in")]

total_score = 0

for in_file_name in in_file_names:
    in_data = read_in(in_file_name)

    header = in_data.pop(0)

    print(*header)

    LIST_OF_VARIABLES = header

    REFACTOR_objects = []

    REFEACTOR_sorted_objects = []

    for elements in in_data:
        REFEACTOR_sorted_objects.append(REFACTOR_class(*elements))

    # sort objects by their weight in descending order
    REFEACTOR_sorted_objects.sort(key=lambda x: x.weight(), reverse=True)

    out_data = []

    # process data...

    write_out(in_file_name, out_data)

    score = 0

    total_score += score

print(f"total score: {total_score}")
