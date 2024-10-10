# Quickwit BDX/IO

## Titre

Découvrons ensemble la relève de l'observabilité avec les logs et traces : Quickwit

## Abstract

Aujourd'hui sur les projets cloud native, on dispose systématiquement d'une stack d'observabilité en place. Il en existe de nombreuses (Elasticstack, Graylog, Grafana...). Toutes ces stacks, à l'exception de solutions SaaS onéreuses telles que Datadog, reposent le plus souvent sur deux solutions pour le stockage et la recherche des logs: Elasticsearch ou Grafana Loki.

Ces deux solutions présentent toute deux des avantages et inconvénients : d'un côté Elasticsearch repose sur un moteur de recherche très puissant (Apache Lucene) mais consomme énormément de ressources pour maintenir des index performants, notamment il faut un noeud principal et deux replicas et tout est stocké sur du disque bloc storage (SSD), ce qui peut devenir excessivement cher particulièrement sur du cloud public. De l'autre Loki très rapide à l'ingestion et moins couteux car stock les logs sur de l'object storage mais ne dispose pas de la puissance du moteur d'indexation d'elastic ce qui fait que les recherches sont souvent lentes et complexes.

Dans cette présentation, nous allons parler d'une nouvelle solution qui réunis le meilleur des deux mondes, Quickwit, et expliquer comment elle y est parvenue : en ré-écrivant un moteur de recherche comparable à Lucene avec de hautes performances et en utilisant le gain pour stocker les données indexée dans de l'object storage, ce qui le rend complètement stateless et plus facile à opérer. On arrive à des performances similaires à celles d'Elasticsearch voire les surpassent avec des coûts d'infrastructure qui sont très largement réduits.

Nous verrons également dans cette présentation que Quickwit peut également servir de backend pour stocker des traces via OpenTelemetry et est compatible avec Jaeger UI ce qui permet également conserver ses traces durablement dans le temps grace à la promesse de l'object storage. 

Cette présentation s'accompagnera d'une démo dans laquelle Quickwit ingèrera des logs et traces en provenance d'une application Python via OTLP/grpc et on présentera des dashboards avec le plugin Grafana permettant de mettre en corrélation des logs et des traces et se substituer à un APM (_Application Performance Monitoring_, outil pour mesurer la performance de vos applications).

## Elevator pitch

Pour l'instant ça serait une première édition de ce talk en public mais déjà donné à plusieurs reprises avec succès dans des organisations internes.

Parmi les références on pourra citer quelques benchmark et storytelling disponibles ici :
* "How Binance built a 100PB log service with Quickwit": https://quickwit.io/blog/quickwit-binance-story
* "Benchmarking Quickwit vs. Loki": https://quickwit.io/blog/benchmarking-quickwit-loki

## Git repo

* Repo principal: https://gitlab.comwork.io/comwork_public/talks/bdx-quickwit
* Github mirror: https://github.com/idrissneumann/bdx-quickwit

## Demo

Suivre ce [README](./demo/README.md) pour reproduire la démo.

## Slides

Les slides sont disponibles [ici](./slides.pdf).
