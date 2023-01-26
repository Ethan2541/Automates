# -*- coding: utf-8 -*-
"""
Code modifiable.
"""

from automate import Automate
from state import State
from transition import Transition
from myparser import *
import os


""" Code donne en exemple
automate = Automate.creationAutomate("exempleAutomate.txt")
automate.show("exempleAutomate")

s1= State(1, False, False)
s2= State(2, False, False)
print (s1==s2)
print (s1!=s2)
"""






""" Creation de l'automate auto """

""" Etats """
s0 = State(0, True, False)
s1 = State(1, False, False)
s2 = State(2, False, True)

""" Transitions """
t1 = Transition(s0, "a", s0)
t2 = Transition(s0, "b", s1)
t3 = Transition(s1, "a", s2)
t4 = Transition(s1, "b", s2)
t5 = Transition(s2, "a", s0)
t6 = Transition(s2, "b", s1)

""" Affichage """
auto = Automate([t1, t2, t3, t4, t5, t6])
print(auto)
auto.show("A_ListeTrans")





""" Creation de l'automate auto1 """

""" On conserve les etats et transitions precedents """
auto1 = Automate([t1, t2, t3, t4, t5, t6], [s0, s1, s2])
print(auto1)
auto1.show("A1_ListeTrans")

assert(auto1.equals(auto))





""" Creation de l'automate auto2 """

""" La creation se fait a partir du fichier texte auto """
auto2 = Automate.creationAutomate("auto.txt")
print(auto2)
auto2.show("A2_ListeTrans")

assert(auto2.equals(auto))





""" Manipulations sur les transitions """

""" Suppression d'une transition """
t = Transition(s0, "a", s1)
auto.removeTransition(t)
print(auto)

""" Ajout d'une transition """
auto.addTransition(t)
print(auto)
auto.show("A3_ListeTrans")





""" Manipulations sur les etats """

""" Suppression d'un etat """
auto.removeState(s1)
print(auto)

""" Ajout d'un etat """
auto.addState(s1)
print(auto)

s2 = State(0, True, False)
auto.addState(s2)
print(auto)
auto.show("A4_ListeTrans")





""" Liste des transitions """

print(auto1.getListTransitionsFrom(s1))





""" Test des fonctions """

st1 = State(1, True, False)
st2 = State(2, False, True)
st3 = State(3, False, False)
st4 = State(4, False, False)

tr1 = Transition(st1, "a", st1)
tr2 = Transition(st1, "a", st3)
tr3 = Transition(st1, "b", st2)
tr4 = Transition(st2, "b", st1)
tr5 = Transition(st3, "b", st2)
tr6 = Transition(st3, "a", st4)
tr7 = Transition(st4, "a", st4)
tr8 = Transition(st4, "b", st2)
tr9 = Transition(st2, "b", st4)

auto01 = Automate([tr1, tr2, tr3, tr4, tr5, tr6, tr7, tr8, tr9], [st1, st2, st3, st4])
# auto02 = Automate([tr5, tr6, tr7, tr8], [st3, st4])

print(Automate.accepte(auto01, "aaaaab"))
