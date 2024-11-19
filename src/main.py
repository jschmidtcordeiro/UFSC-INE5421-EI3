"""
Alunos:
  Gabriel Reimann Cervi (22204117)
  João Pedro Schmidt Cordeiro (22100628)
"""

from sys import argv
from grammar import Grammar

# Funcao para printar os casos de testes do Moodle de uma forma mais organizada
def print_test_cases():
    print("================================================")
    print("\nCaso de teste 1:")
    print("Gramática 1:")
    input = "{S,S',A,B}{a,b,c,d}{S}{S = Bd; A = a; A = Sa; B = b; B = Bc; B = Ab; S' = &; S' = S}"
    Grammar.from_string(input).print_productions()
    print("Gramática 2:")
    input = "{S,S',A,B}{a,b,c,d}{S}{S = Bd; A = a; A = Sa; B = b; B = Bc; B = Ab; S' = &; S' = S}"
    Grammar.from_string(input).print_productions()
    print("\n================================================")

    print("\nCaso de teste 2:")
    print("Gramática 1:")
    input = "{E,F,P,T}{(,),*,**,+,-,/,cte,id}{E}{E = T; E = E + T; E = E - T; F = F ** P; F = P; P = id; P = (E); P = cte; T = F; T = T / F; T = T * F}"
    Grammar.from_string(input).print_productions()
    print("Gramática 2:")
    input = "{E,F,P,T}{(,),*,**,+,-,/,cte,id}{E}{E = T; E = E + T; E = E - T; F = F ** P; F = P; P = id; P = (E); P = cte; T = F; T = T / F; T = T * F}"
    Grammar.from_string(input).print_productions()

    print("\n================================================")

    print("\nCaso de teste 3:")
    print("Gramática 1:")
    input = "{A,C,S}{a,b,c,d}{A}{A = Acc; A = Sc; C = a; C = Scd; C = Aba; C = Cb; S = Aa; S = Sab; S = Cc}"
    Grammar.from_string(input).print_productions()
    print("Gramática 2:")
    input = "{A,C,S}{a,b,c,d}{A}{A = Acc; A = Sc; C = a; C = Scd; C = Aba; C = Cb; S = Aa; S = Sab; S = Cc}"
    Grammar.from_string(input).print_productions()

    print("\n================================================")

def main():
    grammar = Grammar.from_string(input)
    grammar.remove_useless_symbols()
    grammar.remove_epsilon_productions()
    grammar.remove_unit_productions()
    grammar1 = grammar.clone()
    grammar.remove_left_recursion()

    print(f"<<{grammar1.string_output()}><{grammar.string_output()}>>")


if __name__ == "__main__":
    main()
