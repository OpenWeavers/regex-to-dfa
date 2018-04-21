import subprocess
from antlr4 import *
from collections import defaultdict
import pygraphviz as pgv

if __name__ is not None and "." in __name__:
    from .RegExParser import RegExParser
    from .RegExLexer import RegExLexer
    from .RegExVisitor import RegExVisitor
    from .DFA import DFA
else:
    from RegExParser import RegExParser
    from RegExLexer import RegExLexer
    from RegExVisitor import RegExVisitor
    from DFA import DFA


def draw_parse_tree(node, filename,format='png'):
    G = pgv.AGraph(rankdir='TB')
    queue = [(node, 0)]
    visited = []
    i = 0
    while queue:
        current = queue.pop(0)
        parent_id = current[1]
        if current[0] not in visited:
            visited.append(current[0])
            for child in [current[0].left, current[0].right]:
                if child is not None:
                    i += 1
                    G.add_node(str(parent_id) + current[0].text,
                               label=current[0].text)
                    G.add_node(str(i) + child.text, label=child.text)
                    G.add_edge(str(parent_id) + current[0].text,
                               str(i) + child.text)
                    queue.append((child, i))
    G.draw(filename, format=format, prog='dot')


def regex_to_dfa(root, visitor):
    Dstates = [frozenset(root.firstpos)]
    Dtran = defaultdict(dict)
    q_0 = frozenset(root.firstpos)
    queue = [frozenset(root.firstpos)]
    while queue:
        S = queue.pop(0)
        for a in ['a', 'b']:
            U = set()
            for p in S:
                if visitor.charmap[p - 1] == a:
                    U = U.union(visitor.followpos[p])
                U = frozenset(U)
                if U not in Dstates:
                    Dstates.append(U)
                    queue.append(U)
                Dtran[S][a] = U
    F = {q for q in Dstates if len(visitor.charmap) in q}
    return DFA(Dstates, {'a', 'b'}, Dtran, q_0, F)


if __name__ == '__main__':
    regex = input("Enter the regular expression: ")
    with open('test.txt', "w") as file:
        file.writelines([regex, '\n'])
    input_file = FileStream('test.txt')
    lexer = RegExLexer(input_file)
    stream = CommonTokenStream(lexer)
    parser = RegExParser(stream)
    tree = parser.prog()
    visitor = RegExVisitor()
    root = visitor.visit(tree)
    draw_parse_tree(root, 'parsetree.pdf',format='pdf')
    subprocess.call(['evince', 'parsetree.pdf'])
    D = regex_to_dfa(root, visitor)
    D.draw('dfa.pdf',format='pdf')
    subprocess.call(['evince', 'dfa.pdf'])
    string = input('Enter a string to be tested: ')
    print("Accepted" if D.is_accepted(string) else "Not accepted")
