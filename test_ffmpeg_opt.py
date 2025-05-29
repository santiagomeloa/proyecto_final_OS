import subprocess
import os
import time

print("Aplicando configuraciones del sistema...")

# Desactivar restricciones de perf
subprocess.run("echo 0 | sudo tee /proc/sys/kernel/perf_event_paranoid", shell=True)

# Activar HugePages
subprocess.run("sudo sysctl -w vm.nr_hugepages=1024", shell=True)
subprocess.run("echo always | sudo tee /sys/kernel/mm/transparent_hugepage/enabled", shell=True)

# Inicia el proceso con perf
cmd = [
    'perf', 'stat',
    'ffmpeg', '-i', '1406-147169807_small.mp4',
    '-c:v', 'libx264',
    '-preset', 'slow',
    '-threads', '4',
    'output_opt.mp4'
]

print("Ejecutando FFmpeg con optimizaciones")

# Inicia el proceso en segundo plano
proceso = subprocess.Popen(cmd)
pid = proceso.pid

# Espera un momento para asegurarse de que se inicie
time.sleep(1)

# Aplicar prioridades
subprocess.run(f"sudo chrt --batch -p {pid}", shell=True)
subprocess.run(f"sudo renice -20 -p {pid}", shell=True)

# Esperar que termine
proceso.wait()
