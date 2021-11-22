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


def verif_word(word):
    st = set(initial_state)
    nxt = set()
    for let in word:
        # adaug tranzitiile realizate prin epsilon, cuvantul vid
        len_st = len(st)
        while len_st != 0:
            for a in st:
                if epsilon in tr[a].keys():
                    set.update(tr[a][epsilon])
            # daca sunt egale, inseamna ca nu a fost adaugata nici o stare
            if len(st) == len_st:
                len_st = 0
            else:
                len_st = len(st)
        # dupa ce am adauga toate starile epsilon, in nxt punem starile in care ajungem prin litera la care suntem in cuvant,
        # din starile din st
        for x in st:
            if let in tr[x].keys():
                nxt.update(tr[x][let])
        # daca nu avem nimic in nxt, inseamna ca nu am ajuns in nici o stare, deci nu putem continua
        if len(nxt) == 0:
            return False
        st = nxt
        nxt = set()

    return len(st.intersection(final_state)) != 0

if validation():
    print("NFA Valid")
else:
    print("NFA Invalid")


if verif_word(sys.argv[2]):
    print("Word Accepted")
else:
    print("Word Rejected")