# Discord-ProgramCompiler
Un bot pour compiler et exécuter les programmes envoyés sur discord.
**Ce bot a été créé pour un challenge privé. Si vous voulez l'utiliser, vous devrez certainement le modifier.**

Ce bot accepte les fichiers Python, Java, NodeJS, C, C++, C#, F# and Rust. Si vous voulez en ajouter, proposez-le moi !

**Les entrées sont données par __l'entré standard__ (*stdin*), et pas par arguments !**

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

Ajouter `test` enverra l'exercice sans être classé. Les points ne conteront pas dans le classement.

Une fois que le test a été envoyé, il va être exécuté et testé avec les tests de l'exercice. Vous serez averti des erreurs, s'il y en a.

## Commandes Utilisateur

#### Lister tous les tests disponibles

`!list [langage]`

Si `langage` est spécifié, envoie la liste de tous les exercices de ce langage.
S'il ne l'est pas, envoie la liste de tous les exercices disponibles dans tous les langages.

Alias : `!liste`, `!listes`

#### Afficher les détails d'un exercice

`!detail <titre>`

Envoie les détails d'un exercice spécifique.

Alias : `!exercice`, `!exercise`, `!details`

#### Afficher votre profil

`!profil [utilisateur]`

Si `utilisateur` est spécifié, envoie ses détails (nom, image, score total, liste des exercices participés).
S'il ne l'est pas, envoie votre profil.

`utlisateur` peut être de la forme d'un Prénom-Nom (`!profil "Jean Pierre"`), d'un identifiant discord (`!profil 704416295914182878`), ou d'une mention (`!profil @JeanPierre#4242`).

Alias: `!profile`, `!me`

#### Classement

`!classement [langage]`

Si `langage` est spécifié, envoie le classement de tous les exercices de ce langage, trié par score du langage.
S'il ne l'est pas, envoie le classement général de tous les participants, trié par score total.

Alias: `!leaderboard`, `!top`


## Commandes Administrateur

Elles fonctionnent de la même manière que les commandes shell, avec des arguments comme `-a "Ceci est un argument"`.

#### Créer un nouvel exercice

`!create -t <titre> [-D -i -o -d -h -l -T -e]`

|    Argument    |                     Description                     | Défaut |
| -------------- | --------------------------------------------------- | ------ |
|-t --title      |**Obligatoire** Le titre de l'exercice               |        |
|-D --description|La description de l'exercice                         | *Vide* |
|-i --input      |Description des entrées envoyées par l'exercice      | *Vide* |
|-o --output     |Description des sorties attendues par l'exercice     | *vide* |
|-d --difficulty |La difficulté de l'exercice (entre 1 et 10)          |   1    |
|-h --hidden     |Si la sortie attendue doit être masquée ou non       | false  |
|-l --language   |Indiquer le langage de l'exercice (Python, Java, C)  |  tous  |
|-T --timeout    |Temps maximum d'exécution (en secondes) de l'exercice|   10   |
|-e --enable     |Si l'exercice est disponible ou non                  | true   |

Les participants **ne peuvent pas** utiliser `-h` (true by default), `-l` (all), `-T` (10s) and `-e` (false).
L'exercice sera soumit à un administrateur pour approbation.

Alias : `!createTest`, `!createExercise`

Exemple : `!create -t Addition -D "Calculez l'addition de deux nombres" -i "Deux nombres, un par ligne" -o "Le résultat de l'addition" -d 1 -h false -l Java -T 5`

#### Modifier un exercice existant

`!edit -t <titre> [-D -i -o -d -h -l -T -e]`

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
**Ni l'entrée ni la sortie ne doivent finir par un `\n` !!**

Alias: `!addTest`

Exemple: `!add -t Addition -i "1\n1" -o "2"`

#### Afficher les tests d'un exercice

`!see <titre> [quantité]`

Si `quantité` est spécifiée, envoie les `quantité` premiers tests de l'exercice.
Sinon, envoie tous les tests de cet exercice.
