"""
Alunos:
  Gabriel Reimann Cervi (22204117)
  João Pedro Schmidt Cordeiro (22100628)
"""
from grammar import Grammar

def main():
    input = "{A,B,S}{a,b,c,d}{S}{S = Bd; S = &; B = Bc; B = b; B = Ab; A = Sa; A = a}"
    grammar = Grammar.from_string(input)
    print(grammar)
   
if __name__ == "__main__":
    main()