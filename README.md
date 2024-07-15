# Quickwit talk fr

## Titre

Découvrons ensemble la relève de l'observabilité avec les logs et traces : Quickwit

## Abstract

Aujourd'hui sur les projets cloud native, on dispose systématiquement d'une stack d'observabilité en place. Il en existe de nombreuses (Elasticstack, Graylog, Grafana...). Toutes ces stacks, à l'exception de solutions SaaS onéreuses telles que Datadog, reposent le plus souvent sur deux solutions pour le stockage et la recherche des logs: Elasticsearch ou Grafana Loki.

Ces deux solutions présentent toute deux des avantages et inconvénients : d'un côté Elasticsearch repose sur un moteur de recherche très puissant (Apache Lucene) mais consomme énormément de ressources pour maintenir des index performants, ce qui peux très vite devenir excessivement cher notamment sur du cloud public. De l'autre Loki très rapide à l'ingestion et moins couteux car stock les logs sur de l'object storage mais ne dispose pas de la puissance du moteur d'indexation d'elastic ce qui fait que les recherches sont souvent lentes et complexes.

Dans cette présentation, nous allons parler d'une nouvelle solution qui réunis le meilleur des deux mondes, Quickwit, et expliquer comment elle y est parvenue : en ré-écrivant un moteur de recherche comparable à Lucene avec de hautes performances et en utilisant le gain pour stocker les données indexée dans de l'object storage. On arrive donc à des performances similaires à celles d'elastic voire les surpassent avec des coûts d'infrastructure beaucoup qui sont très largement réduits.

Nous verrons également dans ce talk que Quickwit peut également servir de backend pour stocker des traces via OpenTelemetry et est compatible avec Jaeger UI ce qui permet également conserver ses traces durablement dans le temps grace à la promesse de l'object storage. On terminera enfin par une démo avec le plugin Grafana qui permet entre autre de corréler ses logs et ses traces et également faire office d'alternative aux APM.
