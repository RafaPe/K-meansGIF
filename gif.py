import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import random
from PIL import Image
import os

class Point:
  def __init__(self, coor, centroid):
    self.coor = coor
    self.centroid = centroid

def euclidean(a,b):
    dif = a - b
    return np.sqrt((dif**2).sum())

def new_centroid(points):
    x = 0
    y = 0
    for point in points:
        x = x + point[0]
        y = y + point[1]
    x = x/len(points)
    y = y/len(points)
    centroid = [x,y]
    # print(points)
    return centroid

def plot_points_centroids(points, centroids):
    colors = ['r','b','y','m','y','k','b','c']
    index = 0
    for centroid in centroids:
        plt.plot(centroid[0],centroid[1], marker = '+', linewidth = 0, color = colors[index], markersize=15)
        index = index + 1
    
    new_points = []
    for point in points:
        p = Point(point, [0,0])
        i = 0
        max_distancia = float('inf')
        for centroid in centroids:
            distancia = euclidean(np.array(point),np.array(centroid))
            if distancia < max_distancia:
                max_distancia = distancia
                color = i
                p.centroid = centroid
                # aux_centroid = centroid
            i = i + 1
        plt.plot(point[0],point[1], marker = '.', linewidth = 0, color = colors[color], markersize = 10)
        new_points.append(p)
    # plt.show()
    
    return new_points
    
def generate_initial_centroids(points, k):
    no_centroids = k
    min_p = points.min()
    max_p = points.max()

    centroids = []
    for _ in range(no_centroids):
        x = random.uniform(min_p,max_p)
        y = random.uniform(min_p,max_p)
        centroid = [x,y]
        centroids.append(centroid)

    return centroids

def k_means(points, k, max_iter):
    centroids = generate_initial_centroids(points, k)
    new_points = plot_points_centroids(points, centroids)
    ims = []
    name = "initial.png"
    plt.savefig(name)
    im = Image.open(name)
    ims.append(im)
    plt.clf()

    for i in range(max_iter):
        clusters = []
        for centroid in centroids:
            cluster = []
            for p in new_points:
                if p.centroid == centroid:
                    cluster.append(p.coor)
            clusters.append(cluster)

        j = 0
        aux_centroids = []
        for cluster in clusters:
            if len(cluster) == 0:
                aux_centroids.append(centroids[j])
            else:
                aux_centroids.append(new_centroid(cluster))
            j = j + 1
        
        centroids = aux_centroids
        new_points = plot_points_centroids(points, centroids)

        name = "iter_no" + str(i) + ".png"
        plt.savefig(name)
        im = Image.open(name)
        ims.append(im)
        plt.clf()
        # plt.show()
    ims[0].save('k_means.gif', save_all=True, append_images=ims[1:], optimize=False, duration=1100, loop=0)
    path = os.getcwd() 
    for filename in os.listdir(path):
        if filename.endswith('.png'):
            os.remove(filename) 



if __name__ == "__main__": 
    points = np.array([[-6,17],[-10,13],[-6,9],[-2,13],[-3,0],[1,4],[5,0],[1,-4],[6,11],[10,15],[14,11],[10,7],[15,7],[9,10],[-4,10],[5,1],[7,0],[2,1],[-6,20],[-10,15],[-7,-3],[15,15]])
    k_means(points, 3, 7)