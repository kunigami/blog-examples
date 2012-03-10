import subprocess
import os

# Arquivo com solucoes p/ uncapacited facility location
optFile = open('instances/uncapopt.txt', 'r')

lines = optFile.readlines()

results = "\\begin{table}\n"
results += "\\begin{tabular}{l | c | c | c | c | c}\n"
results += "Instance & \\# Facilities & \\# Clients & Gap (\\%) & Gap DP (\\%) & Time (s)\\\\\n"
results += "\\hline\n"

for f in lines:
    instance, optimal = f.split()
    optimal = float(optimal)

    filename = os.path.join('instances/', instance + '.txt')

    # Executa o algoritmo
    cmd = 'src/./facility_location ' + filename
    print 'executando: ', cmd
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output = proc.communicate()
    nFacilities, nClients, value, dual, time = output[0].split()

    value = float(value)
    dual = float(dual)
    time = float(time)

    gap = ((value-optimal)/optimal + 1e-8) * 100.0
    # Gap dual-primal
    gapDP = (value - dual)/value * 100.0
        
    print 'gap: {0:.2f}%'.format(gap)

    results += ('{} & {:3} & {:3} & {:.1f} & {:.1f} & {:.2f}\\\\\n'.format(instance, nFacilities, nClients, gap, gapDP, time))

fin = open('doc/template.tex', 'r')
fout = open('doc/results.tex', 'w')

results += "\\end{tabular}\n"
results += "\\end{table}\n"

for l in fin.readlines():
    if l.strip() == '%python:table':
        fout.write(results)
    else:
        fout.write(l)

fin.close()
fout.close()
