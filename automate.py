# -*- coding: utf-8 -*-

"""
LUONG Ethan - 28627904
"""

from transition import *
from state import *
import os
import copy
from itertools import product
from automateBase import AutomateBase



class Automate(AutomateBase):

    def succElem(self, state, lettre):

        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs





    def succ (self, listStates, lettre):

        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        l = []

        # On considere le successeur de chaque etat de la liste
        for state in listStates:
            # On ajoute les etats successeurs
            l += self.succElem(state, lettre)

        # On utilise la transformation en ensemble pour supprimer les doublons
        return list(set(l))





    @staticmethod
    def accepte(auto,mot) :

        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """

        # On part des etats initiaux et on stocke les etats finaux
        l = auto.getListInitialStates()
        lF = auto.getListFinalStates()

        # On determine les chemins possibles au fur et a mesure
        for lettre in mot:
            l = auto.succ(l, lettre)

        for state in lF:
            if (state in l):
                print ("L'automate accepte le mot " + mot)
                return True

        print ("L'automate n'accepte pas le mot " + mot)
        return False





    @staticmethod
    def estComplet(auto,alphabet) :

        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """

        # On tient compte de tous les etats
        l = auto.listStates

        for state in l:
            for lettre in alphabet:
                l2 = auto.succElem(state, lettre)
                # On verifie pour chaque etat et chaque lettre si un etat succede
                if (len(l2) == 0):
                    return False

        return True





    @staticmethod
    def estDeterministe(auto) :

        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """

        # On stocke la liste des etats
        lI = list(auto.getListInitialStates())
        alpha = list(auto.getAlphabetFromTransitions())

        # Si plusieurs etats initiaux : non deterministe
        if (len(lI) > 1):
            return False

        l = list(auto.listStates)

        for state in l:
            # Pour chaque etat et chaque lettre, on etablit :
            for lettre in alpha:
                # La liste des etats successeurs
                l2 = auto.succElem(state, lettre)

                if (len(l2) > 1):
                    # S'il y a plusieurs successeurs : non deterministe
                    return False

        return True





    @staticmethod
    def completeAutomate(auto,alphabet) :

        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """

        # Copie de l'automate
        copieAuto = copy.deepcopy(auto)

        # Ajout d'un etat puits
        emptyState = State(-1, False, False, "_")
        for lettre in alphabet:
            t = Transition(emptyState, lettre, emptyState)
            copieAuto.addTransition(t)

        # On dirige les transitions manquantes, vers l'etat puits
        l = auto.listStates

        for state in l:
            for lettre in alphabet:
                l2 = auto.succElem(state, lettre)
                # On verifie pour chaque etat et chaque lettre si rien ne succede
                if (len(l2) == 0):
                    # Auquel cas, on ajoute une transition vers l'etat puits
                    copieAuto.addTransition(Transition(state, lettre, emptyState))

        return copieAuto





    @staticmethod
    def determinisation(auto) :

        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """

        # Verification du cas trivial
        if (Automate.estDeterministe(auto)):
            return copy.deepcopy(auto)

        # Initialisation des variables et d'un automate vide
        detAuto = Automate([], [])
        lI = list(auto.getListInitialStates())
        alpha = list(auto.getAlphabetFromTransitions())
        l = [lI]   # Liste des etats restants a traiter
        id = 0

        # Ajout de l'etat initial
        s = State(id, True, State.isFinalIn(lI), str(set(lI)))
        id += 1
        detAuto.addState(s)

        # Tant qu'un etat doit etre traite :
        while (l):
            # On considere chaque lettre
            for lettre in alpha:
                l2 = auto.succ(l[0], lettre)
                bool = True

                # On verifie le cas ou l2 est vide
                if (l2 == []):
                    continue

                # On stocke l'etat source
                # On verifie si l'etat dest n'a pas deja ete cree
                for etat in detAuto.listStates:
                    if (etat.label == str(set(l[0]))):
                        temp = etat
                    if (etat.label == str(set(l2))):
                        s = etat
                        bool = False

                # Si necessaire, on cree l'etat dest et on l'ajoute
                if (bool):
                    s = State(id, False, State.isFinalIn(l2), str(set(l2)))
                    detAuto.addState(s)
                    id += 1
                    l.append(list(l2))

                # On ajoute la transition
                detAuto.addTransition(Transition(temp, lettre, s))

            l.pop(0)

        return detAuto





    @staticmethod
    def complementaire(auto,alphabet):

        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """

        # Partant d'un automate complet deterministe :
        cplmtAuto = Automate.determinisation(Automate.completeAutomate(auto, alphabet))

        # On fait des etats non finaux, des etats finaux ; et vice-versa
        for state in cplmtAuto.listStates:
            state.fin = not(state.fin)

        return cplmtAuto


    @staticmethod
    def intersection (auto0, auto1):

        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """

        # On verifie le cas trivial
        if (auto0.equals(auto1)):
            return auto0

        # Initialisation des variables
        lI0 = auto0.getListInitialStates()
        lI1 = auto1.getListInitialStates()

        lF0 = auto0.getListFinalStates()
        lF1 = auto1.getListFinalStates()

        ls0 = auto0.listStates
        ls1 = auto1.listStates
        lst = list(product(ls0, ls1))

        lt0 = auto0.listTransitions
        lt1 = auto1.listTransitions

        id = 0

        st = []
        tr = []

        # On parcourt toutes les transitions et tous les tuples
        for t0 in lt0:
            for t1 in lt1:
                for tup in lst:
                    # Si une transition valable a ete trouvee :
                    if ((tup[0] == t0.stateSrc) and (tup[1] == t1.stateSrc) and (t0.etiquette == t1.etiquette)):

                        bool1 = True
                        bool2 = True
                        t = (t0.stateDest, t1.stateDest)

                        # On verifie que l'etat source n'existe pas
                        for etat in st:
                            if (etat.label == str(tup)):
                                etat1 = etat
                                bool1 = False

                        # Si ce n'est pas le cas, on le cree et l'ajoute
                        if (bool1):
                            etat1 = State(id, ((tup[0] in lI0) and (tup[1] in lI1)), ((tup[0] in lF0) and (tup[1] in lF1)), str(tup))
                            st.append(etat1)
                            id += 1

                        # De meme pour l'etat dest
                        for etat in st:
                            if (etat.label == str(t)):
                                etat2 = etat
                                bool2 = False

                        if (bool2):
                            etat2 = State(id, ((t[0] in lI0) and (t[1] in lI1)), ((t[0] in lF0) and (t[1] in lF1)), str(t))
                            st.append(etat2)
                            id += 1

                        # On termine en ajoutant la transition correspondante
                        tr.append(Transition(etat1, t0.etiquette, etat2))

        return Automate(tr, st)





    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """

        """ QUESTION FACULTATIVE """

        return





    @staticmethod
    def concatenation (auto1, auto2):

        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """

        # Initialisation des variables
        st = list(auto1.listStates)
        tr = list(auto1.listTransitions)
        lI1 = list(auto1.getListInitialStates())
        lF1 = list(auto1.getListFinalStates())
        lI2 = list(auto2.getListInitialStates())
        bool = State.isFinalIn(lI1)

        # On ajoute les etats d'auto2 manquants au fur et a mesure
        # Cela permettra de pouvoir concatener le meme langage pour l'etoile
        # On definit les etats initiaux selon si le mot vide est reconnu par auto1
        # On verifie bien que les S1 et S2 sont disjoints
        for s in auto2.listStates:
            if (s not in st):
                if (not(bool)):
                    s.init = False
                st.append(s)

        # On ajoute toutes les transitions d'auto2
        for t in auto2.listTransitions:
            if (t not in tr):
                tr.append(t)

        # On ajoute les transitions de la forme (s,a,i)
        for t in auto1.listTransitions:
            if (t.stateDest in lF1):
                for i in lI2:
                    transition = Transition(t.stateSrc, t.etiquette, i)
                    # On verifie que la transition n'existe pas deja
                    # Cela sera utile pour concatener le meme langage
                    if (transition not in tr):
                        tr.append(transition)

        return Automate(tr, st)





    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """

        """ QUESTION FACULTATIVE """

        # On tire profit de la concatenation pour obtenir les transitions (s,a,i)
        etAuto = Automate.concatenation(auto, auto)

        # On ajoute un nouvel etat permettant d'accepter le mot vide
        nvState = State(-2, True, True, "j")
        etAuto.addState(nvState)

        return etAuto
