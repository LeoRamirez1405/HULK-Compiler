from cmp.ast import AtomicNode,BinaryNode,UnaryNode
from cmp.pycompiler import Grammar
from cmp.tools.automata import(DFA,NFA,automata_closure,automata_concatenation,automata_minimization,automata_union,nfa_to_dfa)
from cmp.tools.evaluation import evaluate_parse
from cmp.tools.parsing import metodo_predictivo_no_recursivo
from cmp.utils import Token

q=DFA
class EpsilonNode(AtomicNode):
 def evaluate(self):
  return q(states=1,finals=[0],transitions={})

r=EpsilonNode
class SymbolNode(AtomicNode):
 def evaluate(self):
  s=self.lex
  return q(states=2,finals=[1],transitions={(0,s):1})

c=SymbolNode
class ClosureNode(UnaryNode):
 @staticmethod
 def operate(value):
  return automata_closure(value)

Q=ClosureNode
class UnionNode(BinaryNode):
 @staticmethod
 def operate(lvalue,rvalue):
  return automata_union(lvalue,rvalue)

R=UnionNode
class ConcatNode(BinaryNode):
 @staticmethod
 def operate(lvalue,rvalue):
  return automata_concatenation(lvalue,rvalue)

FF=ConcatNode
def regex_tokenizer(text,G,skip_whitespaces=True):
  # print(text)
  h=[]
  GG={x:Token(x,G[x])for x in['|','*','(',')','\xce\xb5']}
  backlashed = False
  for z in text:  
      if(z == '\\'):
        backlashed = True
        continue
      
      if skip_whitespaces and z.isspace():
        continue
      try:
        if not backlashed:
          j=GG[z]
        else:
          raise KeyError
        
      except KeyError:
        backlashed = False
        j=Token(z,G['symbol'])
      finally:
        print(f"Added {j}")
        h.append(j)
  h.append(Token('$',G.EOF))
  return h

def build_grammar():
 G=Grammar()
 E=G.NonTerminal('E',True)
 T,F,A,X,Y,Z=G.NonTerminals('T F A X Y Z')
 p,M,S,B,a,U=G.Terminals('| * ( ) symbol \xce\xb5')
 E%=T+X,lambda h,s:s[2],None,lambda h,s:s[1]
 X%=p+E,lambda h,s:R(h[0],s[2])
 X%=G.Epsilon,lambda h,s:h[0]
 T%=F+Y,lambda h,s:s[2],None,lambda h,s:s[1]
 Y%=T,lambda h,s:FF(h[0],s[1])
 Y%=G.Epsilon,lambda h,s:h[0]
 F%=A+Z,lambda h,s:s[2],None,lambda h,s:s[1]
 Z%=M,lambda h,s:Q(h[0])
 Z%=G.Epsilon,lambda h,s:h[0]
 A%=a,lambda h,s:c(s[1])
 A%=U,lambda h,s:r(s[1])
 A%=S+E+B,lambda h,s:s[2]
 return G

G=build_grammar()
L=metodo_predictivo_no_recursivo(G)

class Regex:
    def __init__(self,regex,skip_whitespaces=False):
        W=self
        W.regex=regex
        W.automaton=W.build_automaton(regex)

    def __call__(self,text):
        W=self
        return W.automaton.recognize(text)
    
    @staticmethod
    def build_automaton(regex,skip_whitespaces=False):
        h=regex_tokenizer(regex,G,skip_whitespaces=False)
        f=L(h)
        T=evaluate_parse(f,h)
        H=T.evaluate()
        X=nfa_to_dfa(H)
        k=automata_minimization(X)
        return k
