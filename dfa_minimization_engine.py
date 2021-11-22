import sys

initial_state = []
final_state = []
tr = dict()
sigma = []
states = []


# Functie ce verifica daca starea este initiala sau finala
# In cazul in care avem deja o stare finala, DFA-ul este invalid
def state_type(x, y, init, fin):
    if y == 'S':
        if len(init):
            return 1
        init.append(x)
    else:
        fin.append(x)
    return 0


# Functia care valideaza DFA-ul
def validation():
    f = open(sys.argv[1], "r")
    transitions = []

    # Citesc fiecare linie si verific daca incepe vreo sectiune
    for line in f:
        line = line.rstrip('\n')

        if line == 'Sigma:':
            arr = f.readline().rstrip('\n')
            while arr != 'End':
                arr = arr.strip()
                # Verific daca arr e cometariu si ca arr nu e o linie goala
                if len(arr) and arr[0] != '#':
                    sigma.append(arr)
                arr = f.readline().rstrip('\n')

        if line == 'States:':
            arr = f.readline().rstrip('\n')
            while arr != 'End':
                arr = arr.strip()
                if len(arr) and arr[0] != '#':
                    arr = arr.split(',')
                    states.append(arr[0])
                    # Dupa stare poate sa apara F sau S, daca apare, verific tipul
                    # Daca state_type returneaza 0, inseamna ca sunt mai multe stari initiale in input
                    if len(arr) > 1:
                        if state_type(arr[0], arr[1], initial_state, final_state) == 1:
                            return False
                        # Starea poate fi initiala si finala
                        if len(arr) > 2:
                            if state_type(arr[0], arr[2], initial_state, final_state) == 1:
                                return False

                arr = f.readline().rstrip('\n')
        # Am considerat ca forma tranzitiilor din exemplu este cea corecta, adica prima stare,
        # litera din alfabet si cea de-a doua stare sunt despartite doar de virgula
        if line == 'Transitions:':
            arr = f.readline().rstrip('\n')
            while arr != 'End':
                arr = arr.strip()
                if len(arr) and arr[0] != '#':
                    arr = arr.split(',')
                    transitions.append(arr)
                arr = f.readline().rstrip('\n')

    f.close()

    # tr este un dictionar de dictionare in care retin fiecare muchie
    for st in states:
        tr[st] = dict()

    # fiecare stare are dictionarul ei in tr, cu muchiile care pleaca din ea
    for x in transitions:
        # verific daca starile si litera sunt valide
        if x[0] not in states or x[1] not in sigma or x[2] not in states:
            return False
        # daca starea are mai mult de o muchie reprezentata cu aceeasi litera, nu este un DFA valid
        if x[1] in tr[x[0]].keys():
            return False
        tr[x[0]][x[1]] = x[2]

    return True

# daca DFA-ul este valid, il minimizez
if validation():
    # minimize_dfa reprezinta matricea triunghiulara in care sunt retiunute cuvintele prin care difera starile
    minimized_dfa = dict();
    for i in range(1, len(states)):
        minimized_dfa[states[i]] = dict()
        # O stare nefinala si una finala sunt separabile prin cuvantul vid. Am ales simbolul '@' pentru cuvantul vid
        if(states[i] not in final_state):
            for j in range(i):
                if states[j] not in final_state:
                    minimized_dfa[states[i]][states[j]] = []
                else:
                    minimized_dfa[states[i]][states[j]] = ['@']
        else:
            for j in range(i):
                if states[j] not in final_state:
                    minimized_dfa[states[i]][states[j]] = ['@']
                else:
                    minimized_dfa[states[i]][states[j]] = []

    ok = 1
    len_cuv = 1
    while(ok):
        ok = 0
        for i in range(1, len(states)):
            for j in range(i):
                # Daca cele doua stari sunt echivalente pentru cuvintele de lungime len_cuv,
                # verificam daca sunt separabile printr-un cuvant de lungime len_cuv + 1
                if len(minimized_dfa[states[i]][states[j]]) == 0:
                    for let in sigma:
                        q1 = tr[states[i]][let]
                        q2 = tr[states[j]][let]
                        # Trebuie sa interschimbam starile pentru ca matricea este triunghiulara
                        if q1 in minimized_dfa[q2].keys():
                            q1, q2 = q2, q1
                        # Daca starile sunt diferite si sunt separabile printr-un cuvant de lungime len_cuv,
                        # inseamna ca starile pe care le verificam sunt separabile printr-un cuvant de lungime
                        # len_cuv + 1
                        if q1 != q2 and len(minimized_dfa[q1][q2]) == len_cuv:
                            minimized_dfa[states[i]][states[j]].extend(minimized_dfa[q1][q2])
                            minimized_dfa[states[i]][states[j]].append(let)
                            ok = 1
                            break

        len_cuv += 1
        # Cat timp gasim pereche de stari care devine separabila, repetam

    # in minimized_dfa_states vom grupa starile in functie de echivalenta lor
    # pos va retine indicele din minimized_dfa_states in care se afla o anumita stare
    minimized_dfa_states = []
    pos = dict()
    for i in range(len(states) - 1, -1, -1):
        if states[i] not in pos.keys():
            # daca starea nu a fost inca adaugata intr-o stare din DFA-ul minimal, cream o noua stare pentru aceasta
            pos[states[i]] = len(minimized_dfa_states)
            minimized_dfa_states.append([states[i]])
        for j in range(i):
            # adaugam starile echivalente cu aceasta in starea nou creata in minimized_dfa_states
            if len(minimized_dfa[states[i]][states[j]]) == 0 and states[j] not in pos.keys():
                pos[states[j]] = pos[states[i]]
                minimized_dfa_states[pos[states[i]]].append(states[j])

    # tr_minimized retine tranzitiile DFA-ului minimal
    tr_minimized = dict()

    # pentru dictionarul tranzitiilor pun noul nume al starilor, concatenez toate starile din DFA-ul
    # initial care formeaza noua stare. Nu salvez modificarile in minimized_dfa_states pentru ca
    # trebuie sa am acces si la tranzitiile din DFA-ul initial
    for x in minimized_dfa_states:
        tr_minimized[''.join(x)] = dict()
        for let in sigma:
            tr_minimized[''.join(x)][let] = ''.join(minimized_dfa_states[pos[tr[x[0]][let]]])

    # dupa ce am terminat tranzitiile, retin si in minimize_dfa_states noul nume al starilor
    for i in range(len(minimized_dfa_states)):
        minimized_dfa_states[i] = ''.join(minimized_dfa_states[i])

    # starea initiala a DFA-ului minimal este aceea in care se afla starea initiala din DFA-ul dat
    minimized_start = minimized_dfa_states[pos[initial_state[0]]]
    # toate starile in care se afla o stare finala din DFA-ul initial sunt stari finale in DFA-ul minimal
    minimized_final = []
    minimized_final = [minimized_dfa_states[pos[x]] for x in final_state if minimized_dfa_states[pos[x]] not in minimized_final]

    # afisez DFA-ul minimal
    print("Minimized DFA states: ", minimized_dfa_states)
    print("Minimized DFA start: ",minimized_start)
    print("Minimized DFA final: ",minimized_final)
    print("Minimized DFA: ", tr_minimized)