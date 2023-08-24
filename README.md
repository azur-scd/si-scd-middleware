# Middleware pour les API du SI SCD

![forthebadge](forthebadge.svg)

Container à déployer sur un serveur jouant le rôle de serveur mandataire entre le SI et des applications tierces.

## Objectif

- Pouvoir requêter les API du SI depuis un client en "outrepassant" les contraintes de paramétrages du serveur si-scd.unice.fr (protocole http + restriction d'accès sur IP) par une requête serveur intermédiaire qui redirige les données en sortie vers le client
- Pouvoir manipuler les données Koha au passage afin de les rendre plus simples à parser côté client / ou les enrichir à la volée

## Cas d'usage

- Horaires des BU : passerelle exposant http://si-scd.unice.fr/si-scd/php/si2primo/allHoraires.php pour le portail web
- Bases de données (docelec) : passerelle exposant les métadonnées de signalement des BDD http://si-scd.unice.fr/si-scd-prod/api/signalement pour Primo. Les métadonnées sont converties en oai_dc à la volée (conversion xslt) et re-exposées en "simulant" un endpoint de serveur OAI-PMH (https://localhost:5000/oai.py?verb=ListRecords&metadataPrefix=oai_dc&set=BDD en local), qui sert ensuite de datasource OAI pour la configuration d'un pipe Primo.
  
## Routing API

- /api/v1 : Hello World
- /api/v1/hello : Hello World
- /api/v1/horaires : horaires d'ouverture des BU à - 1 semaine et + 6 mois
- /oai.py?verb=ListRecords&metadataPrefix=oai_dc&set=BDD : bdd en oai_dc


## Dev : Build & déploiement

### En local

```
git clone https://github.com/azur-scd/si-scd-middleware.git
docker build -t azurscd/si-scd-middleware:latest .
docker run -d --name si-scd-middleware -p 5000:5000 -v <your_local_path>/si-scd-middleware:/app azurscd/si-scd-middleware:latest

```
Tourne en local sur https://localhost:5000/si-scdo-middleware (ex : [https://localhost:5000/si-scd-middleware/api/v1/hello](https://localhost:5000/si-scd-middleware/api/v1/hello))

### CI/CD

Chaque commit/push sur Github déclenche une Github Action qui rebuild et push l'image sur Docker Hub.

## Prod

Dépôt Docker Hub : [https://hub.docker.com/repository/docker/azurscd/si-scd-middleware](https://hub.docker.com/repository/docker/azurscd/si-scd-middleware)

## Documentation

Doc Swagger



