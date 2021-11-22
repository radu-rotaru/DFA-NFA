import sys
# le-am declarat global pentru ca imi trebuie la verificarea cuvintelor
# si imi e mai usor asa decat sa le returnez pe toate intr-o lista
initial_state = []
final_state = []
tr = dict()


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
    sigma = []
    states = []
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
                        # daca am returnat 0, inseamna ca sunt mai multe stari initiale in input
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
            return False
        # daca starea are mai mult de o muchie reprezentata cu aceeasi litera, nu este DFA, deci nu e valid
        if x[1] in tr[x[0]].keys():
            return False
        tr[x[0]][x[1]] = x[2]

    return True


def verif_word(word):
    st = initial_state[0]
    for let in word:
        if let not in tr[st].keys():
            return False
        st = tr[st][let]

    return st in final_state


if validation():
    print("DFA Valid")
else:
    print("DFA Invalid")
