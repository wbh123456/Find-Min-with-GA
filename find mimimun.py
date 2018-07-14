#Optimize the minimum point for funtion (100*sin(x)+0.01*x^2) through genetic algorithm (min = (-1.5705,-99.975)) 
#evolution by crossover, mutation
# all values are 3 dec places


#process:1. generate random generation ->2. calculate fitnesses of the population -> 3. select parents based on fitnesses -> 4. combine parents dna to get next generation -> go to step 2


import random
import math
import matplotlib.pyplot as plt

selection_range=300000
population=200
num_generations=80
mutation_rate = 0.008


total_mutation_record=0
maximum_extensionmutation=0
best_list=[]
best = [1E10,1E10]
def random_generation():
    #generate a random genertion of population defined above
    generation=[]
    for i in range(population):
        generation.append(round(random.uniform(-selection_range,selection_range),3))
    return generation

def get_fitness(generation):                #(list)--(list)
    # the bigger the fitness is, the better the solution is
    #fitness is the difference between the max y value and the y value
    value_list = []
    fitness_list = []
    for x in range (len(generation)):
        num = generation[x]
        value_list.append (100*math.sin(num)+0.01*num**2)
        #get corresponding y value
    maxvalue= max(value_list)
    for x in range (len(generation)):
        value= value_list[x]
        fitnessvalue = (maxvalue-value)**2
        fitness_list.append(fitnessvalue)
        
    global best  
    global best_list
    minvalue = min(value_list)
    
    if minvalue <= best[1]:
        best = [generation[value_list.index(minvalue)],minvalue]
        best_list.append(best[0])
    else:
        best_list.append(best[0])
  
    #record best value    
    return fitness_list

def select_individuals(generation,fitness_list):    #select a group of individuls based on its fitness to form next generation
    # (list, list) to (list)
    selected_individuals = []
    fitness_sum = sum (fitness_list)
    # if all the individuals are identical
    if fitness_sum == 0:
        print("sum_fitness = 0, all values are the same")
    #generate corresponding picking posibility for the generation    
    length = len(fitness_list)
    prob_list = []
    #pick individuals based on posibility
    for x in range(len(fitness_list)):
        prob_list.append((fitness_list[x]) /fitness_sum)
    for x in range(0, length*2):
        target=random.random()
        accumulation = 0
        i = 0
        while (i <length and accumulation <= target):
            accumulation += prob_list[i]
            i += 1
        index = i -1
        selected = generation[index]
        selected_individuals.append(selected)
    return selected_individuals
                  
def get_newgeneration(selected_individuals):      
    # list(2*popultion) -> list(population)
    #get new individuals from selected old individuals
    mylist = []
    newgeneration=[]
    
    #turn selected_individuals to a binary list with form'(-)0b###'
    for x in range(len(selected_individuals)):
        num = bin(int(selected_individuals[x]*1000))            # num = acctual num *1000 to eliminate decimal places
        mylist.append(num)
        
    # insert '0' to whichever is value that is smaller to make two values (dna) equal length   
    for x in range(population):
        a_list = list(mylist[2*x])
        b_list = list(mylist [2*x +1])
        if a_list[0] != '-':
            a_list.insert(0,'+')     
        if b_list[0] != '-':
            b_list.insert(0,'+')
        dif = abs(len(a_list)-len(b_list))
        ab_list=[]
        if len(a_list) > len(b_list):
            for x in range(dif):
                b_list.insert(3,'0')
        if len(a_list) < len(b_list):
            for x in range(dif):
                a_list.insert(3,'0')
               
    #add mutation based on mutation rate
        for x in range(len(a_list)):
            global mutation_record
            global total_mutation_record  
                
            if x>= 3 and mutation_rate > random.uniform(0,1):
                ab_list.append( str(random.choice([0,1])) )  
                total_mutation_record+=1
                mutation_record += 1
    #if no mutation, generate child dna based on parents'      
            else:    
                ab_list.append(random.choice([a_list[x],b_list[x]]))
    #extension mutation settings        
        global maximum_extensionmutation
            
        extensionmutation = 0
        
        while x>=3 and mutation_rate>random.uniform(0,1):
            ab_list.append( str(random.choice([0,1])) )  
            total_mutation_record+=1
            mutation_record += 1
            extensionmutation += 1
            maximum_extensionmutation = max( maximum_extensionmutation , extensionmutation)             
        ab2 = ''.join(ab_list)
        ab10 = int(ab2 , 2)/1000  #back to actual num by /1000
        newgeneration.append(ab10)
    return (newgeneration)

# a list to record average values
generation = random_generation()
fitness = get_fitness(generation)
print("generaiton 1:",generation,'\n')
print('    average value =' , sum(generation)/len(generation))
average_list = [sum(generation)/len(generation)]




for x in range(1, num_generations):
    mutation_record = 0
    nextgeneration = get_newgeneration(select_individuals(generation, fitness))[:]
    fitness = get_fitness(nextgeneration)
    generation = nextgeneration[:]
    average = sum(nextgeneration)/len(nextgeneration)
    average_list.append(average)
    print("generation",x+1)
    print(nextgeneration)
    #print('   fitness =',fitness)
    print('    average value =' , average)
    print('    local mutaton',mutation_record)

print("\ntotal mutation= ",total_mutation_record)
print("maximum extension mutation", maximum_extensionmutation)
print("best number found = ",best) 

with open('average_values.csv','w') as file:
    file.write('average value'+','+'best value'+'\n')
    for x in range(num_generations):
        file.write(str(average_list[x])+','+str(best_list[x])+'\n')
      
plt.plot(average_list,'x')
plt.plot(best_list,'.')
plt.show()