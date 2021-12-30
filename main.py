q1 = 0  # First Quantum
q2 = 0  # Second Quantom
processes = []  # All processes


class Process:
    def __init__(self, label, burstTime, arivalTime):
        self.label = label
        self.burstTime = int(burstTime)
        self.arivalTime = int(arivalTime)
        self.turnaroundTime = 0
        self.exitTime = -1
        self.remainingTime = self.burstTime
        self.responceRatio = 0

    # copies a process
    def copy(self):
        return Process(self.label, self.burstTime, self.arivalTime)

    # runs process for 1 time (decreases remaining time by 1)
    def run(self):
        self.remainingTime -= 1

    # checkes if a process is finished runnig or not -returns T or F
    def isFinished(self):
        return self.remainingTime == 0

    # calculates turnaround time
    def turnAroundTime(self):
        return self.exitTime - self.arivalTime

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

        # creates a list containing arival time of each process
        arivalTimes = file.readline().split(',')
        arivalTimes = list(map(lambda x: x.strip(), arivalTimes))

        # sets Quantum 1
        global q1
        q1 = int(file.readline())
        # sets Quantum 2
        global q2
        q2 = int(file.readline())

        global processes
        # creates a list of tupples containig all data of a process
        processes = list(map(lambda x: Process(
            x[0], x[1], x[2]), zip(labels, burstTimes, arivalTimes)))
        # sorts all processes by arival time
        processes.sort(key=lambda process: process.arivalTime)


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
            # if the arival time of a process equals to the time we're on,
            if process.arivalTime == time:
                # adds the process to ready queue,
                readyQueue.append(process)
                # and removes it from the processes list.
                processesCopy.remove(process)

            # when reaches the first arival time that
            #  we haven't reached yet, gets out of for loop
            elif process.arivalTime > time:
                break
        srt = None
        # srt is the process with shortest remaining time

        for process in readyQueue:
            # if there is no srt, or the process has less
            # burst time than srt: set the process as srt
            if not srt or srt.remainingTime > process.remainingTime:
                srt = process

        # if there is srt and it's also running, increase turnaround time by 1
        if srt and srt is running:
            srt.turnaroundTime += 1

        # if srt and running are different, print the running process and replace them
        elif srt and running:
            print(f'{running.label}({running.turnaroundTime})', end=' --> ')
            running.turnaroundTime = 0
            running = srt
            running.turnaroundTime += 1

        # when nothing is running, set srt as running
        elif srt:
            running = srt
            running.turnaroundTime += 1

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
    print(f'{running.label}({running.turnaroundTime})')
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
    # response ratio = 1 + w/s
    # where w is total waiting time until the time
    # and s is service time of process (burstTime)

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
            if process.arivalTime <= time:

                readyQueue.append(process)
                processesCopy.remove(process)

            elif process.arivalTime > time:
                break

        hrr = None
        for process in readyQueue:
            process.responseRatio = (
                time - process.arivalTime + process.remainingTime) / process.burstTime
            # process.responseRatio = 1 + (
            #     (process.burstTime + (time - process.arivalTime)) / process.burstTime)
            if not hrr or hrr.responseRatio < process.responseRatio:
                hrr = process

        running = hrr
        running.turnaroundTime += running.burstTime
        running.remainingTime = 0
        time += running.burstTime
        running.exitTime = time
        readyQueue.remove(running)
        sumTT += running.turnAroundTime()
        sumWT += running.waitingTime()

    print(f'{running.label}({running.turnaroundTime})')

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


def rr():
    #=======================================#
    #==            Round Robin            ==#
    #=======================================#

    print('=================================')
    print('=          Round Robin          =')
    print('=================================')
    print()


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


#===========================================#
loadFile('test.txt')
srtf()
hrrn()
