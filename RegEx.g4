grammar RegEx;

prog : (regex newline)*;

regex : regex '*'      #klnee
  | regex regex	       #concatenation
  | regex '|' regex    #alternation
  | ID         	       #identifier
  | 'e'	       	       #epsilon
  | '(' regex ')'      #parenthesis
  ;

newline : '\n';

ID: [ab];
WS: [\t\r ]->skip;
