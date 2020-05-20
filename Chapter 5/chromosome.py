from __future__ import annotations
from typing import TypeVar, Tuple, Type
from abc import ABC, abstractmethod

T = TypeVar('T', bound = 'Chromosome') # for returning self
# This means that anything that fills in a variable that is of
# type T must be an instance of Chromosome of a subclass of
# Chromosome.


# Base class for all chromosomes; all methods must be overridden
class Chromosome(ABC):
    @abstractmethod
    def fitness(self) -> float:
        ...
    
    @classmethod
    @abstractmethod
    def random_instance(cls: Type[T]) -> T:
        ...
        
    @abstractmethod
    def crossover(self: T, other: T) -> Tuple[T, T]:
        ...
        
    @abstractmethod
    def mutate(self) -> None:
        ...