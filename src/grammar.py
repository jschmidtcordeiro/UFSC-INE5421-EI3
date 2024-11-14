from itertools import combinations

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

    def print_productions(self):
        # Print initial symbol first
        if self.initial_symbol in self.productions:
            productions_str = " | ".join(self.productions[self.initial_symbol])
            print(f"    {self.initial_symbol} -> {productions_str}")
        
        # Print remaining symbols in alphabetical order
        for symbol in sorted(self.productions.keys()):
            if symbol != self.initial_symbol:
                productions_str = " | ".join(self.productions[symbol])
                print(f"    {symbol} -> {productions_str}")
    
    def remove_useless_symbols(self):
        self.remove_unreachable_symbols()
        self.remove_unproductive_symbols()

    # Update the grammar based on the productions
    def update_grammar(self):
        non_terminals = []
        terminals = []

        for symbol in self.non_terminals:
            if symbol in self.productions:
                non_terminals.append(symbol)

                for production in self.productions[symbol]:
                    for char in production:
                        if char in self.terminals and char not in terminals:
                            terminals.append(char)
        
        self.non_terminals = non_terminals
        self.terminals = terminals

    def remove_unreachable_symbols(self):
        reachable_symbols = set()
        marked = set()
        marked.add(self.initial_symbol)

        # Remove symbols that are not in the productions
        for symbol in self.non_terminals:
            if symbol not in self.productions:
                self.non_terminals.remove(symbol)

        while marked:
            symbol = marked.pop()
            reachable_symbols.add(symbol)
            if symbol in self.productions:
                for production in self.productions[symbol]:
                    for char in production:
                        if char in self.non_terminals and char not in reachable_symbols:
                            marked.add(char)

        non_reachable_symbols = set(self.non_terminals) - reachable_symbols
        print("Removing non-reachable symbols:", non_reachable_symbols)
        for symbol in non_reachable_symbols:
            self.non_terminals.remove(symbol)
            if symbol in self.productions:
                del self.productions[symbol]

        self.update_grammar()

    def remove_unproductive_symbols(self):
        productive_symbols = set()

        ## Run through all non-terminal symbols and mark them as productive if they have a production with only terminal symbols or epsilon
        for symbol in self.non_terminals:
            if symbol in self.productions:
                for production in self.productions[symbol]:
                    if all(char in self.terminals for char in production):
                        productive_symbols.add(symbol)
        
        if not productive_symbols:
            return

        have_symbols_to_mark = True

        while have_symbols_to_mark:
            have_symbols_to_mark = False
            # For all not marked non-terminal symbols
            for non_terminal_symbol in set(self.non_terminals) - productive_symbols:
                for production in self.productions[non_terminal_symbol]:
                    if all(char in self.terminals or char in productive_symbols for char in production):
                        productive_symbols.add(non_terminal_symbol)
                        have_symbols_to_mark = True

        non_productive_symbols = set(self.non_terminals) - productive_symbols
        print("Removing non-productive symbols:", non_productive_symbols)

        # Remove non-productive symbols from productions
        for symbol in non_productive_symbols:
            del self.productions[symbol]
        
        # Remove non-productive symbols from non-terminals
        self.non_terminals = list(productive_symbols)
        
        # Remove productions with non-productive symbols (fixed version)
        for symbol in self.non_terminals:
            # Create a new list with only the valid productions
            valid_productions = [
                production for production in self.productions[symbol]
                if not any(non_productive_symbol in production 
                          for non_productive_symbol in non_productive_symbols)
            ]
            self.productions[symbol] = valid_productions
        self.print_productions()

        self.update_grammar()

    def remove_epsilon_productions(self):
        nullable_symbols = {'&'}

        # 1. Identificar os não-terminais anuláveis:
        # a. Inicialize o conjunto de não-terminais anuláveis (Nε) como vazio.
        # b. Para cada produção da forma A → α na gramática:
        #     i. Se α contém apenas ε, adicione A ao conjunto Nε.
        # c. Enquanto houver novos não-terminais a adicionar ao Nε:
        #     i. Para cada produção A → X1 X2 ... Xn:
        #         - Se todos os Xi pertencem a Nε, adicione A ao Nε.

        # Search for non-terminal symbols with epsilon productions
        for symbol in self.non_terminals:
            for production in self.productions[symbol]:
                if '&' in production:
                    nullable_symbols.add(symbol)
        
        
        old_nullable_symbols_length = 1 # '&' is already in nullable_symbols
        while old_nullable_symbols_length != len(nullable_symbols):
            old_nullable_symbols_length = len(nullable_symbols)
            for symbol in self.non_terminals:
                for production in self.productions[symbol]:
                    if all(char in nullable_symbols for char in production):
                        nullable_symbols.add(symbol)

        print("Nullable symbols:", nullable_symbols)

        # 2. Eliminar produções ε:
        # a. Para cada produção A → X1 X2 ... Xn:
        #     i. Gere todas as combinações possíveis de X1 X2 ... Xn removendo 0 ou mais não-terminais de Nε.
        #     ii. Adicione as novas produções resultantes à gramática, sem duplicatas.
        # b. Remova todas as produções originais que contêm ε no lado direito (como A → ε), exceto se forem do símbolo inicial.

        for symbol in self.non_terminals:
            new_productions = set()  # Use set to avoid duplicates
            for production in self.productions[symbol][:]:  # Create a copy to iterate
                if production == '&':
                    continue  # Skip epsilon productions for now
                
                # Find positions of nullable symbols in the production
                nullable_positions = [i for i, char in enumerate(production) 
                                   if char in nullable_symbols and char != '&']
                
                # Generate all possible combinations of these positions
                for r in range(len(nullable_positions) + 1):
                    for pos_combo in combinations(nullable_positions, r):
                        # Create new production by keeping characters NOT in pos_combo
                        new_prod = ''.join(char for i, char in enumerate(production) 
                                         if i not in pos_combo)
                        if new_prod:  # Don't add empty productions
                            new_productions.add(new_prod)
                
            # Update productions for this symbol
            self.productions[symbol] = list(new_productions)
            
            # Keep epsilon production only for initial symbol if it was nullable
            if symbol == self.initial_symbol and symbol in nullable_symbols:
                self.productions[symbol].append('&')
        
        # 3. Tratar o símbolo inicial:
        # a. Se o símbolo inicial S ainda gera ε:
        #     i. Adicione um novo símbolo inicial S' com produções:
        #         - S' → S
        #         - S' → ε        if '&' in self.productions[self.initial_symbol]:
        #     ii. Remover a produção ε do símbolo inicial S.
        # Create new initial symbol (S')
        self.print_productions()
        if '&' in self.productions[self.initial_symbol]:
            new_initial = self.initial_symbol + "'"
            while new_initial in self.non_terminals:  # Ensure unique name
                new_initial += "'"
        
            # Add new initial symbol to non-terminals
            self.non_terminals.append(new_initial)
        
            # Add productions for new initial symbol
            self.productions[new_initial] = [self.initial_symbol, '&']

            # Remove epsilon production from initial symbol
            self.productions[self.initial_symbol].remove('&')
            
            # Update initial symbol
            self.initial_symbol = new_initial

        print("Productions after removing epsilon productions:")
        self.print_productions()

        self.update_grammar()

    def remove_unit_productions(self):
        # For each non-terminal A, compute set of non-terminals reachable through unit productions
        unit_pairs = set()
        for A in self.non_terminals:
            # Initialize with reflexive pairs (A,A)
            current_pairs = {(A, A)}
            changed = True
            
            while changed:
                changed = False
                # Look for B → C where (A,B) is already found
                new_pairs = set()
                for B, C in [(b, c) for b, c in current_pairs]:
                    if B in self.productions:
                        for prod in self.productions[B]:
                            # If production is a single non-terminal
                            if len(prod) == 1 and prod in self.non_terminals:
                                new_pair = (A, prod)
                                if new_pair not in current_pairs:
                                    new_pairs.add(new_pair)
                                    changed = True
                current_pairs.update(new_pairs)
            unit_pairs.update(current_pairs)
        
        # Create new productions without unit productions
        new_productions = {}
        for A in self.non_terminals:
            new_productions[A] = []
            # For each non-terminal B reachable from A through unit productions
            for _, B in [(x, y) for x, y in unit_pairs if x == A]:
                if B in self.productions:
                    # Add all non-unit productions of B to A
                    for prod in self.productions[B]:
                        # Skip unit productions
                        if len(prod) != 1 or prod not in self.non_terminals:
                            if prod not in new_productions[A]:
                                new_productions[A].append(prod)
        
        # Update the grammar's productions
        self.productions = new_productions

        self.update_grammar()

        print("Productions after removing unit productions:")
        self.print_productions()

    def remove_left_recursion(self):
        pass

