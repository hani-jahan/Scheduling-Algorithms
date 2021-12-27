q1 = 0
q2 = 0
processes = []

class Process:
    def __init__(self, execTime, startTime):
        self.execTime = execTime
        self.startTime = startTime


def loadFile(fileName):
    with open(fileName, 'r') as file:
        processCount = int(file.readline())

        execTimes = file.readline().split(',')
        execTimes = map(execTimes, lambda x: x.strip())

        startTimes = file.readline().split(',')
        startTimes = map(startTimes, lambda x: x.strip())

        global q1
        q1 = int(file.readline())
        global q2
        q2 = int(file.readline())

        global processes
        processes = map(zip(execTimes, startTimes),
                        lambda x: Process(x[0], x[1]))

