import subprocess
import time

print("Aplicando configuraciones del sistema...")

# Desactivar restricciones para perf
subprocess.run("echo 0 | sudo tee /proc/sys/kernel/perf_event_paranoid", shell=True)

# Activar HugePages
subprocess.run("sudo sysctl -w vm.nr_hugepages=1024", shell=True)
subprocess.run("echo always | sudo tee /sys/kernel/mm/transparent_hugepage/enabled", shell=True)

# Comando base FFmpeg
cmd = [
    'perf', 'stat',
    'ffmpeg', '-i', '1406-147169807_small.mp4',
    '-c:v', 'libx264',
    '-preset', 'slow',
    '-threads', '4',
    'output_opt2.mp4'
]

print("Ejecutando FFmpeg con optimización (sin SCHED_BATCH)...")

# Inicia el proceso
proceso = subprocess.Popen(cmd)
pid = proceso.pid

# Esperar brevemente
time.sleep(1)

# Aplicar prioridad con nice
subprocess.run(f"sudo renice -20 -p {pid}", shell=True)

# Esperar que finalice
proceso.wait()
