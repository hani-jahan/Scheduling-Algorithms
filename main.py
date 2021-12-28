q1 = 0
q2 = 0
processes = []


class Process:
    def __init__(self, label, execTime, startTime):
        self.label = label
        self.execTime = int(execTime)
        self.startTime = int(startTime)
        self.runningTime = 0


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
    processesCopy = processes.copy()
    readyQueue = []
    i = 0
    while len(processesCopy) != 0 or len(readyQueue) != 0:
        for process in processesCopy:
            if process.startTime == i:
                readyQueue.append(process)
                processesCopy.remove(process)
            elif process.startTime > i:
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
        if srt: 
            srt.execTime -= 1
        i += 1
        if srt and srt.execTime == 0: readyQueue.remove(srt)
    print(f'{running.label}({running.runningTime})', end='')
loadFile('test.txt')
srtf()
