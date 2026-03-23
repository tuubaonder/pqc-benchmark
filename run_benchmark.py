import subprocess, time, statistics, sys, re

ossl = sys.argv[1]
alg = sys.argv[2]
port = sys.argv[3]
results_file = sys.argv[4]
group = sys.argv[5] if len(sys.argv) > 5 else alg

result = subprocess.run(
    [ossl, "s_time", "-connect", f"127.0.0.1:{port}",
     "-new", "-time", "30"],
    capture_output=True,
    text=True,
    timeout=60
)

output = result.stdout + result.stderr
print(output)

# Parse: "XX connections in 30.00s; XX.XX connections/user sec"
match = re.search(r'(\d+) connections in ([\d.]+)s', output)
if match:
    connections = int(match.group(1))
    seconds = float(match.group(2))
    mean = (seconds / connections) * 1000
    std = 0.0
    print(f"{alg}: {mean:.3f} ms ({connections} connections)")
    with open(results_file, "a") as f:
        f.write(f"{alg},{mean:.3f},{std:.3f}\n")
else:
    print(f"ERROR: Could not parse output for {alg}")
    print(output)
