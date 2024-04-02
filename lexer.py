from cmp.automata import State
from cmp.tools.myRegex import Regex
from cmp.utils import Token

class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):

            currentRegex = Regex(regex)
            states = State.from_nfa(currentRegex.automaton, True)
    
            for state in states[1]:
                if state.final:
                    state.tag = (token_type, n)

            regexs.append(states[0])

        return regexs
    
    def _build_automaton(self):
        start = State('start')
        
        for regex in self.regexs:
            start.add_epsilon_transition(regex)
        
        return start.to_deterministic()
    
        
    def _walk(self, string):
        state = self.automaton

        #Si comentas este for da bateo con la variable -final-
        for s in state.state:
                    if s.final:
                        final = state
                        final_lex = lex
                    else: 
                        final = None
        
        final_lex = lex = ''
        
        for symbol in string:
    
            if symbol in state.transitions:
                transitionStates = state.transitions[symbol]
                state = transitionStates[0]
                lex += symbol

                for s in state.state:
                    if s.final:
                        final = state
                        final_lex = lex
            else:
                break

        return final, final_lex

    def _tokenize(self, text):
        
        while text:
            final, lex = self._walk(text)
            
            if final is None:
                yield '$', self.eof
                return


            priority = float('inf')
            for s in final.state:
                if s.final:
                    ttype, p = s.tag
                    if p < priority:
                        priority = p
                        token_type = ttype

                    
            yield lex, token_type
            
            text = text[len(lex):]

        yield '$', self.eof

    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]