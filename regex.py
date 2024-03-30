b"from cmp.ast import AtomicNode,BinaryNode,UnaryNode\nfrom cmp.pycompiler import Grammar\nfrom cmp.tools.automata import(DFA,NFA,automata_closure,automata_concatenation,automata_minimization,automata_union,nfa_to_dfa)\nfrom cmp.tools.evaluation import evaluate_parse\nfrom cmp.tools.parsing import metodo_predictivo_no_recursivo\nfrom cmp.utils import Token\nq=DFA\nclass EpsilonNode(AtomicNode):\n def evaluate(self):\n  return q(states=1,finals=[0],transitions={})\nr=EpsilonNode\nclass SymbolNode(AtomicNode):\n def evaluate(self):\n  s=self.lex\n  return q(states=2,finals=[1],transitions={(0,s):1})\nc=SymbolNode\nclass ClosureNode(UnaryNode):\n @staticmethod\n def operate(value):\n  return automata_closure(value)\nQ=ClosureNode\nclass UnionNode(BinaryNode):\n @staticmethod\n def operate(lvalue,rvalue):\n  return automata_union(lvalue,rvalue)\nR=UnionNode\nclass ConcatNode(BinaryNode):\n @staticmethod\n def operate(lvalue,rvalue):\n  return automata_concatenation(lvalue,rvalue)\nFF=ConcatNode\ndef regex_tokenizer(text,G,skip_whitespaces=True):\n h=[]\n GG={x:Token(x,G[x])for x in['|','*','(',')','\xce\xb5']}\n for z in text:\n  if skip_whitespaces and z.isspace():\n   continue\n  try:\n   j=GG[z]\n  except KeyError:\n   j=Token(z,G['symbol'])\n  finally:\n   h.append(j)\n h.append(Token('$',G.EOF))\n return h\ndef build_grammar():\n G=Grammar()\n E=G.NonTerminal('E',True)\n T,F,A,X,Y,Z=G.NonTerminals('T F A X Y Z')\n p,M,S,B,a,U=G.Terminals('| * ( ) symbol \xce\xb5')\n E%=T+X,lambda h,s:s[2],None,lambda h,s:s[1]\n X%=p+E,lambda h,s:R(h[0],s[2])\n X%=G.Epsilon,lambda h,s:h[0]\n T%=F+Y,lambda h,s:s[2],None,lambda h,s:s[1]\n Y%=T,lambda h,s:FF(h[0],s[1])\n Y%=G.Epsilon,lambda h,s:h[0]\n F%=A+Z,lambda h,s:s[2],None,lambda h,s:s[1]\n Z%=M,lambda h,s:Q(h[0])\n Z%=G.Epsilon,lambda h,s:h[0]\n A%=a,lambda h,s:c(s[1])\n A%=U,lambda h,s:r(s[1])\n A%=S+E+B,lambda h,s:s[2]\n return G\nG=build_grammar()\nL=metodo_predictivo_no_recursivo(G)\nclass Regex:\n def __init__(self,regex,skip_whitespaces=False):\n  W=self\n  W.regex=regex\n  W.automaton=W.build_automaton(regex)\n def __call__(self,text):\n  W=self\n  return W.automaton.recognize(text)\n @staticmethod\n def build_automaton(regex,skip_whitespaces=False):\n  h=regex_tokenizer(regex,G,skip_whitespaces=False)\n  f=L(h)\n  T=evaluate_parse(f,h)\n  H=T.evaluate()\n  X=nfa_to_dfa(H)\n  k=automata_minimization(X)\n  return k\n"
