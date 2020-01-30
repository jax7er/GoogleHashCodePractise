# imports
import os


# class defs
class Ride:
    def __init__(self, id, start_r, start_c, finish_r, finish_c, earliest_start, latest_finish):
        self.id = id
        self.start_r = start_r
        self.start_c = start_c
        self.finish_r = finish_r
        self.finish_c = finish_c
        self.earliest_start = earliest_start
        self.latest_finish = latest_finish

        self.distance = abs(start_r - finish_r) + abs(start_c - finish_c)

    def fun_name(self):
        return self


class Car:
    def __init__(self):
        self.ride = None
        self.next_ready = 0
        self.prev_rides = []

    def is_free(self, step):
        return step >= self.next_ready

    def start_ride(self, ride, step):
        if self.ride is not None:
            self.prev_rides.append(self.ride)
            travel = abs(self.ride.finish_r - ride.start_r) + abs(self.ride.finish_c - ride.start_c)
        else:
            travel = 0

        self.next_ready = step + travel + ride.distance

        self.ride = ride

    def fun_name(self):
        return self


# functions
def read_in(in_file_name):
    print(in_file_name)

    delimiter = " "
    inputs = []

    with open(in_file_name, "r") as read_f:
        for line in read_f:
            elements = line.replace("\n", "").split(delimiter)

            # convert numeric input
            elements = [float(e) if e.count(".") <= 1 or e.replace(".", "").isnumeric() else e for e in elements]
            elements = [int(e) if type(e) is float and e.is_integer() else e for e in elements]

            inputs.append(elements)

    return inputs


def write_out(in_file_name, out_data):
    out_file_name = in_file_name.replace(".in", ".out")

    with open(out_file_name, "w") as write_f:
        for elements in out_data:
            write_f.write(" ".join(str(e) for e in elements) + "\n")


def get_weight(car, ride):
    if car.ride is not None:
        travel = abs(car.ride.finish_r - ride.start_r) + abs(car.ride.finish_c - ride.start_c)
    else:
        travel = 0

    return ride.distance - travel + (start_bonus if ride.earliest_start <= step + travel else 0)


# main script
in_file_names = [s for s in os.listdir(".") if s.endswith(".in")]

total_score = 0

for in_file_name in in_file_names:
    in_data = read_in(in_file_name)

    header = in_data.pop(0)

    print(*header)

    num_rows, num_cols, num_cars, num_rides, start_bonus, num_steps = header

    cars = [Car() for _ in range(num_cars)]
    rides = []

    for id, elements in enumerate(in_data):
        rides.append(Ride(id, *elements))

    # process data...
    for step in range(num_steps):
        for car in cars:
            if car.is_free(step):
                best_ride = None
                best_weight = 0

                for ride in rides:
                    weight = get_weight(car, ride)

                    if best_ride is None or weight > best_weight:
                        best_ride = ride
                        best_weight = weight

                if best_ride is not None:
                    car.start_ride(best_ride, step)

                    del rides[rides.index(best_ride)]

    out_data = []

    for car in cars:
        out_data.append([len(car.prev_rides) + 1, *[x.id for x in car.prev_rides], car.ride.id])

    write_out(in_file_name, out_data)

    score = 0

    total_score += score

print(f"total score: {total_score}")
