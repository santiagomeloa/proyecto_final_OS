import subprocess

print("Ejecutando prueba base de FFmpeg")

cmd = [
    'perf', 'stat',
    'ffmpeg', '-i', '1406-147169807_small.mp4',
    '-c:v', 'libx264',
    '-preset', 'slow',
    '-threads', '4',
    'output_base.mp4'
]

subprocess.run(cmd)
