# Discord-ProgramCompiler
Un bot pour compiler et exécuter les programmes envoyés sur discord.
**Ce bot a été créé pour un challenge privé. Si vous voulez l'utiliser, vous devrez certainement le modifier.**

Ce bot n'accepte que les fichiers Python, Java et C. Si vous voulez en ajouter, proposez-le moi !

## Submition

Pour envoyer un test, envoyez le fichier par message privé à `ProgramCompiler#3290`.

- S'il n'y a qu'un seul fichier, son nom doit être le même que l'exercice pour lequel vous participez.
- S'il y a plusieurs fichiers pour le projet de votre exercice, vous devez le zipper comme montré ci-dessous. Le fichier principal (qui va être exécuté) doit avoir le nom de l'exercice, ainsi que le zip.
```
NomDeLexercice.zip
├── NomDeLexercice.ext
└── AutreFichier.ext
```
`NomDeLexercice` doit être le nom exact de l'exercice pour lequel vous participez.
`.ext` est l'extension de votre fichier. Par exemple, si vous l'avez écrit en Java, `.ext` devra être `.java`

Une fois que le test a été envoyé, il va être exécuté et testé avec les tests de l'exercice. Vous serez averti des erreurs, s'il y en a.

## Commandes Utilisateur

#### Lister tous les tests disponibles

`!list`

Envoie la liste des tests existants disponibles.

Alias: `!liste`, `!listes`, `!exercice`, `!exercices`, `!exercise` , `!exercises`

#### Afficher votre profil

`!profil`

Envoie les détails de votre profil (nom, image, score total, liste des exercices participés).

Alias: `!profile`, `!me`

#### Classement

`!classement`

Envoie le classement général de tous les participants, trié par score total.

Alias: `!leaderboard`, `!top`


## Commandes Administrateur

Elles fonctionnent de la même manière que les commandes shell, avec des arguments comme `-a "Ceci est un argument"`.

#### Créer un nouvel exercice

`!create -t <titre> [-D -i -o -d -h]`

|    Argument    |                  Description                    | Défaut |
| -------------- | ----------------------------------------------- | ------ |
|-t --title      |**Obligatoir** Le titre de l'exercice            |        |
|-D --description|La description de l'exercice                     | *Vide* |
|-i --input      |Description des entrées envoyées par l'exercice  | *Vide* |
|-o --output     |Description des sorties attendues par l'exercice | *vide* |
|-d --difficulty |La difficulté de l'exercice (entre 1 et 10)      |   1    |
|-h --hidden     |Si la sortie attendue doit être masquée ou non   | false  |

Alias : `!createTest`, `!createExercise`

Exemple : `!create -t Addition -D "Calculez l'addition de deux nombres" -i "Deux nombres, un par ligne" -o "Le résultat de l'addition" -d 1 -h false`

#### Modifier un exercice existant

`!edit -t <titre> [-D -i -o -d -h]`

Voir *Créer un nouvel exercice* pour la liste des arguments.
Vous devez fournir un titre/nom d'exercice correct pour pouvoir l'editer.

#### Supprimer un exercice

`!remove <titre>`

`titre` doit être un exercice existant.

Alias : `!delete`, `!del`

Exemple: `!remove Addition`

#### Ajouter un test à un exercice

`!add -t <titre> -i <input> -o <output>`

|  Argument  |                     Description                   |
| ---------- | ------------------------------------------------- |
|-t --title  |**Obligatoire** Le titre de l'exercice à modifier  |
|-i --input  |**Obligatoire** L'entrée envoyée au programme      |
|-o --output |**Obligatoire** La sortie attendu par le programme |

Pour entrer plusieurs lignes, séparez-les par `\n`.

Alias: `!addTest`

Exemple: `!add -t Addition -i "1\n1" -o "2"`
