"""
Alunos:
  Gabriel Reimann Cervi (22204117)
  João Pedro Schmidt Cordeiro (22100628)
"""
from grammar import Grammar

def main():
    input = "{A,B,S}{a,b,c,d}{S}{S = Bd; S = &; B = Bc; B = b; B = Ab; A = Sa; A = a}"
    input = "{A,B,C,D,E,F,S}{a,b,c,d,e,f}{S}{S = aSa;S = FbD;S = BE;A = aA; A = CA; A = &; B = bB; B = FE; C = cCb; C = AcA; D = Dd; D = fF; D = c; E = BC; E = eE; E = EB; F = fF; F = Dd}"
    input = "{S,A,B,C,D}{a,b,c,d}{S}{S = AB; S = aS; A = bA; A = BC; B = db; B = C; B = &; C = cCc; C = BD; D = CD; D = d; D = &}"
    input = "{S,A,B,C}{a,b,c}{S}{S = ABC; A = &; B = b; B = &; C = c; C = &}"
    grammar = Grammar.from_string(input)
    grammar.remove_useless_symbols()
    grammar.remove_epsilon_productions()
    grammar.remove_unit_productions()
   
if __name__ == "__main__":
    main()