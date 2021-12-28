q1 = 0
q2 = 0
processes = []


class Process:
    def __init__(self, label, execTime, startTime):
        self.label = label
        self.execTime = int(execTime)
        self.remainingTime = self.execTime
        self.startTime = int(startTime)
        self.endTime = -1
        self.runningTime = 0

    def copy(self):
        return Process(self.label, self.execTime, self.startTime)

    def run(self):
        self.remainingTime -= 1
    
    def isFinished(self):
        return self.remainingTime == 0
    
    def turnAroundTime(self):
        return self.endTime - self.startTime

def loadFile(fileName):
    with open(fileName, 'r') as file:
        processCount = int(file.readline())
        labels = list(map(lambda i: f'P{i}', range(processCount)))

        execTimes = file.readline().split(',')
        execTimes = list(map(lambda x: x.strip(), execTimes))

        startTimes = file.readline().split(',')
        startTimes = list(map(lambda x: x.strip(), startTimes))

        global q1
        q1 = int(file.readline())
        global q2
        q2 = int(file.readline())

        global processes
        processes = list(map(lambda x: Process(x[0], x[1], x[2]), zip(
            labels, execTimes, startTimes)))
        processes.sort(key=lambda process: process.startTime)


def srtf():
    running = None
    global processes
    processesCopy = list(map(lambda x: x.copy(), processes))
    readyQueue = []
    time = 0
    sumTT = 0
    sumWT = 0
    while len(processesCopy) != 0 or len(readyQueue) != 0:
        for process in processesCopy:
            if process.startTime == time:
                readyQueue.append(process)
                processesCopy.remove(process)
            elif process.startTime > time:
                break
        srt = None
        for process in readyQueue:
            if not srt or srt.execTime > process.execTime:
                srt = process
        if srt and srt is running:
            srt.runningTime += 1
        elif srt and running:
            print(f'{running.label}({running.runningTime})', end='--')
            running.runningTime = 0
            running = srt
            running.runningTime += 1
        elif srt:
            running = srt
            running.runningTime += 1
        if running:
            running.run()
        time += 1
        if running and running.isFinished():
            running.endTime = time
            readyQueue.remove(running)
            sumTT += running.turnAroundTime()
    print(f'{running.label}({running.runningTime})')
    sumTT += running.turnAroundTime()
    avgTT = sumTT / len(processes)
    print(f'Average Turnaround Time: {avgTT}')

loadFile('test.txt')
srtf()
