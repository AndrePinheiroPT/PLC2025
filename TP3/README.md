# TPC 3:
Andre Filipe Dourado Pinheiro, A108473

 - Construir um analisador léxico para uma liguagem de query com a qual se podem escrever frases do género,

```
select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000
```

## Lista de resultados:

Os resultados podem ser encontrados [aqui](./analyser.ipynb)