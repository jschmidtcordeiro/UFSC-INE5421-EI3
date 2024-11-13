"""
Alunos:
  Gabriel Reimann Cervi (22204117)
  João Pedro Schmidt Cordeiro (22100628)
"""
from grammar import Grammar

def main():
    input = "{A,B,S}{a,b,c,d}{S}{S = Bd; S = &; B = Bc; B = b; B = Ab; A = Sa; A = a}"
    input = "{A,B,C,D,E,F,S}{a,b,c,d,e,f}{S}{S = aSa;S = FbD;S = BE;A = aA; A = CA; A = &; B = bB; B = FE; C = cCb; C = AcA; D = Dd; D = fF; D = c; E = BC; E = eE; E = EB; F = fF; F = Dd}"
    grammar = Grammar.from_string(input)
    grammar.remove_useless_symbols()
   
if __name__ == "__main__":
    main()