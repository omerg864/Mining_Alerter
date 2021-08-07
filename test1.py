import os, sys, select, subprocess

args = ['cmd.exe', '-c', 'while true; do date; sleep 2; done']
p1 = subprocess.Popen(args, stdout=subprocess.PIPE, universal_newlines=True)
p2 = subprocess.Popen(args, stdout=subprocess.PIPE, universal_newlines=True)

while True:
    rlist, wlist, xlist = select.select([p1.stdout, p2.stdout], [], [])
    for stdout in rlist:
        sys.stdout.write(os.read(stdout.fileno(), 1024))