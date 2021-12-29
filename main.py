q1 = 0  # First Quantum
q2 = 0  # Second Quantom
processes = []  # All processes


class Process:
    def __init__(self, label, execTime, startTime):
        self.label = label
        self.execTime = int(execTime)
        self.remainingTime = self.execTime
        self.startTime = int(startTime)
        self.endTime = -1
        self.runningTime = 0

    # copies a process
    def copy(self):
        return Process(self.label, self.execTime, self.startTime)

    # changes remaining time for a process
    def run(self):
        self.remainingTime -= 1

    # checkes if a process is finished runnig or not -returns T or F
    def isFinished(self):
        return self.remainingTime == 0

    # calculates turnaround time
    def turnAroundTime(self):
        return self.endTime - self.startTime

    # calculates waiting time
    def waitingTime(self):
        return self.turnAroundTime() - self.execTime


def loadFile(fileName):
    # loads a file and reads the data
    with open(fileName, 'r') as file:
        processCount = int(file.readline())
        # sets a label for every process
        labels = list(map(lambda i: f'P{i}', range(processCount)))

        # creates a list containing execution time of each process
        execTimes = file.readline().split(',')
        execTimes = list(map(lambda x: x.strip(), execTimes))

        # creates a list containing start time of each process
        startTimes = file.readline().split(',')
        startTimes = list(map(lambda x: x.strip(), startTimes))

        # sets Quantum 1
        global q1
        q1 = int(file.readline())
        # sets Quantum 2
        global q2
        q2 = int(file.readline())

        global processes
        # creates a list of tupples containig all data of a process
        processes = list(map(lambda x: Process(
            x[0], x[1], x[2]), zip(labels, execTimes, startTimes)))
        # sorts all processes by shortest start time
        processes.sort(key=lambda process: process.startTime)


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
            # if the start time of a process equals to the time we're on,
            if process.startTime == time:
                # adds the process to ready queue,
                readyQueue.append(process)
                # and removes it from the processes list.
                processesCopy.remove(process)

            # when reaches the first start time that
            #  we haven't reached yet, gets out of for loop
            elif process.startTime > time:
                break
        srt = None
        # srt is the process with shortest remaining time

        for process in readyQueue:
            # if there is no srt, or the process has less
            # execution time than srt: set the process as srt
            if not srt or srt.execTime > process.execTime:
                srt = process

        # if there is srt and it's also running, increase running time by 1
        if srt and srt is running:
            srt.runningTime += 1

        # if srt and running are different, print the running process and replace them
        elif srt and running:
            print(f'{running.label}({running.runningTime})', end=' --> ')
            running.runningTime = 0
            running = srt
            running.runningTime += 1

        # when nothing is running, set srt as running
        elif srt:
            running = srt
            running.runningTime += 1

        # each time loop starts, decrease remaining time of running by 1
        if running:
            running.run()
        # increase time by 1
        time += 1

        # when running is finished,
        # set the endTime to the time
        # and remove it from ready queue
        if running and running.isFinished():
            running.endTime = time
            readyQueue.remove(running)
            # calculate sum of turnaround time and sum of waiting time
            sumTT += running.turnAroundTime()
            sumWT += running.waitingTime()
    # print the running process
    print(f'{running.label}({running.runningTime})')
    # calculate sum of turnaround time and sum of waiting time
    sumTT += running.turnAroundTime()
    sumWT += running.waitingTime()
    # calculate average of turnaround time and average of waiting time
    avgTT = sumTT / len(processes)
    avgWT = sumWT / len(processes)
    # print averages
    print(" ____________________________________________________")
    print("|                                                    |")
    print(f'|   Average Turnaround Time:\t{avgTT}   |')
    print(f'|   Average   Waiting  Time:\t{avgWT}   |')
    print("|____________________________________________________|")
    print()


def hrrn():
    #=======================================#
    #==    Highest Response Ratio Next    ==#
    #=======================================#

    print('=================================')
    print('=  Highest Response Ratio Next  =')
    print('=================================')
    print()
    # response ratio = 1 + w/s
    # where w is total waiting time until the time
    # and s is service time of process (execTime)
    pass


def rr():
    #=======================================#
    #==            Round Robin            ==#
    #=======================================#

    print('=================================')
    print('=          Round Robin          =')
    print('=================================')
    print()
    pass


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
    pass


#===========================================#
loadFile('test.txt')
srtf()
hrrn()
rr()
mfq()
