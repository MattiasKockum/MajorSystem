#!/usr/bin/env python3

# Programme écrit par Mattias Kockum
# Le 13 juillet 2020
# Le but de ce programme est de trouver les mots français correspondant à un enchaînement phonétique de mon système majeur

import os

voyelles = ["a", "e", "h", "i", "o", "u", "w", "y", "é", "ê", "è", "ë", "ä", "ö", "ô", "à", "å", "â", "î", "ï", " "] #voyelles phoniques
consonnes = {"z" : "0", "r" : "4", "t" : "1", "p" : "9", "q" : "7", "s" : "0", "d" : "1", "f" : "8", "g" : "7", "j" : "6", "k" : "7", "l" : "5", "m" : "3", "x" : "70", "c" : "7","ç" : "0", "v" : "8", "b" : "9", "n" : "2"}
consonnes_spéciales = {
	"c" : {("", "a") : "7",("", "e") : "0", ("", "h") : "6",("", "i") : "0", ("", "o") : "7", ("", "u") : "7"},
	"t" : {("", "ie") : "0", ("", "ion") : "0", ("", " ") : "", ("", "s ") : ""},
	"g" : {("", "a") : "7", ("", "e") : "6", ("", "i") : "6", ("", "o") : "7", ("", "u") : "7", ("", "y") : "6"},
	"n" : {("", "t") : "", ("a", "ce") : "", ("", " ") : "", ("", "s ") : "", ("", "d") : "", ("", "t") : ""},
	"p" : {("", "h") : "8"},
	"r" : {("e", " ") : ""},
	"s" : {("", " ") : ""},
	"l" : {("ouil", "e") : "", ("oui", "le") : "", ("ei", "l") : "", ("eil", "") : "", ("ei", "") : ""},
	"d" : {("", " ") : "", ("", "s ") : ""},
	"x" : {},
	"m" : {("", "p") : "", ("", "b") : ""}
	}


lettres = [i for i in voyelles] + [i for i in consonnes]
for i in lettres:
	consonnes_spéciales["x"][(i, " ")] = "" # x muet à la fin des mots

consonnes_spéciales["x"][("e", " ")] = "70" # sauf à la fin des mots en ex comme index

"""
("", " ") : "", ("", "s ") : "" correspond à une lettre muette à la fin d'un mot
"""


def phonétique(mot):
	"""
	On rentre un mot (string) et on renvoie sa prononciation phonétique en français (approximative et à vérifier, le français c'est chaud)
	"""
	prononciation = [""]
	mot = formatage(mot)
	for i,j in enumerate(mot):
		#print(prononciation)
		if j in voyelles:
			prononciation.append("")
		elif consonnes[j] == prononciation[-1]:
			# cas des doubles lettres
			pass
		elif j in consonnes_spéciales:
			spécialité = False
			for diphtongue in consonnes_spéciales[j]:
				if mot[i+1: i+1+len(diphtongue[1])] == diphtongue[1] and mot[i-len(diphtongue[0]): i] == diphtongue[0]:
					prononciation.append(consonnes_spéciales[j][diphtongue])
					spécialité = True
					break
			if not spécialité:
				prononciation.append(consonnes[j])
		elif j in consonnes:
			prononciation.append(consonnes[j])
	vide = True
	for i in prononciation:
		if i != "":
			vide = False
			break
	if vide:
		return(-1)
	return(int("".join(prononciation)))


def formatage(mot):
	# Transformation du mot de manière lisible => arc-en-ciel -> arc en ciel
	mot_formatté = ""
	mot = mot.lower()
	for i in mot:
		if i in lettres:
			mot_formatté += i
		else:
			mot_formatté += " "
	mot_formatté += " " # espace signifie la fin du mot
	return(mot_formatté)


def dico_liste():
	f = open("fr.txt")
	r = [i[:-1] for i in f]
	f.close()

	Dico_mémoire = {}
	Liste_mémoire = []

	for i in r:
		phon = phonétique(i)
		if phon in Liste_mémoire:
			Dico_mémoire[phon].append(i)
		else:
			Dico_mémoire[phon] = [i]
			Liste_mémoire.append(phon)
	return(Dico_mémoire, Liste_mémoire)



def main():
	print("Chargement du dictionnaire...")

	Dico_mémoire, Liste_mémoire = dico_liste()

	os.system('cls' if os.name == 'nt' else 'clear')
	while True:
		entrée = input("Quel chiffre vous interesse ?   (Q pour quitter)\n>>>")
		nombre = -1
		if entrée.lower() == "q":
			break
		else:
			try:
				nombre = int(entrée)
			except:
				pass
		os.system('cls' if os.name == 'nt' else 'clear')
		if nombre not in Liste_mémoire:
			print("Je ne connais pas mot correspondant, désolé...")
		else:
			for i in Dico_mémoire[nombre]:
				print(i)
			print("\n")
		if nombre == -1:
			print("(Voilà où sont rangés les mots du dictionnaire qui ne servent pas pour ce système, bien joué pour les avoir trouvé !)\n")

if __name__ == '__main__':
	main()
