import subprocess, time, statistics, sys, os

ossl = sys.argv[1]
alg = sys.argv[2]
port = sys.argv[3]
results_file = sys.argv[4]
group = sys.argv[5] if len(sys.argv) > 5 else alg
iterations = 1000
times = []

cmd = f"echo '' | {ossl} s_client -connect 127.0.0.1:{port} -groups {group} -tls1_3 2>/dev/null"

for i in range(iterations):
    start = time.perf_counter()
    subprocess.run(cmd, shell=True, timeout=10)
    end = time.perf_counter()
    times.append((end - start) * 1000)

mean = statistics.mean(times)
std = statistics.stdev(times)
print(f"{alg}: {mean:.3f} +/- {std:.3f} ms")
with open(results_file, "a") as f:
    f.write(f"{alg},{mean:.3f},{std:.3f}\n")
