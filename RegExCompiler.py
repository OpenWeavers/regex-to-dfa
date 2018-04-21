from antlr4 import *

if __name__ is not None and "." in __name__:
    from .RegExParser import RegExParser
    from .RegExCfgLexer import RegExLexer
    from .RegExVisitor import RegExVisitor
else:
    from RegExParser import RegExParser
    from RegExLexer import RegExLexer
    from RegExVisitor import RegExVisitor


class RegExCompiler:
    def __init__(self, filepath):
        self.input = FileStream(filepath)
        self.lexer = RegExLexer(self.input)
        self.stream = CommonTokenStream(self.lexer)
        self.parser = RegExParser(self.stream)
        self.tree = self.parser.prog()

    def compile(self):
        return RegExVisitor(self.stream).visit(self.tree)

    def draw_parse_tree(self):
        # TODO: ADD graphviz support
        # Now Prints in LISP Style
        # (root child1 child2 ... childN)
        print(self.tree.toStringTree(recog=self.parser))

