q1 = 0  # First Quantum
q2 = 0  # Second Quantom
processes = []  # All processes


class Process:
    def __init__(self, label, burstTime, arrivalTime):
        self.label = label
        self.burstTime = int(burstTime)
        self.arrivalTime = int(arrivalTime)
        self.execTime = 0
        self.exitTime = -1
        self.remainingTime = self.burstTime

    def __str__(self):
        return (f'label:{self.label}\t Burst:{self.burstTime}\t Arrival:{self.arrivalTime}\t TT:{self.execTime}\t exit:{self.exitTime}\t remaining:{self.remainingTime}\t Responce Ratio:{self.responseRatio()}')

    # copies a process
    def copy(self):
        return Process(self.label, self.burstTime, self.arrivalTime)

    # runs process for 1 time (decreases remaining time by 1)
    def run(self):
        self.remainingTime -= 1

    # checkes if a process is finished runnig or not -returns T or F
    def isFinished(self):
        return self.remainingTime == 0

    # calculates turnaround time
    def turnAroundTime(self):
        return self.exitTime - self.arrivalTime


    def responseRatio(self, time):
        return (time - self.arrivalTime + self.remainingTime) / self.burstTime

    # calculates turnaround time by waiting time
    def turnAroundTime_byWT(self):
        return self.burstTime + self.waitingTime()

    # calculates waiting time
    def waitingTime(self):
        return self.turnAroundTime() - self.burstTime


def loadFile(fileName):
    # loads a file and reads the data
    with open(fileName, 'r') as file:
        processCount = int(file.readline())
        # sets a label for every process
        labels = list(map(lambda i: f'P{i}', range(processCount)))

        # creates a list containing burst time of each process
        burstTimes = file.readline().split(',')
        burstTimes = list(map(lambda x: x.strip(), burstTimes))

        # creates a list containing arrival time of each process
        arrivalTimes = file.readline().split(',')
        arrivalTimes = list(map(lambda x: x.strip(), arrivalTimes))

        # sets Quantum 1
        global q1
        q1 = int(file.readline())
        # sets Quantum 2
        global q2
        q2 = int(file.readline())

        global processes
        # creates a list of tupples containig all data of a process
        processes = list(map(lambda x: Process(
            x[0], x[1], x[2]), zip(labels, burstTimes, arrivalTimes)))
        # sorts all processes by arrival time
        processes.sort(key=lambda process: process.arrivalTime)


def srtf():
    #=======================================#
    #==   shortest remaining time first   ==#
    #=======================================#

    print('=================================')
    print('= shortest remaining time first =')
    print('=================================')
    print()
    running = None
    # 'runing' is the process that is running at the time
    global processes
    # create a copy of all processes
    processesCopy = list(map(lambda x: x.copy(), processes))
    # set an empty ready queue
    readyQueue = []
    # set time
    time = 0
    # set sum of turnaround time
    sumTT = 0
    # set sum of waiting time
    sumWT = 0

    # loop runs until processes list or ready queue are not empty
    while len(processesCopy) != 0 or len(readyQueue) != 0:
        # for all the processes:
        for process in processesCopy:
            # if the arrival time of a process equals to the time we're on,
            if process.arrivalTime == time:
                # adds the process to ready queue,
                readyQueue.append(process)
            # when reaches the first arrival time that
            #  we haven't reached yet, gets out of for loop
            elif process.arrivalTime > time:
                break
            for process in readyQueue:
                # and removes it from the processes list.
                if process in processesCopy:
                    processesCopy.remove(process)

        srt = None
        # srt is the process with shortest remaining time

        for process in readyQueue:
            # if there is no srt, or the process has less
            # burst time than srt: set the process as srt
            if not srt or srt.remainingTime > process.remainingTime:
                srt = process

        # if there is srt and it's also running, increase turnaround time by 1
        if srt and srt is running:
            srt.execTime += 1

        # if srt and running are different, print the running process and replace them
        elif srt and running:
            print(f'{running.label}({time})', end=' --> ')
            running.execTime = 0
            running = srt
            running.execTime += 1

        # when nothing is running, set srt as running
        elif srt:
            running = srt
            running.execTime += 1

        # each time loop starts, decrease remaining time of running by 1
        if running:
            running.run()
        # increase time by 1
        time += 1

        # when running is finished,
        # set the exitTime to the time
        # and remove it from ready queue
        if running and running.isFinished():
            running.exitTime = time
            readyQueue.remove(running)
            # calculate sum of turnaround time and sum of waiting time
            sumTT += running.turnAroundTime()
            sumWT += running.waitingTime()
    # print the running process
    print(f'{running.label}({time})')
    # calculate sum of turnaround time and sum of waiting time
    sumTT += running.turnAroundTime()
    sumWT += running.waitingTime()
    # calculate average of turnaround time and average of waiting time
    avgTT = sumTT / len(processes)
    avgWT = sumWT / len(processes)
    # print averages
    print(" _______________________________________")
    print("|                                       |")
    print(f'|   Average Turnaround Time:\t{avgTT}\t|')
    print(f'|   Average   Waiting  Time:\t{avgWT}\t|')
    print("|_______________________________________|")
    print()


def hrrn():
    #=======================================#
    #==    Highest Response Ratio Next    ==#
    #=======================================#

    print('=================================')
    print('=  Highest Response Ratio Next  =')
    print('=================================')
    print()

    running = None
    # 'runing' is the process that is running at the time
    global processes
    # create a copy of all processes
    processesCopy = list(map(lambda x: x.copy(), processes))
    # set an empty ready queue
    readyQueue = []
    # set time
    time = 0
    # set sum of turnaround time
    sumTT = 0
    # set sum of waiting time
    sumWT = 0

    while len(processesCopy) != 0 or len(readyQueue) != 0:
        for process in processesCopy:
            if process.arrivalTime <= time:
                readyQueue.append(process)
            elif process.arrivalTime > time:
                break
            for process in readyQueue:
                if process in processesCopy:
                    processesCopy.remove(process)

        hrr = None
        for process in readyQueue:

            if not hrr or hrr.responseRatio(time) < process.responseRatio(time):
                hrr = process

        hrr.execTime += hrr.burstTime
        hrr.remainingTime = 0
        time += hrr.burstTime
        hrr.exitTime = time
        print(f'{hrr.label}({time})', end=' --> ')
        readyQueue.remove(hrr)
        sumTT += hrr.turnAroundTime()
        sumWT += hrr.waitingTime()

    # calculate average of turnaround time and average of waiting time
    avgTT = sumTT / len(processes)
    avgWT = sumWT / len(processes)
    # print averages
    print()
    print(" _______________________________________")
    print("|                                       |")
    print(f'|   Average Turnaround Time:\t{avgTT}\t|')
    print(f'|   Average   Waiting  Time:\t{avgWT}\t|')
    print("|_______________________________________|")
    print()


def rr():
    #=======================================#
    #==            Round Robin            ==#
    #=======================================#

    print('=================================')
    print('=          Round Robin          =')
    print('=================================')
    print()

    running = None
    global q1
    global processes
    # create a copy of all processes
    processesCopy = list(map(lambda x: x.copy(), processes))
    # set an empty ready queue
    readyQueue = []
    # set time
    time = 0

    while len(processesCopy) != 0 or len(readyQueue) != 0 or (running and not running.isFinished()):
        # for all the processes:
        for process in processesCopy:
            if process.arrivalTime <= time:
                readyQueue.append(process)
            elif process.arrivalTime > time:
                break
        if running and not running.isFinished():
            readyQueue.append(running)
        for process in readyQueue:
            if process in processesCopy:
                processesCopy.remove(process)

        running = readyQueue.pop(0)

        if running.remainingTime <= q1:
            time += running.remainingTime
            running.remainingTime = 0
            running.exitTime = time
            running.execTime += running.remainingTime
            print(f'{running.label}({time})', end=' --> ')
            running.execTime = 0

        elif running.remainingTime > q1:
            running.remainingTime -= q1
            running.execTime += q1
            time += q1
            print(f'{running.label}({time})', end=' --> ')
            running.execTime = 0


def mfq():
    #=======================================#
    #==     Multilevel Feedback Queue     ==#
    #==                                   ==#
    #== Queue1 & Queue2: RR, Queue3: FCFS ==#
    #=======================================#

    print('=================================')
    print('=   Multilevel Feedback Queue   =')
    print('=================================')
    print()

    running = None
    global q1
    global q2
    global processes
    # create a copy of all processes
    processesCopy = list(map(lambda x: x.copy(), processes))
    # set empty ready queueس
    queue1 = []
    queue2 = []
    queue3 = []
    # set time
    time = 0


#===========================================#
loadFile('test.txt')
# srtf()
# hrrn()
rr()
