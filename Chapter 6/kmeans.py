from __future__ import annotations
from typing import TypeVar, Generic, List, Sequence
from copy import deepcopy
from functools import partial
from random import uniform
from statistics import mean, pstdev
from dataclasses import dataclass
from data_point import DataPoint


def zscores(original: Sequence[float]) -> List[float]:
    avg: float = mean(original)
    std: float = pstdev(original)
    if std == 0:  # return all zeros if ther is no variation
        return [0] * len(original)
    return [(x - avg) / std for x in original]


Point = TypeVar("Point", bound=DataPoint)


class KMeans(Generic[Point]):
    @dataclass
    class Cluster:
        points: List[Point]
        centroid: DataPoint

    def __init__(self, k: int, points: List[Point]) -> None:
        if k < 1:  # k-means can't do negative or zero clusters
            raise ValueError
        self._points: List[Point] = points
        self._zscore_normalize()  # defined below
        # initialise empty clusters with random centroids
        self._clusters: List[KMeans.Cluster] = []
        for _ in range(k):
            rand_point: DataPoint = self._random_point()  # defined below
            # assign centroid to a Cluster class variable
            cluster: KMeans.Cluster = KMeans.Cluster([], rand_point)
            # add to ._clusters list
            self._clusters.append(cluster)

    @property
    def _centroids(self) -> List[DataPoint]:
        return [x.centroid for x in self._clusters]

    # a method that returns a list of values of one dimension/field of
    # every datapoint
    def _dimension_slice(self, dimension: int) -> List[float]:
        return [x.dimensions[dimension] for x in self._points]

    #  method to replace the values in dimensions with their z-scores
    #  equivalent
    def _zscore_normalize(self) -> None:
        # create temp list zscored
        zscored: List[List[float]] = [[] for _ in range(len(self._points))]
        # .num_dimensions is a property of DataPoint class
        for dimension in range(self._points[0].num_dimensions):
            # get the list of values for the dimension
            dimension_slice: List[float] = self._dimension_slice(dimension)
            for index, zscore in enumerate(zscores(dimension_slice)):
                zscored[index].append(zscore)
        for i in range(len(self._points)):
            # update the .dimensions part of each datapoint with
            # values in zscored
            self._points[i].dimensions = tuple(zscored[i])

    def _random_point(self) -> DataPoint:
        # empty list to hold the dimensions of the random point, which
        # this method will return
        rand_dimensions: List[float] = []
        # .num_dimensions is a property of DataPoint class
        for dimension in range(self._points[0].num_dimensions):
            # get the list of values for the dimension
            values: List[float] = self._dimension_slice(dimension)
            # calculate a random value that's within the bound of values
            rand_value: float = uniform(min(values), max(values))
            rand_dimensions.append(rand_value)
        return DataPoint(rand_dimensions)

    # Find the closest cluster centroid to each point and assign the point to
    # that cluster
    def _assign_clusters(self) -> None:
        for point in self._points:
            # partial() takes a function and provides it with some of its parameters
            #  before the function is applied. In this case, we supply the
            # DataPoint.distance() method with the point we are calculating from as
            # its other parameter. This will result in each centroid’s distance to
            # the point being computed and the lowest-distance centroid’s being returned by min().
            closest: DataPoint = min(
                self._centroids, key=partial(DataPoint.distance, point)
            )
            idx: int = self._centroids.index(closest)
            cluster: KMeans.Cluster = self._clusters[idx]
            cluster.points.append(point)

    def _generate_centroids(self) -> None:
        for cluster in self._clusters:
            if len(cluster.points) == 0:  # keep the same centroid if no points
                continue
            means: List[float] = []
            for dimension in range(cluster.points[0].num_dimensions):
                dimension_slice: List[float] = [
                    p.dimensions[dimension] for p in cluster.points
                ]
                # add the mean of a particular dimension to the means list
                means.append(mean(dimension_slice))
            # the means list is now new centroid of the cluster
            cluster.centroid = DataPoint(means)

    def run(self, max_iterations: int = 100) -> List(KMeans.Cluster):
        for iteration in range(max_iterations):
            for cluster in self._clusters:
                # clear all clusters, KMeans.Cluster.points is a list - can use .clear()
                cluster.points.clear()
            self._assign_clusters()  # find cluster each point is closest to
            old_centroids: List[DataPoint] = deepcopy(self._centroids)  # record
            self._generate_centroids()  # find new centroids
            if old_centroids == self._centroids:  # have centroids moved?
                print(f"Converged after {iteration} iterations")
                return self._clusters
        return self._clusters


if __name__ == "__main__":
    point1: DataPoint = DataPoint([2.0, 1.0, 1.0])
    point2: DataPoint = DataPoint([2.0, 2.0, 5.0])
    point3: DataPoint = DataPoint([3.0, 1.5, 2.5])
    kmeans_test: KMeans[DataPoint] = KMeans(2, [point1, point2, point3])
    test_clusters: List[KMeans.Cluster] = kmeans_test.run()
    for index, cluster in enumerate(test_clusters):
        print(f"Cluster {index}: {cluster.points}")
"""
Expected Output:

Converged after 1 iterations
Cluster 0: [(2.0, 1.0, 1.0), (3.0, 1.5, 2.5)]
Cluster 1: [(2.0, 2.0, 5.0)]
"""
