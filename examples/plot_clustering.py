"""
Clustering
==========

In this example, the use of the clustering plot methods is shown applied to the
Canadian Weather dataset. K-Means and Fuzzy K-Means algorithms are employed to
calculate the results plotted.
"""

# Author: Amanda Hernando Bernabé
# License: MIT

# sphinx_gallery_thumbnail_number = 6

import matplotlib.pyplot as plt
import numpy as np
from skfda import datasets
from skfda.exploratory.visualization.clustering import (
    plot_clusters, plot_cluster_lines, plot_cluster_bars)
from skfda.ml.clustering import KMeans, FuzzyKMeans


##############################################################################
# First, the Canadian Weather dataset is downloaded from the package 'fda' in
# CRAN. It contains a FDataGrid with daily temperatures and precipitations,
# that is, it has a 2-dimensional image. We are interested only in the daily
# average temperatures, so we select the first coordinate function.
dataset = datasets.fetch_weather()
fd = dataset["data"]
fd_temperatures = fd.coordinates[0]

# The desired FDataGrid only contains 10 random samples, so that the example
# provides clearer plots.
indices_samples = np.array([1, 3, 5, 10, 14, 17, 21, 25, 27, 30])
fd = fd_temperatures[indices_samples]

##############################################################################
# The data is plotted to show the curves we are working with. They are divided
# according to the target. In this case, it includes the different climates to
# which the weather stations belong to.

climate_by_sample = [dataset["target"][i] for i in indices_samples]

# Note that the samples chosen belong to three of the four possible target
# groups. By coincidence, these three groups correspond to indices 1, 2, 3,
# that is why the indices (´climate_by_sample´) are decremented in 1. In case
# of reproducing the example with other ´indices_samples´ and the four groups
# are not present in the sample, changes should be made in order ´indexer´
# contains numbers in the interval [0, n_target_groups) and at least, an
# occurrence of each one.
indexer = np.asarray(climate_by_sample) - 1

indices_target_groups = np.unique(climate_by_sample)
climates = dataset["target_names"][indices_target_groups]

# Assigning the color to each of the groups.
colormap = plt.cm.get_cmap('tab20b')
n_climates = len(climates)
climate_colors = colormap(np.arange(n_climates) / (n_climates - 1))

fd.plot(group=indexer, group_colors=climate_colors,
        group_names=climates)

##############################################################################
# The number of clusters is set with the number of climates, in order to see
# the performance of the clustering methods, and the seed is set to one in
# order to obatain always the same result for the example.

n_clusters = n_climates
seed = 2

##############################################################################
# First, the class :class:`~skfda.ml.clustering.KMeans` is instantiated with
# the desired. parameters. Its :func:`~skfda.ml.clustering.KMeans.fit` method
# is called, resulting in the calculation of several attributes which include
# among others, the the number of cluster each sample belongs to (labels), and
# the centroids of each cluster. The labels are obtaiined calling the method
# :func:`~skfda.ml.clustering.KMeans.predict`.

kmeans = KMeans(n_clusters=n_clusters, random_state=seed)
kmeans.fit(fd)
print(kmeans.predict(fd))

##############################################################################
# To see the information in a graphic way, the method
# :func:`~skfda.exploratory.visualization.clustering_plots.plot_clusters` can
# be used.

# Customization of cluster colors and labels in order to match the first image
# of raw data.
cluster_colors = climate_colors[np.array([0, 2, 1])]
cluster_labels = climates[np.array([0, 2, 1])]

plot_clusters(kmeans, fd, cluster_colors=cluster_colors,
              cluster_labels=cluster_labels)

##############################################################################
# Other clustering algorithm implemented is the Fuzzy K-Means found in the
# class :class:`~skfda.ml.clustering.FuzzyKMeans`. Following the
# above procedure, an object of this type is instantiated  with the desired
# data and then, the
# :func:`~skfda.ml.clustering.FuzzyKMeans.fit` method is called.
# Internally, the attribute ``labels_`` is calculated, which contains
# ´n_clusters´ elements for each sample and dimension, denoting the degree of
# membership of each sample to each cluster. They are obtained calling the
# method :func:`~skfda.ml.clustering.FuzzyKMeans.predict`. Also, the centroids
# of each cluster are obtained.

fuzzy_kmeans = FuzzyKMeans(n_clusters=n_clusters, random_state=seed)
fuzzy_kmeans.fit(fd)
print(fuzzy_kmeans.predict(fd))

##############################################################################
# To see the information in a graphic way, the method
# :func:`~skfda.exploratory.visualization.clustering_plots.plot_clusters` can
# be used. It assigns each sample to the cluster whose membership value is the
# greatest.

plot_clusters(fuzzy_kmeans, fd, cluster_colors=cluster_colors,
              cluster_labels=cluster_labels)

##############################################################################
# Another plot implemented to show the results in the class
# :class:`~skfda.ml.clustering.FuzzyKMeans` is
# :func:`~skfda.exploratory.visualization.clustering_plots.plot_cluster_lines`
# which is similar to parallel coordinates. It is recommended to assign colors
# to each of the samples in order to identify them. In this example, the
# colors are the ones of the first plot, dividing the samples by climate.

colors_by_climate = colormap(indexer / (n_climates - 1))

plot_cluster_lines(fuzzy_kmeans, fd, cluster_labels=cluster_labels,
                   sample_colors=colors_by_climate)

##############################################################################
# Finally, the function
# :func:`~skfda.exploratory.visualization.clustering_plots.plot_cluster_bars`
# returns a barplot. Each sample is designated with a bar which is filled
# proportionally to the membership values with the color of each cluster.

plot_cluster_bars(fuzzy_kmeans, fd, cluster_colors=cluster_colors,
                  cluster_labels=cluster_labels)

##############################################################################
# The possibility of sorting the bars according to a cluster is given
# specifying the number of cluster, which belongs to the interval
# [0, n_clusters).
#
# We can order the data using the first cluster:
plot_cluster_bars(fuzzy_kmeans, fd, sort=0, cluster_colors=cluster_colors,
                  cluster_labels=cluster_labels)

##############################################################################
# Using the second cluster:
plot_cluster_bars(fuzzy_kmeans, fd, sort=1, cluster_colors=cluster_colors,
                  cluster_labels=cluster_labels)

##############################################################################
# And using the third cluster:
plot_cluster_bars(fuzzy_kmeans, fd, sort=2, cluster_colors=cluster_colors,
                  cluster_labels=cluster_labels)
