# UFSC-INE5421-EI3
Trabalho 3 - INE5421: Linguagens Formais e Compiladores

Nesta atividade, você deverá implementar um programa em Python que execute duas etapas principais:

1. **Remover transições por épsilon e remover produções unitárias**:
    - A primeira etapa do programa deve eliminar todas as transições por épsilon (produções que geram a palavra vazia representada por &). Após isso, sem as transições por épsilon, o programa deve remover todas as produções unitárias da gramática.
2. **Eliminar a recursão à esquerda**:
    - A segunda etapa do programa deve eliminar as recursões à esquerda presentes na gramática, tornando-a adequada para ser usada na construção do Analisador Sintático Preditivo LL(1).

**FORMATO DE ENTRADA**

**"{NT}{T}{NT Inicial}{Produções}"**

Onde:

- é a lista de não-terminais.
    
    {NT}
    
- é a lista de terminais.
    
    {T}
    
- é o símbolo inicial da gramática.
    
    {NT Inicial}
    
- é a lista de produções separadas por ';'.
    
    {Produções}
    

Cada produção tem o formato:

**"<Não-terminal> = <Corpo da produção>"**

Onde

<Corpo da produção>

pode ser uma sequência de símbolos terminais e não-terminais, e pode também conter o símbolo & que representa a produção vazia (*epsilon*). Atenção ao fato de que &

**não**

é um Terminal, logo não aparece na definição de G.

**FORMATO DE SAÍDA**

**<<Gramatica 1><Gramatica 2>>**

Onde:

- **Gramatica 1** é a gramática resultante após aplicar a etapa 1 (remoção de transições por épsilon e produções unitárias).
- **Gramatica 2** é a gramática resultante após aplicar a etapa 2 (eliminação da recursão à esquerda).

**Exemplo de Entrada e Saída**

Entrada:

```
"{A,B,S}{a,b,c,d}{S}{S = Bd; S = &; B = Bc; B = b; B = Ab; A = Sa; A = a}"

```

Saída:

```
<<{A,A',B,B',S}{a,b,c,d}{S}{S = Bd; S = &; B = bB'; B = AbB'; B' = cB'; B' = &; A = bB'daA'; A = bB'dA'; A = aA'; A' = bB'daA'; A' = bB'dA'; A' = &}><{A,A',B,B',S}{a,b,c,d}{S}{S = Bd; S = &; B = bB'; B = AbB'; A = bB'daA'; A = &aA'; A = aA'; B' = cB'; B' = &; A' = bB'daA'; A' = &}>>
```

**Instruções:**

- **Arquivo Principal**: Todo o código deve estar presente no arquivo **main.py**, que será fornecido a você. Certifique-se de que todas as funções estejam contidas neste arquivo.
- **Formato da Saída**: Mantenha a saída no formato especificado. A ordem dos elementos não é relevante dentro dos conjuntos **{ }**. O importante é que todos os elementos estejam presentes.
- **Tratamento de Vazio**: Utilize o símbolo **&** para representar a produção vazia (épsilon).
- **Criando novos NT:** O algoritmo de remoção de escape por & e o de eliminação de recursão à esquerda envolve a criação de novos não terminais, seque um exemplo:
    
    S ⇒ S a | S b | c | d
    
    Removendo a recursão à esquerda do S, ficaria:
    
    S ⇒ cS' | dS'
    
    S' ⇒ ε | aS' | bS'
    
    Ou seja, quando criado um novo NT, o nome dele deve sempre ser o nome do símbolo que originou ele (nesse caso, foi o S), e concatenar com um apóstrafo '.
    
    **Dicas:**
    
- **Faça as etapas na ordem:** o algoritmo de Remoção de Recursão à esquerda requer que a gramática de entrada não possua nenhum NT (com exceção do NT inicial) que tenha escape por &. Além disso, ele também requer que a gramática não possua operações unitárias, por isso, considere a etapa 1 como uma "preparação" da entrada para a etapa 2.
- **Não esqueça de computar os NT que são recursivos à esquerda indiretamente, exemplo:**
    
    A ⇒ B r
    
    B ⇒ C d
    
    C ⇒ A t
    
- **O mesmo vale para escape por &, exemplo:**A ⇒ B r | B CB ⇒ d | &C ⇒ A t | B b