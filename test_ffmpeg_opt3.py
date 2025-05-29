import subprocess
import time
import os
import shutil

# Ruta de trabajo en RAM
ramdisk_path = "/tmp/ramdisk"
video_name = "1406-147169807_small.mp4"
video_ram = os.path.join(ramdisk_path, video_name)

# Crear directorio si no existe
if not os.path.exists(ramdisk_path):
    print("📁 Creando carpeta /tmp/ramdisk...")
    os.makedirs(ramdisk_path)

# Montar tmpfs en la carpeta
print("⏫ Montando ramdisk...")
subprocess.run(["sudo", "mount", "-t", "tmpfs", "-o", "size=512M", "tmpfs", ramdisk_path])

# Copiar el video al ramdisk
print("📦 Copiando video al ramdisk...")
shutil.copy(video_name, video_ram)

# Ajustar permisos para perf
print("🔧 Ajustando configuración de perf...")
subprocess.run("echo 0 | sudo tee /proc/sys/kernel/perf_event_paranoid", shell=True)

# Activar HugePages
subprocess.run("sudo sysctl -w vm.nr_hugepages=1024", shell=True)
subprocess.run("echo always | sudo tee /sys/kernel/mm/transparent_hugepage/enabled", shell=True)

# Comando optimizado
cmd = [
    'perf', 'stat',
    'taskset', '-c', '2,3,4,5',
    'ionice', '-c2', '-n0',
    'nice', '-n', '-20',
    'ffmpeg', '-i', video_ram,
    '-c:v', 'libx264',
    '-preset', 'slow',
    '-threads', '4',
    'output_advanced.mp4'
]

print("🚀 Ejecutando FFmpeg con optimizaciones avanzadas...\n")
start_time = time.time()
subprocess.run(cmd)
end_time = time.time()
print(f"\n⏱️ Tiempo total medido por Python: {end_time - start_time:.3f} s")

# Limpiar RAM
print("🧹 Limpiando ramdisk...")
subprocess.run(["sudo", "umount", ramdisk_path])
