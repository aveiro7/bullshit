# Flow-shop problem solution
# with Simulated Annealing

# How to use: first argument on command line is number of machines, second argument - number of tasks
# When the application is run properly, user is prompted about more data, which is (for each task)
# time on first machine, time on second machine, ... , time on last machine, gain of the task
# Each number (integer!) should be entered in new line.
# The last prompt is about maximum allowed time.

# To increase the accuracy of the algorithm, change constants: numberOfIterations and temperature

import sys
from itertools import permutations
import random
import math
from copy import deepcopy

numberOfMachines = 0
numberOfTasks = 0
tasks = []
maxTime = 0
numberOfIterations = 100
temperature = 1

# additional function to check if a solution is valid
def findFirstCompletedTask(runningTasks):
    id = 0
    time = maxTime
    machine = 0
    for i in range(0, len(runningTasks)):
        if len(runningTasks[i]) > 0:
            if runningTasks[i][1] < time:
                time = runningTasks[i][1]
                id = runningTasks[i][0]
                machine = i
    return (id, time, machine)

# additional function
def notEmpty(listOfTasks):
    for task in listOfTasks:
        if len(task) > 0:
            return True
    return False

# checking the validity of the solution
def isGoodSolution(sol):
    # empty solution is not valid
    if not sol:
        return False

    # too big solution is not valid
    if(len(sol) > numberOfTasks):
        return False

    # simulate executing each task of the solution
    machines = []
    for i in range(0, numberOfMachines):
        machines.append([])

    for i in sol:
        machines[0].append([i, tasks[i][0]])

    # at first only task that's running is the first one
    runningTasks = [machines[0][0]]

    overallTime = 0
    while notEmpty(runningTasks):
        (id, time, machineNr) = findFirstCompletedTask(runningTasks)
        overallTime += time

        if overallTime > maxTime:
            return False

        # update time for each running task
        for i in range(0, len(runningTasks)):
            if len(machines[i]) > 0:
                machines[i][0][1] -= time

        # move completed tasks to next machines
        for i in range(0, len(runningTasks)):
            if len(machines[i]) > 0 and machines[i][0][1] == 0:
                if i < (numberOfMachines - 1):
                    task_id = machines[i][0][0]
                    machines[i+1].append([task_id, tasks[task_id][i+1]])
                del machines[i][0]

        # update runningTasks
        runningTasks = []
        for machineQueue in machines:
            if not machineQueue:
                runningTasks.append([])
            else:
                runningTasks.append(machineQueue[0])
    return True

def isLastPermutation(perm):
    for i in range(1, len(perm)):
        if perm[i] > perm[i - 1]:
            return False
    return True

# checking in the neighbourghood
def findNextSolution(sol, perm):
    # for an empty list, randomly add one task
    if len(sol) == 0:
        randomTask = random.randint(0, numberOfTasks - 1)
        sol.append(randomTask)
        perm = next(permutations(sol))
        return (sol, perm)
    # if it's the last permutation, change existing solution (with equal probability: add, delete or swap)
    if isLastPermutation(sol):

        # if all the tasks are included, delete one
        if len(sol) == numberOfTasks:
            toDelete = random.randint(0, numberOfTasks - 1)
            del sol[toDelete]

        indexToDelete = random.randint(0, len(sol) - 1)
        newTask = sol[0]
        while newTask in sol:
            newTask = random.randint(0, numberOfTasks - 1)

        randomProbability = random.random()
        if randomProbability < 0.33:
            sol.append(newTask)
            del sol[indexToDelete]
        elif randomProbability < 0.66:
            del sol[indexToDelete]
        else:
            sol.append(newTask)

        sol.sort()
        perm = permutations(sol)
        next(perm)
    # it there are next permutations, check them
    else:
        sol = list(next(perm))

    # return only valid solutions
    if isGoodSolution(sol):
        return (sol, perm)
    else:
        return findNextSolution(sol,perm)

# first solution is based on all the tasks available
def findFirstSolution():
    solution = list(range(0, numberOfTasks))
    permutation = permutations(solution)
    while not isGoodSolution(solution):
        (solution, permutation) = findNextSolution(solution,permutation)
    return solution

# calculates value of the solution (gain)
def getValue(sol):
    val = 0
    for i in sol:
        val += tasks[i][-1]
    return val

# calculates (randomly) if a worse solution should be accepted
def calculateProbability(f):
    ppb = math.exp(f / temperature)
    x = random.uniform(0, 1)
    return x < ppb

# calculates the solution of the problem
def findSolution():
    sol = findFirstSolution()
    permutation = permutations(sol)
    next(permutation)
    for i in range(0, numberOfIterations):
        oldSolution = deepcopy(sol)
        oldPermutation = deepcopy(permutation)
        newSolution, newPermutation = findNextSolution(sol, permutation)
        sol = oldSolution
        permutation = oldPermutation
        val = getValue(oldSolution)
        newValue = getValue(newSolution)
        if newValue >= val:
            sol = newSolution
            permutation = newPermutation
        elif calculateProbability(newValue - val):
            sol = newSolution
            permutation = newPermutation
    return sol

def main():
    global numberOfMachines
    global numberOfTasks
    global tasks
    global maxTime

    if len(sys.argv) < 3:
        raise BaseException

    numberOfMachines = int(sys.argv[1])
    numberOfTasks = int(sys.argv[2])

    i = 0
    tasks = []
    while i < numberOfTasks:
        j = 0
        task = []
        while j <= numberOfMachines:
            x = int(input("Please, give me more data: "))
            task.append(x)
            j += 1
        tasks.append(task)
        i += 1
    maxTime = int(input("Enter maximum allowed time: "))

    # Here is hardcoded sample problem - the optimal solution is [1, 0] with gain 55
    # tasks = [[5, 1, 20],[1, 6, 35]]
    # maxTime = 8

    sol = findSolution()
    print("Your solution is:", sol, "with total gain:", getValue(sol))

if __name__ == "__main__":
    main()