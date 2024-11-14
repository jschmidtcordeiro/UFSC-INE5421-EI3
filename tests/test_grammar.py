import json
import pytest
from pathlib import Path
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.grammar import Grammar

def load_test_cases(filename):
    test_cases_dir = Path(__file__).parent / "test_cases"
    with open(test_cases_dir / filename) as f:
        return json.load(f)

def assert_grammar_equals(actual, expected):
    """Helper function to compare grammars"""
    assert sorted(actual.non_terminals) == sorted(expected["non_terminals"]), "Non-terminals don't match"
    assert sorted(actual.terminals) == sorted(expected["terminals"]), "Terminals don't match"
    assert actual.initial_symbol == expected["initial_symbol"], "Initial symbol doesn't match"
    
    # Compare productions, ignoring order of productions for each non-terminal
    for nt in expected["productions"]:
        assert nt in actual.productions, f"Non-terminal {nt} missing from productions"
        assert sorted(actual.productions[nt]) == sorted(expected["productions"][nt]), \
            f"Productions for {nt} don't match"

class TestGrammar:
    def test_from_string(self):
        input_str = "{A,B,S}{a,b,c,d}{S}{S = Bd; S = &; B = Bc; B = b; B = Ab; A = Sa; A = a}"
        grammar = Grammar.from_string(input_str)
        
        expected = {
            "non_terminals": ["A", "B", "S"],
            "terminals": ["a", "b", "c", "d"],
            "initial_symbol": "S",
            "productions": {
                "S": ["Bd", "&"],
                "B": ["Bc", "b", "Ab"],
                "A": ["Sa", "a"]
            }
        }
        
        assert_grammar_equals(grammar, expected)

    @pytest.mark.parametrize("test_case", load_test_cases("useless_symbols.json"))
    def test_remove_useless_symbols(self, test_case):
        print(f"\nTesting: {test_case['name']}")
        grammar = Grammar.from_string(test_case["input"])
        grammar.remove_useless_symbols()
        assert_grammar_equals(grammar, test_case["expected"])

    @pytest.mark.parametrize("test_case", load_test_cases("epsilon_productions.json"))
    def test_remove_epsilon_productions(self, test_case):
        print(f"\nTesting: {test_case['name']}")
        grammar = Grammar.from_string(test_case["input"])
        grammar.remove_epsilon_productions()
        assert_grammar_equals(grammar, test_case["expected"])

    # @pytest.mark.parametrize("test_case", load_test_cases("unit_productions.json"))
    # def test_remove_unit_productions(self, test_case):
    #     print(f"\nTesting: {test_case['name']}")
    #     grammar = Grammar.from_string(test_case["input"])
    #     grammar.remove_unit_productions()
    #     assert_grammar_equals(grammar, test_case["expected"])

    # def test_combined_transformations(self):
    #     """Test all transformations in sequence"""
    #     input_str = "{S,A,B,C}{a,b,c}{S}{S = A; A = B; B = C; C = c; C = &}"
    #     grammar = Grammar.from_string(input_str)
        
    #     # Apply all transformations
    #     grammar.remove_useless_symbols()
    #     grammar.remove_epsilon_productions()
    #     grammar.remove_unit_productions()
        
    #     expected = {
    #         "non_terminals": ["S", "A", "B", "C", "S'"],
    #         "terminals": ["c"],
    #         "initial_symbol": "S'",
    #         "productions": {
    #             "S'": ["S", "&"],
    #             "S": ["c"],
    #             "A": ["c"],
    #             "B": ["c"],
    #             "C": ["c"]
    #         }
    #     }
        
    #     assert_grammar_equals(grammar, expected) 