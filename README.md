# regex-to-dfa
A Python Implementation to convert Regular Expression directly to DFA

# Pre Requisites
- `python3`
- `graphviz`, `libgraphviz` in case of Ubuntu
- `java` and `javac` (Install from any package like `openjdk`
- `antlr4`, follow the exact steps from their [website](http://www.antlr.org/) and add `export`s to the shell configuration file(Usually `~/.bashrc`)

# Parser Capabilities
## Alphabets
- RegExs should be defined over alphabet `{a,b}`
- Epsilon is coded as `e`
- Whitespaces are skipeed
## Rules
- Klnee Closure Operator (`*`)
- Concatenation
- Alternation Operator (`|`)
- Grouping by means of Parenthesis

# Installation
`python3 -m pip install -r requirements.txt`

# Running
`python3 main.py`
