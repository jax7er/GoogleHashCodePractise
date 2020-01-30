class DataCenter:
    def __init__(self, videos):
        self.videos = videos


class Cache:
    def __init__(self, size):
        self.size = size
        self.videos = {}

    def free_space(self):
        return self.size - sum(v for _, v in self.videos.items())


class Endpoint:
    def __init__(self, requests, latencies):
        self.requests = requests
        self.latencies = latencies
        self.best_latencies = {}


def load_caches(endpoints, caches, datacenter):
    e_c_v_scores = []

    for e_id, e in enumerate(endpoints):
        for c_id, c in enumerate(caches):
            if c_id in e.latencies:
                for v_id, count in e.requests.items():
                    score = count * (e.latencies[-1] - e.latencies[c_id])
                    e_c_v_scores.append((e_id, c_id, v_id, score))

    # sort scores in descending order
    e_c_v_scores.sort(key=lambda x: x[-1], reverse=True)

    for e_id, c_id, v_id, score in e_c_v_scores:
        v_size = datacenter.videos[v_id]

        if v_size <= caches[c_id].free_space():
            caches[c_id].videos[v_id] = v_size


def calculate_best_sources(endpoint, caches):
    endpoint.best_latencies = {}

    for v_id, count in endpoint.requests.items():
        best_latency = endpoint.latencies[-1]
        source_id = -1

        for cache_i, cache in enumerate(caches):
            if cache_i in endpoint.latencies:
                if v_id in cache.videos and endpoint.latencies[cache_i] < best_latency:
                    best_latency = endpoint.latencies[cache_i]
                    source_id = cache_i

        endpoint.best_latencies[v_id] = source_id


def calculate_total_latency(endpoint):
    return sum(endpoint.requests[v_id] * endpoint.latencies[source_id]
               for v_id, source_id in endpoint.best_latencies.items())


total_score = 0

for file_name in ["kittens.in.txt", "me_at_the_zoo.in", "trending_today.in", "videos_worth_spreading.in"]:
    with open("me_at_the_zoo.in") as f:
        nvideos, nendpoints, nrequests, ncaches, csize = [int(n) for n in f.readline().split(" ")]
        vsizes = [int(n) for n in f.readline().split(" ")]

        endpoint_latencies = []
        endpoint_requests = [{} for i in range(nendpoints)]

        for endpoint in range(nendpoints):
            dclatency, caches = [int(n) for n in f.readline().split(" ")]

            data = {-1: dclatency}

            for n in range(caches):
                id, latency = [int(n) for n in f.readline().split(" ")]
                data[id] = latency

            endpoint_latencies.append(data)

        for request in range(nrequests):
            vid, eid, numreqs = [int(n) for n in f.readline().split(" ")]
            endpoint_requests[eid][vid] = numreqs


    dc = DataCenter(vsizes)
    caches = [Cache(csize)] * ncaches
    endpoints = [Endpoint(endpoint_requests[i], endpoint_latencies[i]) for i in range(nendpoints)]

    for cache in caches:
        for endpoint in endpoints:
            calculate_best_sources(endpoint, caches)

    total_requests = 0
    for endpoint in endpoints:
        total_requests += sum(v for _, v in endpoint.requests.items())

    total_latency = 0
    for endpoint in endpoints:
        total_latency += calculate_total_latency(endpoint)

    score = 1000 * total_latency / total_requests

    total_score += score

total_score = int(total_score)

print(f"total score: {total_score}")
print(f"{100 * total_score / 2651999:.1f}% of best score of any team (2651999)")
