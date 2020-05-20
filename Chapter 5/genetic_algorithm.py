from __future__ import annotations
from typing import TypeVar, Generic, List, Tuple, Callable
from enum import Enum
from random import choices, random
from heapq import nlargest
from statistics import mean
from chromosome import Chromosome

C = TypeVar('C', bound = Chromosome) # type of the chromosome

class GeneticAlgorithm(Generic[C]):
    SelectionType = Enum('SelectionType', 'ROULETTE TOURNAMENT')
    
    def __init__(self, initial_population: List[C], threshold: float,
                max_generations: int = 100, mutation_chance: float = 0.01, 
                crossover_chance: float = 0.7, selection_type = SelectionType.TOURNAMENT) -> None:
        self._population: List[C] = initial_population
        self._threshold: float = threshold
        self._max_generations: int = max_generations
        self._mutation_chance: float = mutation_chance
        self._crossover_chance: float = crossover_chance
        self._selection_type: GeneticAlgorithm.SelectionType = selection_type
        # the fitness key will be some callable that 
        # takes ._population[0] as argument with the fitness attribute
        # the ._fitness_key will be different for each of our subclasses
        self._fitness_key: Callable = type(self._population[0]).fitness
            
    # define the roulette method of selection
    # Use the probability distribution wheel to pick 2 parents
    # Note: will not work on negative fitness results
    # the choices function (from the Python module random) 
    ### takes a list of things we want to pick from, a weight list for those things, and no. of things to pick###
    # https://www.w3schools.com/python/ref_random_choices.asp
    def _pick_roulette(self, wheel: List[float]) -> Tuple[C, C]:
        return tuple(choices(self._population, weights = wheel, k = 2))
    
    # Choose num_participants at random and take the best 2
    def _pick_tournament(self, num_participants: int) -> Tuple[C, C]:
        participants: List[C] = choices(self._population, k = num_participants)
        # use the nlargest method from heapq to pick the 2 most fitting chromosomes
        return tuple(nlargest(2, participants, key = self._fitness_key))
    
    # Replace the population with a new generation of individuals
    def _reproduce_and_replace(self) -> None:
        new_population: List[C] = []
        
        # keep going until we've filled the new generation
        while len(new_population) < len(self._population):
            
            # pick the 2 parents
            if self._selection_type == GeneticAlgorithm.SelectionType.ROULETTE:
                # we are increasing the chance of more fit chromosomes so we use the fitnesses of 
                # them as our wheel/weights
                parents: Tuple[C, C] = self._pick_roulette([x.fitness() for x in self._population])
                    
            else:
                # we will only take half if it is a tournament
                parents = self._pick_tournament(len(self._population) // 2)
            # potentially crossover the 2 parents
            if random() < self._crossover_chance:
                new_population.extend(parents[0].crossover(parents[1]))
            else:
                # if there are no children, the parents are just added to the new population
                new_population.extend(parents)
            
            # if we had an odd number, we'll have 1 extra , so we remove it
        if len(new_population) > len(self._population):
            new_population.pop()
                
        # replace reference
        self._population = new_population
            
    # With _mutation_chance probability mutate each individual
    def _mutate(self) -> None:
        for individual in self._population:
            if random() < self._mutation_chance:
                individual.mutate()
    
    # The .run() method coordinates all the different steps and bring the population from one gen
    # to another. It also keeps track of the best chromosome found at any point in the search
    # Run the genetic algorithm for max_generations iterations
    # and return the best individual found
    
    def run(self) -> C:
        best: C = max(self._population, key = self._fitness_key)
        for generation in range(self._max_generations):
            # early exit if we hit threshold
            if best.fitness() >= self._threshold:
                return best
            print(f'Generation {generation} Best {best.fitness()} Avg \
                  {mean(map(self._fitness_key, self._population))}')
            self._reproduce_and_replace()
            self._mutate()
            highest: C = max(self._population, key = self._fitness_key)
            if highest.fitness() > best.fitness():
                  best = highest # found a new best
        return best # best we found in _max_generations
                  