def f(x):
    return x * 2


def trouve(p, t):
    if not p:
        return None
    elif p(t[0]):
        return t[0]
    else:
        trouve(p, t[1:])


def trouve_2(p, t):
    match t:
        case []:
            return None
        case [x, *elts]:
            if p(x):
                return x
            else:
                return trouve_2(p, [*elts])



def tri_insertion(t, inf):
    for i in range(1, len(t)):
        v = t[i]
        j = i
        while j > 0 and not inf(t[j - 1], v):
            t[j] = t[j - 1]
            j = j - 1
        t[j] = v


def queue(liste):
    return liste[1:]


def tete(liste):
    return liste[0]


def insere(v, t):
    if t == [] or v <= tete(t):
        return [v] + t
    else:
        return [tete(t)] + insere(v, queue(t))


def tri_insertion_2(t):
    if not t:
        return []
    else:
        return insere(tete(t), tri_insertion_2(queue(t)))


def tri_insertion_3(t, inf):
    def insere_3(v, t):
        if t == [] or inf(v, tete(t)):
            return [v] + t
        else:
            return [tete(t)] + insere(v, queue(t))

    if not t:
        return []
    else:
        return insere_3(tete(t), tri_insertion_3(queue(t), inf))


def double(f):
    return lambda x: f(f(x))


def compose(f, g):
    return lambda x: f(g(x))


def triple(t):
    return list(map(lambda x: 3 * x, t))


def maj_min(t):
    return list(map(lambda x: (x.upper(), x.lower()), t))


def plus_petit_plus_grand(t, n):
    return list(filter(lambda x: x < n, t)), list(filter(lambda x: x >= n, t))


def partition(p, t):
    return list(filter(lambda x: p(x), t))
