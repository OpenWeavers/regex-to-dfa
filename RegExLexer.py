# Generated from RegEx.g4 by ANTLR 4.7.1
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\n")
        buf.write("%\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3")
        buf.write("\6\3\7\3\7\3\b\3\b\3\t\3\t\3\t\3\t\2\2\n\3\3\5\4\7\5\t")
        buf.write("\6\13\7\r\b\17\t\21\n\3\2\4\3\2cd\5\2\13\13\17\17\"\"")
        buf.write("\2$\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2")
        buf.write("\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\3\23")
        buf.write("\3\2\2\2\5\25\3\2\2\2\7\27\3\2\2\2\t\31\3\2\2\2\13\33")
        buf.write("\3\2\2\2\r\35\3\2\2\2\17\37\3\2\2\2\21!\3\2\2\2\23\24")
        buf.write("\7,\2\2\24\4\3\2\2\2\25\26\7~\2\2\26\6\3\2\2\2\27\30\7")
        buf.write("g\2\2\30\b\3\2\2\2\31\32\7*\2\2\32\n\3\2\2\2\33\34\7+")
        buf.write("\2\2\34\f\3\2\2\2\35\36\7\f\2\2\36\16\3\2\2\2\37 \t\2")
        buf.write("\2\2 \20\3\2\2\2!\"\t\3\2\2\"#\3\2\2\2#$\b\t\2\2$\22\3")
        buf.write("\2\2\2\3\2\3\b\2\2")
        return buf.getvalue()


class RegExLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    ID = 7
    WS = 8

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'*'", "'|'", "'e'", "'('", "')'", "'\n'" ]

    symbolicNames = [ "<INVALID>",
            "ID", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "ID", 
                  "WS" ]

    grammarFileName = "RegEx.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


