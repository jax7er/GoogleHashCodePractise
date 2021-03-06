# imports
import os


# superclass for all others to inherit from
class SuperClass:
    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__ + ": " + ", ".join(f"{k}:{type(v).__name__}={v}" for k, v in vars(self).items())

    def weight(self):
        return float("-inf")


# class defs
class Class(SuperClass):
    def __init__(self):
        super().__init__()


# functions
def read_in(in_file_name):
    delimiter = " "
    inputs = []

    with open(in_file_name, "r") as read_f:
        for line in read_f:
            elements = line.replace("\n", "").split(delimiter)

            # convert numeric input
            elements = [float(e) if e.count(".") <= 1 and e.replace(".", "").replace("-", "").isnumeric() else e for e in elements]
            elements = [int(e) if type(e) is float and e.is_integer() else e for e in elements]

            print(", ".join(f"{type(e).__name__}={e}" for e in elements))

            if len(elements) > 1:
                inputs.append(elements)
            else:
                inputs.append(elements[0])

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
    print(in_file_name)

    in_data = read_in(in_file_name)

    def pop():
        return in_data.pop(0)

    header = pop()

    if type(header) is list:
        print("header:", ", ".join(f"{type(e).__name__}={e}" for e in header))
    else:
        print("header:", f"{type(header).__name__}={header}")

    LIST_OF_VARIABLES = header

    sorted_objects = []

    for elements in in_data:
        sorted_objects.append(Class(*elements))

    # sort objects by their weight in descending order
    sorted_objects.sort(key=lambda x: x.weight(), reverse=True)

    out_data = []

    # process data...

    write_out(in_file_name, out_data)

    score = 0

    total_score += score

print(f"total score: {total_score}")
