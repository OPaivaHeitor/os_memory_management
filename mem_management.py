import random
memory_size_units = 256  # 256 unidades de 4KB (1MB)
nextFitPointer = 0
TIME = 0  # Tempo de execução para viabilizar FIFO
total_requests = 10000  # Ajuste de número de requisições


class Process:
    def __init__(self, PID, mem_units, t):
        self.PID = PID
        self.mem_units = mem_units
        self.alloc_time = t


class Memory:
    def __init__(self, size_in_units):
        self.size = size_in_units
        self.memory = []
        self.processList = []
        for i in range(size_in_units):
            self.memory.append(0)  # inicializa vazio
        self.freeMem = size_in_units

    def getOldestProcess(self):
        minTime = (2 ** 63) - 1
        oldestProcess = None

        for process in self.processList:
            if process.alloc_time < minTime:
                minTime = process.alloc_time
                oldestProcess = process

        return oldestProcess

    def firstFit(self, hole_locations, Process):
        for i in range(Process.mem_units):
            self.memory[hole_locations[0] + i] = Process.PID
            self.freeMem -= 1
        self.processList.append(Process)

    def bestFit(self, hole_locations, hole_sizes, Process):
        bestHoleLocation = hole_locations[hole_sizes.index(min(hole_sizes))]
        for i in range(Process.mem_units):
            self.memory[bestHoleLocation + i] = Process.PID
            self.freeMem -= 1
        self.processList.append(Process)

    def worstFit(self, hole_locations, hole_sizes, Process):
        worstHoleLocation = hole_locations[hole_sizes.index(max(hole_sizes))]
        for i in range(Process.mem_units):
            self.memory[worstHoleLocation + i] = Process.PID
            self.freeMem -= 1
        self.processList.append(Process)

    def nextFit(self, hole_locations, hole_sizes, Process, pointer):
        if pointer >= len(self.memory):
            pointer = 0
        for i in range(Process.mem_units):
            self.memory[hole_locations[pointer] + i] = Process.PID
            self.freeMem -= 1
        pointer += Process.mem_units
        self.processList.append(Process)
        return pointer

    # retorna a quantidade de buracos em que o processo cabe, bem como suas localizações e tamanhos
    def find_holes(self, Process, statReport):
        holes_found = 0
        hole_locations = []
        hole_sizes = []
        for i in range(len(self.memory)):
            if self.memory[i] == 0:  # se for buraco (processos não tem pid 0)
                statReport.update_stats(1, 0, 0)
                hole_size = 0
                # itera do início do buraco até o fim da memória
                for j in range(i, len(self.memory)):
                    if self.memory[j] == 0:
                        hole_size += 1
                    else:
                        break  # termina de iterar se encontrar um pid diferente de 0
                if hole_size >= Process.mem_units:  # testa se cabe no buraco
                    holes_found += 1
                    hole_locations.append(i)
                    hole_sizes.append(hole_size)
        if (holes_found > 0):
            return holes_found, hole_locations, hole_sizes
        else:
            return -1

    def alloc_mem(self, Process, method, statReport):
        holes_found = 0
        hole_locations = []
        hole_sizes = []
        if self.freeMem < Process.mem_units:
            return -1
        else:
            if (self.find_holes(Process, statReport) == -1):
                statReport.failCount += 1
                return -1
            else:
                holes_found, hole_locations, hole_sizes = self.find_holes(
                    Process, statReport)
                if method == 0:
                    self.firstFit(hole_locations, Process)  # first fit
                if method == 1:
                    self.bestFit(hole_locations, hole_sizes,
                                 Process)  # best fit
                if method == 2:
                    self.worstFit(hole_locations, hole_sizes,
                                  Process)  # worst fit
                if method == 3:
                    nextFitPointer = self.nextFit(
                        hole_locations, hole_sizes, Process, nextFitPointer)  # next fit

    # deleta um processo da memória seguindo critério FIFO, retorna -1 se não houver nada para ser deletado, e 1 se algo for deletado
    def dealloc_mem(self):
        if len(self.processList) < 1:
            return -1
        else:
            oldProcess = self.getOldestProcess()
            for i in range(len(self.memory)):
                if self.memory[i] == oldProcess.PID:
                    self.memory[i] = 0
                    self.freeMem += 1
            self.processList.remove(oldProcess)
            return 1

    def frag_count(self):
        size_cont = 0
        hole_cont = 0
        flag = 0
        for i in range(len(self.memory)):
            if size_cont > 2:
                size_cont = 0
                flag = 1
            if self.memory[i] == 0 and flag == 0:
                size_cont += 1
            if self.memory[i] != 0:
                flag = 0
                if size_cont > 0 and size_cont <= 2:
                    hole_cont += 1
        return hole_cont


class RequestGenerator:
    def __init__(self):
        self.PID = 1

    def generate_request(self, statReport):
        global TIME
        statReport.update_stats(0, 1, 0)
        self.PID = random.randint(1, 100000)
        self.mem_units = random.randint(3, 15)
        self.alloc_time = TIME
        TIME += 1
        return self.PID, self.mem_units, self.alloc_time


class StatsReporter:
    def __init__(self):
        self.totalTime = 0
        self.meanTime = 0
        self.requestCount = 0
        self.failCount = 0

    def update_stats(self, time, requestCount, failCount):
        self.totalTime += time
        self.requestCount += requestCount
        self.failCount += failCount
        self.meanTime = self.totalTime / self.requestCount

    def generate_report(self):
        print("Tempo medio de alocacao: " + str(self.meanTime))
        print("Percentual de falhas: " +
              str(self.failCount / (self.failCount + self.requestCount)))
        # Generate the report with the required parameters for each algorithm
        # Write the report to a file


def main():
    memory = Memory(memory_size_units)
    generator = RequestGenerator()
    statReport = StatsReporter()
    Allocation_Algorithm = 0  # 0: First Fit, 1: Best Fit, 2: Worst Fit, 3: Next Fit

    if Allocation_Algorithm == 0:
        print("FIRST FIT:")
    if Allocation_Algorithm == 1:
        print("BEST FIT:")
    if Allocation_Algorithm == 2:
        print("WORST FIT:")
    if Allocation_Algorithm == 3:
        print("NEXT FIT:")

    for i in range(total_requests):
        pid, mem_units, alloc_time = generator.generate_request(statReport)
        process = Process(pid, mem_units, alloc_time)
        if memory.alloc_mem(process, Allocation_Algorithm, statReport) == -1:
            if memory.dealloc_mem() == -1:
                print("Erro ao alocar processo")
                break
    statReport.generate_report()
    print("Pelos dados levantados pelo programa, conclui-se que o algoritmo de alocação de memória que apresenta melhor desempenho é o First Fit., enquanto o pior desempenho é o do Worst Fit.")


main()
