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
        self.remove_unreachable_symbols()
        self.remove_unproductive_symbols()

    def remove_unreachable_symbols(self):
        reachable_symbols = set()
        marked = set()
        marked.add(self.initial_symbol)

        while marked:
            symbol = marked.pop()
            reachable_symbols.add(symbol)
            for production in self.productions[symbol]:
                for char in production:
                    if char in self.non_terminals and char not in reachable_symbols:
                        marked.add(char)

        non_reachable_symbols = set(self.non_terminals) - reachable_symbols
        print("Removing non-reachable symbols:", non_reachable_symbols)
        for symbol in non_reachable_symbols:
            del self.productions[symbol]

    def remove_unproductive_symbols(self):
        productive_symbols = set()
        marked = set()

        ## Run through all non-terminal symbols and mark them as productive if they have a production with only terminal symbols or epsilon
        for symbol in self.non_terminals:
            for production in self.productions[symbol]:
                if all(char in self.terminals or char == '&' for char in production):
                    productive_symbols.add(symbol)
        
        if not productive_symbols:
            return

        have_symbols_to_mark = True

        while have_symbols_to_mark:
            have_symbols_to_mark = False
            # For all not marked non-terminal symbols
            for non_terminal_symbol in set(self.non_terminals) - productive_symbols:
                for production in self.productions[non_terminal_symbol]:
                    ## If the production contains terminal symbols, epsilon or productive symbols, mark the symbol
                    if all(char in self.terminals or char == '&' or char in productive_symbols for char in production):
                        productive_symbols.add(non_terminal_symbol)
                        have_symbols_to_mark = True


        non_productive_symbols = set(self.non_terminals) - productive_symbols
        print("Removing non-productive symbols:", non_productive_symbols)
        for symbol in non_productive_symbols:
            del self.productions[symbol]

    def remove_epsilon_productions(self):
        pass

    def remove_unit_productions(self):
        pass

    def remove_left_recursion(self):
        pass

