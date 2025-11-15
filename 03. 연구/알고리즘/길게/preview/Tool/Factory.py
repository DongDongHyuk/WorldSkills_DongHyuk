from Case import Case
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from release.main_perf2_2 import main      # from 'fileName' import main
from main import main      # from 'fileName' import main
Case.main = main

def factory():
    global case
    while Case.ct < limit:
        case = Case(t)
        res = case.run()
        if not res:
            break
    Case.status()

t = 0
limit = 100

Case.printStyle = " [{}] | {},'{}','{}'" # .format(ct, t, m1, *args)
try:
    print()
    factory()
except KeyboardInterrupt:
    Case.failCase = case
    Case.err = 'Ctrl + C'
    Case.status()