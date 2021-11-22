import sys
# le-am declarat global pentru ca imi trebuie la verificarea cuvintelor
# si imi e mai usor asa decat sa le returnez pe toate intr-o lista
initial_state = []
final_state = []
tr = dict()
states = []
sigma = []
epsilon = ''

# verific daca e stare initiala sau finala
# daca mai am deja o stare initiala inseamna ca nu e valid
def state_type(x, y, init, fin):
    if y == 'S':
        if len(init):
            return 1
        init.append(x)
    else:
        fin.append(x)
    return 0


def validation():
    f = open(sys.argv[1], "r")
    transitions = []
    # citesc fiecare linie si verific daca incepe vreo sectiune
    for line in f:
        line = line.rstrip('\n')
        if line == 'Sigma:':
            arr = f.readline().rstrip('\n')
            while arr != 'End':
                arr = arr.strip()
                # verific daca arr e cometariu si ca arr nu e o linie goala
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
                    if len(arr) > 1:   # dupa stare poate sa apara F sau S, daca da, verific tipul
                        # daca am returnat 1, inseamna ca sunt mai multe stari initiale in input
                        if state_type(arr[0], arr[1], initial_state, final_state) == 1:
                            return False
                        if len(arr) > 2:
                            if state_type(arr[0], arr[2], initial_state, final_state) == 1:
                                return False
                arr = f.readline().rstrip('\n')

        if line == 'Transitions:':
            arr = f.readline().rstrip('\n')
            while arr != 'End':
                arr = arr.strip()
                if len(arr) and arr[0] != '#':
                    arr = arr.split(',')
                    transitions.append(arr)
                arr = f.readline().rstrip('\n')

    f.close()

    # tr e un dictionar de dictionare in care retin fiecare muchie
    for st in states:
        tr[st] = dict()

    # fiecare stare are dictionarul ei in tr, cu muchiile care pleaca din ea
    for x in transitions:
        # verific daca starile si litera sunt valide
        if x[0] not in states or x[1] not in sigma or x[2] not in states:
            if epsilon == '':
                epsilon = x[1]
            else:
                return False
        # verific daca mai exista tranzitie prin x[1], daca nu, initializez tr[x[0]][x[1]] cu [] pentru a adauga tranzitii
        if x[1] not in tr[x[0]].keys():
            tr[x[0]][x[1]] = []
        tr[x[0]][x[1]].append(x[2])

    return True

if validation():
    dfa_states = []
    dfa_states.append(initial_state)
    dfa_initial_state = initial_state[0]
    dfa_tr = dict()
    dfa_final_states = []
    len_states = len(dfa_states)
    i = 0
    while i < len_states:
        dfa_tr[''.join(dfa_states[i])] = dict()
        for let in sigma:
            x = set()
            for st in dfa_states[i]:
                if let in tr[st].keys():
                    x.update(tr[st][let])

            if len(x) != 0:
                x = sorted(x)
                dfa_tr[''.join(dfa_states[i])][let] = ''.join(x)
                if(x not in dfa_states):
                    dfa_states.append(x)
                    if set(x) & set(final_state):
                        dfa_final_states.append(''.join(x))

        len_states = len(dfa_states)
        i += 1

    for i in range(len(dfa_states)):
        dfa_states[i] = ''.join(dfa_states[i])

    print("DFA States: ",dfa_states)
    print("DFA Initial State: ",dfa_initial_state)
    print("DFA Final State: ",dfa_final_states)
    print("DFA: ",dfa_tr)

else:
    print("NFA-ul initial nu este valid.")