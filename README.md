# Discord-ProgramCompiler
A bot to compile and execute program sending through discord.
**This bot was created for a private challenge. You might edit it if you want to use it.**

The bot only allows Python, Java and C languages. If you want more, request it to me!

## Submition

To submit a test, send the file by private message to `ProgramCompiler#3290`.

- If their is only one file, its name must be the same as the exercise your submiting to.
- If their are multiple files to your exercise's project, you must zip it like following. The main file (the executed one) must have the exercice name, and the zip too.
```
ExerciseName.zip
├── ExerciseName.ext
└── OtherRandomFile.ext
```
`ExerciceName` is the exact name of the exercise you are submiting for.
`.ext` is the extension of your file. For exemple, if you wrote it in Java, `.ext` should be `.java`

Once the test is submitted, it will be run and tested with the tests of the exercices. You will be warned of error(s) there are any.

## Commands

### Users Commands

#### List all available tests/exercises

`!list`

Send a list of all available exercises.

Aliases: `!liste`, `!listes`, `!exercice`, `!exercices`, `!exercise` , `!exercises`

#### See your profile

`!profile`

Send your profile details (name, picture, total score, list of participate exercises).

Aliases: `!profil`, `!me`

#### Leaderboard

`!leaderboard`

Send the leaderboard of all participants, ordered by total score.

Aliases: `!classement`, `!top`



### Admin Commands

They work like shell commands, with arguments like `-a "This an argument"`.

#### Create a new test/exercise

`!create -t <title> [-D -i -o -d -h]`

|    Argument    |                  Description                    |Default|
| -------------- | ----------------------------------------------- | ----- |
|-t --title      |**Needed** The title of the exercice             |       |
|-D --description|The description of the exercice                  |*Empty*|
|-i --input      |Description of the input sending by the exercice |*Empty*|
|-o --output     |Description of the needed output of the exercice |*Empty*|
|-d --difficulty |The difficulty of the exercice (between 1 and 10)|   1   |
|-h --hidden     |If the needed output of a test is hide when error| false |

Aliases : `!createTest`, `!createExercise`

Example : `!create -t Addition -D "Calculate the addition of two number" -i "Two numbers, one per line" -o "The result of addition" -d 1 -h false`

#### Edit an existing test/exercise

`!edit -t <title> [-D -i -o -d -h]`

See *Create a new test/exercise* for argument list.
You must provide a correct exercise title to edit this test.

#### Remove an existing test/exercise

`!remove <title>`

`title` must be an existing exercise to be deleted.

Aliases : `!delete`, `!del`

Example: `!remove MySuperExercise`

#### Add a test entry to an existing exercise

`!add -t <title> -i <input> -o <output>`

|  Argument  |                 Description                |
| ---------- | ------------------------------------------ |
|-t --title  |**Needed** The title of the exercice        |
|-i --input  |**Needed** The input sended to the program  |
|-o --output |**Needed** The output sended to the program |

To enter mutliple lines, add a `\n` character.

Alias: `!addTest`

Example: `!add -t Addition -i "1\n1" -o "2"`
