# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 11:28:23 2018

@authors:   Romain Garnier
            Théo Godefroy
"""

import random

#Calcule la distance de Levenshtein entre deux objets
def distLevenshtein(pobj1, pobj2): 
    
    cost = 0
    
    mat = initMatrice(len(pobj1)+1)
    for i in range(0, len(pobj1)+1):
        mat[i][0] = i
    for j in range(0, len(pobj2)+1):
        mat[0][j] = j
        
    for i in range(1, len(pobj1)+1):
        for j in range(1, len(pobj2)+1):
            if pobj1[i-1] == pobj2[j-1]:
                cost = 0
            else:
                cost = 1
            
            mat[i][j] = min(mat[i-1][j]+1, mat[i][j-1]+1, mat[i-1][j-1]+cost)
        
    return mat[len(pobj1)][len(pobj1)]
    



#initialise une matrice carrée de dimension pdim pour calculer la distance de Levenshtein
def initMatrice(pdim):
    mat = []
    for i in range(pdim):
        mat.append([])
        for j in range(pdim):
            mat[i].append(0)
    return mat
        
#Retourne deux clusters à partir des deux centroid passés en paramètres
def cluster(pcentroid1, pcentroid2, pdata):
    cluster1 = []
    cluster2 = [] 
    
    for i in pdata:
        dist1 = distLevenshtein(pcentroid1, i)
        dist2 = distLevenshtein(pcentroid2, i)
        if dist1 < dist2:
            cluster1.append(i)
        elif dist1 > dist2:
            cluster2.append(i)
        else:
            rand = random.randint(0, 5)
            if rand%2 == 0:
                cluster1.append(i)
            else:
                cluster2.append(i)
                
    return cluster1, cluster2

#Retourne le centroid du cluster passé en paramètre
def centroid(pcluster, pfrequence):
    centroid = ""
    frequence_centroid = frequence(pcluster)
    
    for i in range(32):
        if pfrequence[i] < frequence_centroid[i]:
            centroid += "1"
        else:
            centroid += "0"
    return plusProche(centroid, pcluster)

#Retourne l'objet appartenant au cluster le plus proche de l'objet passé en paramètre
def plusProche(pobjet, pcluster):
    dist_min = 5000
    centroid = pcluster[0]
    for i in pcluster:
        dist = distLevenshtein(pobjet, i)
        if i != pobjet and dist < dist_min:
            dist_min = dist
            centroid = i
    return centroid

#Retourne la liste des fréquences de chacun des caractères dans les données passées en paramètre
def frequence(pdata):
    frequence = [0 for i in range(32)]
    
    for i in pdata:
        for j in range(32):
            frequence[j] += int(i[j])
    
    for i in range(32):
        frequence[i] /= len(pdata)
    
    return frequence

#fonction principale
def main():
    #récupération des données et passage en binaire
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
    
    #Récupération de la fréquence de chaque caratère
    frequenceL = frequence(data)
    
    #initialisation des centroid
    centroid1 = plusProche("00000000000000001111111111111111", data)
    centroid2 = plusProche("11111111111111110000000000000000", data)
    
    #boucle
    #Calcul des nouveaux clusters et mise à jour des centroids
    for i in range(1):
        cluster1, cluster2 = cluster(centroid1, centroid2, data)
    
        centroid1 = centroid(cluster1, frequenceL)
        centroid2 = centroid(cluster2, frequenceL)
    
    
    #Calcul du nombre de malware dans le premier cluster
    count = 0    
    for i in cluster1:
        if i in data_sol:
            count += 1
    
    
    #Affichage des résultats
    print("[Cluster1] : Taille : " + str(len(cluster1)))
    print("[Cluster1] : Nb Malware : " + str(count))
    print("[Cluster1] : % Malware : " + str(100*count/len(data_sol)))
    print("[Cluster1] : Rapport Malware/Sain : " + str(count/(len(cluster1)-count)))
    
    print("")
    
    print("[Cluster2] : Taille : " + str(len(cluster2)))
    print("[Cluster2] : Nb Malware : " + str(len(data_sol) - count))
    print("[Cluster2] : % Malware : " + str(100*(len(data_sol) - count)/len(data_sol)))
    print("[Cluster2] : Rapport Malware/Sain : " + str((len(data_sol) - count)/(len(cluster2)-(len(data_sol) - count)))) 


main()