# Discord-ProgramCompiler
A bot to compile and execute program sending through discord.
**This bot was created for a private challenge. You might edit it if you want to use it.**

The bot allows Python, Java, NodeJS, C, C++, C#, F# and Rust languages. If you want more, request it to me!

**The input is through __standard input__ (*stdin*), and not through args**!

## Submission

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

Write `test` on the submit message to submit it as unranked. Points will not count.

Once the test is submitted, it will be run and tested with the tests of the exercices. You will be warned of error(s) there are any.

## Users Commands

#### List all available tests/exercises

`!list [language]`

If `language` specified, send list of all exercice of this language.
If not, send list of all available exercises in any language.

Aliases: `!liste`, `!listes`

#### See details of a test/exercise

`!detail <title>`

Send details of a specific exercise.

Aliases: `!exercice`, `!exercise`, `!details`

#### See your profile

`!profile [user]`

If `user` is specified, send the user's profile detail (name, picture, total score, list of participate exercises).
If not, send yours.

`user` can be a FirstName-LastNane (`!profile "Jean Pierre"`), a discord ID (`!profile 704416295914182878`), or a tag (`!profile @JeanPierre#4242`).

Aliases: `!profil`, `!me`

#### Leaderboard

`!leaderboard [language]`

If `language` specified, send the leaderboard for all exercises of this language, ordered by language's score.
If not, send general leaderboard, ordered by total score.

Aliases: `!classement`, `!top`


## Admin Commands

They work like shell commands, with arguments like `-a "This an argument"`.

#### Create a new test/exercise

`!create -t <title> [-D -i -o -d -h -l -T -e]`

|    Argument    |                         Description                       |Default|
| -------------- | --------------------------------------------------------- | ----- |
|-t --title      |**Needed** The title of the exercice                       |       |
|-D --description|The description of the exercice                            |*Empty*|
|-i --input      |Description of the input sending by the exercice           |*Empty*|
|-o --output     |Description of the needed output of the exercice           |*Empty*|
|-d --difficulty |The difficulty of the exercice (between 1 and 10)          |   1   |
|-h --hidden     |If the needed output of a test is hide when error          | false |
|-l --language   |Indicate the language of the exercice (Python, Java, C)    |  all  |
|-T --timeout    |The maximum execution duration (in seconds) of the exercice|   10  |
|-e --enable     |If the exercice is available or not                        | true  |

Users **can't** use `-h` (true by default), `-l` (all), `-T` (10s) and `-e` (false).
Exercise will be submited to administrator for approval.

Aliases : `!createTest`, `!createExercise`

Example : `!create -t Addition -D "Calculate the addition of two number" -i "Two numbers, one per line" -o "The result of addition" -d 1 -h false -l Java -T 5 -e True`

#### Edit an existing test/exercise

`!edit -t <title> [-D -i -o -d -h -l -T -e]`

See *Create a new test/exercise* for argument list.
You must provide a correct exercise title to edit this test.

#### Remove an existing test/exercise

`!remove <title>`

`title` must be an existing exercise to be deleted.

Aliases : `!delete`, `!del`

Example: `!remove Addition`

#### Add a test entry to an existing exercise

`!add -t <title> -i <input> -o <output>`

|  Argument  |                 Description                |
| ---------- | ------------------------------------------ |
|-t --title  |**Needed** The title of the exercice        |
|-i --input  |**Needed** The input sended to the program  |
|-o --output |**Needed** The output sended to the program |

To enter mutliple lines, add a `\n` character.
**Neither input nor output should end by `\n` !!**

Alias: `!addTest`

Example: `!add -t Addition -i "1\n1" -o "2"`

#### See the test entries of an existing exercise

`!see <title> [amount]`

If `amount` is specified, send the `amount` firsts test entries.
If not, send all test entries.
