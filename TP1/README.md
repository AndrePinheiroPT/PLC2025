# TPC 1:
Andre Filipe Dourado Pinheiro, A108473

 - Escreva uma expressão regular que represente strings binárias que não têm a substring 011.

## Lista de resultados:

### Solução:
```regex
1*(0+1)*0*
```

### Explicação:

Provemos que qualquer string gerada por esta expressão não contêm a substring `011`. Ao analisar a expressão, vemos que para cada ocorrência de `1`s, estes aparecem de forma contínua no prefixo da string (representado por `1*`) ou sempre a seguir a um conjunto de `0`s. 

Para a demonstração do recíoproco, basta reparar que a string pode ser separada em: o maior prefixo de `1`s, o maior sufixo de `0`s e depois e todos blocos representados por `0+1`.