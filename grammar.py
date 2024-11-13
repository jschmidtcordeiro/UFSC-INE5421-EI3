class Grammar:
    def __init__(self, non_terminals, terminals, initial_symbol, productions):
        # self.non_terminals = ['A', 'B', 'S']
        # self.terminals = ['a', 'b', 'c', 'd']
        # self.initial_symbol = S
        # self.productions = {'S': ['Bd', '&'], 'B': ['Bc', 'b', 'Ab'], 'A': ['Sa', 'a']}
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.initial_symbol = initial_symbol
        self.productions = productions

    def __str__(self):
        return f"Non-terminals: {self.non_terminals}\nTerminals: {self.terminals}\nInitial symbol: {self.initial_symbol}\nProductions: {self.productions}"

    @classmethod
    def from_string(cls, input_str):
        # Split the input string into sections between curly braces
        sections = input_str.split('{')
        
        # Extract and clean up each component
        non_terminals = sections[1].split('}')[0].split(',')
        terminals = sections[2].split('}')[0].split(',')
        initial_symbol = sections[3].split('}')[0]
        
        # Convert productions into a dictionary for easier manipulation
        production_strings = sections[4].split('}')[0].split(';')
        productions = {}
        for prod in production_strings:
            if '=' in prod:
                left, right = prod.split('=')
                # Remove whitespace from left and right
                left = left.strip()
                right = right.strip()
                # Initialize list if key doesn't exist, then append
                if left not in productions:
                    productions[left] = []
                productions[left].append(right)
                
        return cls(non_terminals, terminals, initial_symbol, productions)
    
    def remove_useless_symbols(self):
        pass

    def remove_epsilon_productions(self):
        pass

    def remove_unit_productions(self):
        pass

    def remove_left_recursion(self):
        pass

