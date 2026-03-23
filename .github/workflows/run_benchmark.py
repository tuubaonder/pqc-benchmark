import subprocess, time, statistics, sys

ossl = sys.argv[1]
alg = sys.argv[2]
port = sys.argv[3]
results_file = sys.argv[4]
group = sys.argv[5] if len(sys.argv) > 5 else alg
iterations = 1000
times = []

for i in range(iterations):
    start = time.perf_counter()
    subprocess.run(
        [ossl, "s_client", "-connect", f"127.0.0.1:{port}",
         "-groups", group, "-tls1_3", "-brief"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=10
    )
    end = time.perf_counter()
    times.append((end - start) * 1000)

mean = statistics.mean(times)
std = statistics.stdev(times)
print(f"{alg}: {mean:.3f} +/- {std:.3f} ms")
with open(results_file, "a") as f:
    f.write(f"{alg},{mean:.3f},{std:.3f}\n")
