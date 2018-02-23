# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 09:04:07 2018

@author: Romain Garnier
"""

def dist(pobj1, pobj2):
    dist = 0
    for i in range(len(pobj1)):
        if pobj1[i] != pobj2[i]:
            dist += 1
    return dist

def cluster(pcentroid1, pcentroid2, pdata):
    cluster1 = []
    cluster2 = [] 
    
    for i in pdata:
        if dist(pcentroid1, i) < dist(pcentroid2, i):
            cluster1.append(i)
        else:
            cluster2.append(i)
    return cluster1, cluster2



def main():
    fichier = open("bin/jeu_tot", "r")
    data = fichier.read().split()
    fichier.close()
    
    fichier = open("bin/jeu_1", "r")
    data_sol = fichier.read().split()
    fichier.close()
    
    
    for i in range(0, len(data)):
        data[i] = str(bin(int(data[i], 16))[2:])
        while len(data[i]) < 32:
            data[i] = "0" + data[i]
    
    for i in range(0, len(data_sol)):
        data_sol[i] = str(bin(int(data_sol[i], 16))[2:])
        while len(data_sol[i]) < 32:
            data_sol[i] = "0" + data_sol[i]
            
    centroid1 = data[0]
    centroid2 = data[int(len(data)/2)]
    
    cluster1, cluster2 = cluster(centroid1, centroid2, data)
    
    
    
main()