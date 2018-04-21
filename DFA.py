from collections import defaultdict
from functools import reduce
import pygraphviz as pgv
import prettytable


class FA:
    def __init__(self, Q, Σ, δ_dict, q_0, F):
        self.Q = Q
        self.Σ = Σ
        self.δ_dict = δ_dict
        self.q_0 = q_0
        self.F = F
        self.extra = set()

    def δ(self, q, a):
        return self.δ_dict[q][a]

    def __str__(self):
        desc = prettytable.PrettyTable(['Parameter', 'Value'])
        desc.add_row(["Q", "{%s}" % ', '.join(str(q) for q in self.Q)])
        desc.add_row(["Σ", "{%s}" % ', '.join(self.Σ)])
        desc.add_row(["q_0", str(self.q_0)])
        desc.add_row(["F", "{%s}" % ', '.join(str(f) for f in self.F)])
        if self.extra:
            desc.add_row(["Extra Symbols", self.extra])
        delta = prettytable.PrettyTable(['δ'] + list(self.Σ.union(self.extra)))
        for q in self.Q:
            delta.add_row([q] + [self.δ(q, a) for a in self.Σ.union(self.extra)])
        desc.add_row(["δ", str(delta)])
        return str(desc)


class DFA(FA):
    def __init__(self, Q, Σ, δ_dict, q_0, F):
        '''assert set(δ_dict.keys()).intersection(Q) == Q
        assert all(
            set(δ_dict[d].keys()).intersection(Σ) == Σ
            and all(x in Q for x in δ_dict[d].values())
            for d in δ_dict)
        assert q_0 in Q
        assert F <= Q  # Subset or Equal'''
        FA.__init__(self, Q, Σ, δ_dict, q_0, F)

    def rename(self, start=0):
        rename_dict = dict(zip(self.Q, {'q%s' % (start + i) for i in range(len(self.Q))}))

        def rename_func(x):
            return rename_dict[x]

        Q = set(map(rename_func, self.Q))
        q_0 = rename_func(self.q_0)
        F = set(map(rename_func, self.F))
        new_delta = defaultdict(dict)
        for q, A in self.δ_dict.items():
            for a in A:
                new_delta[rename_func(q)][a] = rename_func(self.δ_dict[q][a])
        return DFA(Q, self.Σ, new_delta, q_0, F)

    def is_accepted(self, w):
        try:
            return reduce(self.δ, w, self.q_0) in self.F
        except KeyError:
            return False

    def draw(self, filename, prog='dot', format='png'):
        G = pgv.AGraph(directed=True, rankdir='LR')
        G.add_node('qi', shape='point')
        for q in self.Q:
            G.add_node(q, shape='oval', peripheries=2 if q in self.F else 1)
        G.add_edge('qi', self.q_0, label='start')
        for u in self.δ_dict:
            for a, v in self.δ_dict[u].items():
                label = G.get_edge(u, v).attr['label'] + ',' + a if G.has_edge(u, v) else a
                G.add_edge(u, v, label=label)
        G.draw(filename, format=format, prog=prog)

    def union(self, M):
        assert self.Σ == M.Σ
        Q = {(x, y) for x in self.Q for y in M.Q}
        delta_dict = {(x, y): {a: (self.δ(x, a), M.δ(y, a)) for a in self.Σ} for (x, y) in Q}
        F = {(x, y) for x in self.Q for y in M.Q if x in self.F or y in M.F}
        return DFA(Q, self.Σ, delta_dict, (self.q_0, M.q_0), F)

    def intersection(self, M):
        assert self.Σ == M.Σ
        Q = {(x, y) for x in self.Q for y in M.Q}
        delta_dict = {(x, y): {a: (self.δ(x, a), M.δ(y, a)) for a in self.Σ} for (x, y) in Q}
        F = {(x, y) for x in self.F for y in M.F}
        return DFA(Q, self.Σ, delta_dict, (self.q_0, M.q_0), F)

    def difference(self, M):
        assert self.Σ == M.Σ
        Q = {(x, y) for x in self.Q for y in M.Q}
        delta_dict = {(x, y): {a: (self.δ(x, a), M.δ(y, a)) for a in self.Σ} for (x, y) in Q}
        F = {(x, y) for x in self.F for y in M.F if x in self.F and y not in M.F}
        return DFA(Q, self.Σ, delta_dict, (self.q_0, M.q_0), F)

    def compliment(self):
        return DFA(self.Q, self.Σ, self.δ_dict, self.q_0, self.Q - self.F)

    def reduce(self):
        state_pairs = {frozenset({x, y}) for x in self.Q for y in self.Q if x != y}
        non_distinguishable_pairs = set()
        non_distinguishable_states = set()
        distinguishable_pairs = {x for x in state_pairs if len(set(x).intersection(self.F)) == 1}

        def is_distinguishable(pair):
            # Recursive Discovery of Distinguishable Pairs with Memory Function
            if len(pair) == 1:
                return False
            if pair in distinguishable_pairs:
                return True
            else:
                for a in self.Σ:
                    next_pair = frozenset(map(lambda x: self.δ(x, a), pair))
                    if is_distinguishable(next_pair):
                        distinguishable_pairs.update({pair})
                        return True
                return False

        for pair in state_pairs:
            if not is_distinguishable(pair):
                non_distinguishable_pairs.update({pair})
                non_distinguishable_states.update(pair)

        def transitive_closure(array):
            new_list = [frozenset(array.pop(0))]  # initialize first set with value of index `0`

            for item in array:
                for i, s in enumerate(new_list):
                    if any(x in s for x in item):
                        new_list[i] = new_list[i].union(item)
                        break
                else:
                    new_list.append(frozenset(item))
            return set(new_list)

        non_distinguishable_pairs = transitive_closure(list(non_distinguishable_pairs))

        Q = non_distinguishable_pairs.union({frozenset(x) for x in self.Q - non_distinguishable_states})
        delta_dict = defaultdict(dict)
        for q in Q:
            for a in self.Σ:
                delta_dict[q][a] = list({x for x in Q if x.intersection(set(map(lambda x: self.δ(x, a), q)))})[0]
        q_0 = [x for x in Q if self.q_0 in x][0]
        F = {x for x in Q if x.intersection(self.F)}
        print(Q, set(delta_dict[list(Q)[0]].values()), sep='\n')
        return DFA(Q, self.Σ, delta_dict, q_0, F)


if __name__ == '__main__':
    m = DFA({'q0', 'q1'},
            {'a', 'b'},
            {'q0': {'a': 'q1', 'b': 'q0'},
             'q1': {'a': 'q0', 'b': 'q1'}
             },
            'q0',
            {'q0'})
    m.draw('dfa.png')
    print(m.is_accepted('aaaba'))
    n = DFA({'q0', 'q1'},
            {'a', 'b'},
            {'q0': {'a': 'q0', 'b': 'q1'},
             'q1': {'a': 'q1', 'b': 'q0'}
             },
            'q0',
            {'q0'})
    o = DFA({'C', 'D', 'E'},
            {0, 1},
            {'C': {0: 'D', 1: 'E'},
             'D': {0: 'D', 1: 'E'},
             'E': {0: 'C', 1: 'E'}},
            'C',
            {'C', 'D'})
    import string

    p_q = list(string.ascii_uppercase[:8])
    p_sigma = [0, 1]
    p_f = {'C'}
    p_q0 = 'A'
    p_delta = ['BF', 'GC', 'AC', 'CG', 'HF', 'CG', 'GE', 'GC']
    p_delta = [dict(zip(p_sigma, list(x))) for x in p_delta]
    p_delta = dict(zip(p_q, p_delta))
    p = DFA(set(p_q), set(p_sigma), p_delta, p_q0, p_f)
    p.draw('dfa.png')
    p.reduce().draw('dfa_minimized.png')
