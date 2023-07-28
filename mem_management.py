import random
nextFitPointer = 0


class Process:
    def __init__(self, PID, mem_units):
        self.PID = PID
        self.mem_units = mem_units


class Memory:
    def __init__(self, size_in_units):
        self.size = size_in_units
        for i in range(size_in_units):
            self.memory.append(0)  # inicializa vazio
        self.freeMem = size_in_units

    def firstFit(self, hole_locations, Process):
        for i in range(Process.mem.units):
            self.memory[hole_locations[0] + i] = Process.PID
            self.freeMem -= 1

    def bestFit(self, hole_locations, hole_sizes, Process):
        bestHoleLocation = hole_locations(hole_sizes.index(min(hole_sizes)))
        for i in range(Process.mem.units):
            self.memory[bestHoleLocation + i] = Process.PID
            self.freeMem -= 1

    def worstFit(self, hole_locations, hole_sizes, Process):
        worstHoleLocation = hole_locations(hole_sizes.index(max(hole_sizes)))
        for i in range(Process.mem.units):
            self.memory[worstHoleLocation + i] = Process.PID
            self.freeMem -= 1

    def nextFit(self, hole_locations, hole_sizes, Process, pointer):
        for i in range(Process.mem.units):
            self.memory[hole_locations[pointer] + i] = Process.PID
            self.freeMem -= 1
        pointer += Process.mem.units
        return pointer

    def find_holes(self, Process):  # retorna todos os buracos onde o processo cabe
        holes_found = 0
        hole_locations = []
        hole_sizes = []
        for i in range(len(self.memory)):
            if self.memory[i] == 0:  # se for buraco (processos não tem pid 0)
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

    def alloc_mem(self, Process, method):
        holes_found = 0
        hole_locations = []
        hole_sizes = []
        if self.freeMem < Process.mem_units:
            print("Não há memória suficiente para alocar o processo")
            return -1
        else:
            if (self.find_holes(Process) == -1):
                return -1
            else:
                holes_found, hole_locations, hole_sizes = self.find_holes(
                    Process)
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

    def dealloc_mem(self, PID):
        flag = -1
        for i in range(len(self.memory)):
            if self.memory[i] == PID:
                flag = 1
                self.memory[i] = 0
                self.freeMem += 1
        return flag

    # def frag_count(self):
        # Implement the fragmentation count for each algorithm here
        # Return the number of holes with size 1 or 2 units


class RequestGenerator:
    def __init__(self):
        self.PID = 1

    def generate_request(self):
        self.PID = random.randint(1, 100000)
        self.mem_units = random.randint(3, 15)
        return self.PID, self.mem_units


class StatsReporter:  # tempo médio em termos de número de nós atravessados na lista ligada até ocorrer a alocação e percentual de vezes que uma requisição de alocação falhou, pois não havia memória contígua suficiente. Esses parâmetros devem ser obtidos e atualizados a partir da inserção de cada requisição no componente de memória.
    def __init__(self):
        self.first_fit_stats = []
        self.next_fit_stats = []
        self.best_fit_stats = []
        self.worst_fit_stats = []

    # def update_stats(self, algorithm, mem_units, nodes_traversed, failed_allocation):
        # Update the statistics for the specified algorithm with the given parameters

    # def generate_report(self):
        # Generate the report with the required parameters for each algorithm
        # Write the report to a file


memory_size_units = 256  # 1 MB divided by 4 KB block size
memory = Memory(memory_size_units)
generator = RequestGenerator()
reporter = StatsReporter()

total_requests = 100  # You can adjust the number of requests as needed

for _ in range(total_requests):
    pid, mem_units = generator.generate_request()
    # Choose the appropriate allocation algorithm based on your simulation
    # Call the corresponding alloc_mem and dealloc_mem functions
    # Update the statistics using the StatsReporter class

    # Generate the final report using the StatsReporter class
reporter.generate_report()
