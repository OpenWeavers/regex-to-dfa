# Generated from RegEx.g4 by ANTLR 4.7.1
from antlr4 import *
from collections import defaultdict

if __name__ is not None and "." in __name__:
    from .RegExParser import RegExParser
else:
    from RegExParser import RegExParser

# This class defines a complete generic visitor for a parse tree produced by RegExParser.


class Node:
    def __init__(self):
        self.firstpos = set()
        self.lastpos = set()
        self.nullable = False
        self.text = ''
        self.left = None
        self.right = None


class RegExVisitor(ParseTreeVisitor):
    i = 1
    charmap = []
    followpos = defaultdict(set)

    # Visit a parse tree produced by RegExParser#prog.
    def visitProg(self, ctx: RegExParser.ProgContext):
        n = Node()
        n.left = self.visit(ctx.regex(0))
        n.right = self.visit(ctx.newline(0))
        n.text = '.'
        n.nullable = n.left.nullable and n.right.nullable
        n.firstpos = n.left.firstpos.union(n.right.firstpos) if n.left.nullable else n.left.firstpos
        n.lastpos = n.left.lastpos.union(n.right.lastpos) if n.right.nullable else n.right.lastpos
        for i in n.left.lastpos:
            self.followpos[i] = self.followpos[i].union(n.right.firstpos)
        return n
        # print(root.firstpos, root.lastpos, root.nullable, self.followpos)

    # Visit a parse tree produced by RegExParser#epsilon.
    def visitEpsilon(self, ctx: RegExParser.EpsilonContext):
        n = Node()
        n.nullable = True
        n.text = 'e'
        return n

    # Visit a parse tree produced by RegExParser#identifier.
    def visitIdentifier(self, ctx: RegExParser.IdentifierContext):
        n = Node()
        n.text = ctx.getText()
        n.firstpos = {self.i}
        n.lastpos = {self.i}
        self.charmap.append(n.text)
        self.i += 1
        return n

    # Visit a parse tree produced by RegExParser#concatenation.
    def visitConcatenation(self, ctx: RegExParser.ConcatenationContext):
        n = Node()
        n.left = self.visit(ctx.regex(0))
        n.right = self.visit(ctx.regex(1))
        n.text = '.'
        n.nullable = n.left.nullable and n.right.nullable
        n.firstpos = n.left.firstpos.union(n.right.firstpos) if n.left.nullable else n.left.firstpos
        n.lastpos = n.left.lastpos.union(n.right.lastpos) if n.right.nullable else n.right.lastpos
        for i in n.left.lastpos:
            self.followpos[i] = self.followpos[i].union(n.right.firstpos)
        return n

    # Visit a parse tree produced by RegExParser#alternation.
    def visitAlternation(self, ctx: RegExParser.AlternationContext):
        n = Node()
        n.left = self.visit(ctx.regex(0))
        n.right = self.visit(ctx.regex(1))
        n.text = '|'
        n.nullable = n.left.nullable or n.right.nullable
        n.firstpos = n.left.firstpos.union(n.right.firstpos)
        n.lastpos = n.left.lastpos.union(n.right.lastpos)
        return n

    # Visit a parse tree produced by RegExParser#klnee.
    def visitKlnee(self, ctx: RegExParser.KlneeContext):
        n = Node()
        n.nullable = True
        n.text = '*'
        n.left = self.visit(ctx.regex())
        n.firstpos = n.left.firstpos
        n.lastpos = n.left.lastpos
        for i in n.lastpos:
            self.followpos[i] = self.followpos[i].union(n.firstpos)
        return n

    # Visit a parse tree produced by RegExParser#parenthesis.
    def visitParenthesis(self, ctx: RegExParser.ParenthesisContext):
        return self.visit(ctx.regex())

    # Visit a parse tree produced by RegExParser#newline.
    def visitNewline(self, ctx: RegExParser.NewlineContext):
        n = Node()
        n.text = '#'
        n.firstpos = {self.i}
        n.lastpos = {self.i}
        self.charmap.append(n.text)
        self.i += 1
        return n


del RegExParser
