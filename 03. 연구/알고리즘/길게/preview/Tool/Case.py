from time import time
from RandomMap import randomMap

class Case:

    ct = 0
    sumStep, sumTime = 0,0
    avgStep, avgTime = 0,0
    maxStep, maxTime = 0,0

    maxStepCase = None
    maxTimeCase = None
    failCase = None

    printStyle = " [{}] | {},'{}','{}'"

    def __init__(self,Type):
        self.Type = Type
        Case.ct += 1
        self.ct = Case.ct

        self.rdm = randomMap(Type)
        self.Step,self.Time = 0,0
        err = None

    def run(self):
        m,*a = self.rdm
        try:
            t = time()
            self.res = Case.main(self.Type,m,*a)
            self.Step = len(self.res)
            self.Time = round(time() - t,5)
        except Exception as err:
            Case.failCase = self
            self.err = err
            return 0
        else:
            isPrint = self.updateInfo()
            if isPrint:
                self.info(mark = isPrint)
            return 1

    def updateInfo(self):
        Step,Time = self.Step,self.Time
        Case.sumStep += Step
        Case.sumTime += Time
        Case.avgStep = Case.sumStep // Case.ct
        Case.avgTime = round(Case.sumTime / Case.ct,5)
        isMaxStep = Case.maxStep < Step
        isMaxTime = Case.maxTime < Time
        if isMaxStep:
            Case.maxStep = Step
            Case.maxStepCase = self
        if isMaxTime:
            Case.maxTime = Time
            Case.maxTimeCase = self
        return 1 if isMaxStep else 2 if isMaxTime else None

    def i2d(t):
        return [int((t*250)//60),int((t*250)%60)]

    def info(self,st='',mark=None):
        print(st + Case.printStyle.format(self.ct,self.Type,*self.rdm))
        m,s = Case.i2d(self.Time)
        Step = '[↑]'+str(self.Step) if mark == 1 else self.Step
        Time = '[↑]'+str(self.Time) if mark == 2 else self.Time
        print(st + ' {}steps, {}s(dart {}m {}s)'.format(Step,Time,m,s))
        print(st + '')

    def status():
        isFail = Case.failCase != None
        print(' >>>\n')
        print(' Result ->','Failed({})'.format(Case.failCase.err) if isFail else 'Completed')
        print(' Loop in {} times'.format(Case.ct))
        print(' Avg: {}step/{}s(dart {}m {}s)'.format(Case.avgStep,Case.avgTime,*Case.i2d(Case.avgTime)))
        print()
        if isFail:
            Case.failCase.info()
        else:
            print(' [ Max Step ]')
            Case.maxStepCase.info()
            print(' [ Max Time ]')
            Case.maxTimeCase.info()


