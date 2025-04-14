# Career-recommendation-bot

This bot will help you find a job that works best for you.
All you need to do is enter your interests and skills.


## Installation
To install it you can simply run the following command to clone the repository:
```python
git clone https://github.com/NiceFrog12/Career-recommendation-bot
```
After that, you need to make a `config.py` file and create two variables. The first one will be called `python DATABASE = "nameofyourdatabase.db"`, but remember to add `.db` at the end of the string, so that it becomes a database file. The second variable is `TELEBOT_TOKEN`. It is also supposed to be a string, and you can get your token by talking to @botFather on Telegram!

## What can the bot do?
The current version of the bot has multiple commands to set up your experience.
<br>
<br>
This is the starting command. The bot will greet you, and tell you how to set it up.
```
/start
```
This command will register you into the database, which will therefore allow the bot to save skills, recommend proffessions, etc.
```
/register
```
This speaks for itself, the command will give you a list of all the currently supported commands
```
/help
```
This command allows you to select and save a skill that you possess (You can only add skills that are supported by the app)
```
/add
```
This command speaks for itself aswell. This will delete one of your currently selected skills.
```
/delete
```
This command shows all of the skills that were selected by you so far.
```
/show
```

On top of that, the bot catches every single message, and if it finds a keyword in it, that might correspond to a certain job or profession, it will let you know!

## How to modify the project?

### Adding skills

#### 1. Adding skills into the database
Firstly, you will have to add the new skills into the database. Make a new query with a unique id, and name the skill however you want. Go into the jobs table and add the id of the skill into the skill_id column next to the job_id of the corresponding job. Easy!

#### 2. Adding the skills into the bot
There is a supported_skills list at the very top. In the basic project it looks like this:
```python
supported_skills = ["People skills", "Coding", "Cooking", "Languages"]
```
Simply add the name of the skill into the list, but please make sure to do it the same way as you wrote it down in the database.

#### 3. Adding keywords (optional)
I would also do this if you are adding skills. In the dictionary next to the very bottom, you can find a name of a couple jobs and a list of keywords that might hint at an affinity for the job. You will have to manually add new jobs/keywords into the dictionary.
<br>
Dictionary at the start looks like this:
```python
keywords = {
    "Developer" : ["coding", "code", "languages", "culture"],
    "Cook" : ["cooking", "food"],
    "Nurse" : ["med", "medicine", "doctor", "nursing","care","healthcare"],
    "Teacher" : ["kids","teaching","sub",],
    "Translator" : ["language"]
}
```

### Adding jobs

#### Adding the job into the database
This is a little more complicated than adding skills. Firstly, you will have to make a query in the professions query, give it a unique id and the name for the job.
<br>
This is how the query is supposed to look like:
```
id, name
```
Next, head to the jobs table and create a query for the job. It needs a unique id, the job id (from the professions table), and skill id (from the skills table)
<br>
In the end it is suppoesed to look like this:
```csv
id, job_id, skill_id
```
You will have to create a new query for every skill that corresponds to the job. If you know python, however, you can go into logic.py and modify the default_inserts() function.

#### Adding the job into the bot
Go to logic.py and there at the very top you will see big one liners. Don't get scared, it's simple! You will have to add an id for a new job (the list that goes 1,2,3,4,5,etc.) like this:

```python
jobs_profession = [(_,) for _ in ([1,2,3,4,5,add,your,ids,here])]
```
And then you should add the name of the job with that id to another list above it like this:
```python
professions = [(_,) for _ in (["Nurse", "Developer", "Teacher", "Cook", "Translator","more","jobs","here"])]
```
<br>
After you have added the name of the job into the bot, you should make a new list inside the list of skills, with the skill ids corresponding to the job. Here is an example:

```python
jobs_skills_id = [(_,) for _ in ([[2,4], [1,4], [2,4], [3], [2,4], [id1, id2], [id3]])]
```

Don't worry if you don't know which ids correspond to which skills. Here is my cheatsheet:

```
1 : Coding
2 : People skills
3 : Cooking
4 : Languages
```
And just like that, you have added a new job into the mix!

#### Adding keywords (optional)
You will once again have to add keywords corresponding to the job, so that the user can stumble across it in an easier way by typing their interests into the chat. Go into the bottom of main.py and look for the dictionary, there, you can add a new query.
<br>
Here's how the dictionary looks like:
```python
keywords = {
    "Developer" : ["coding", "code", "languages", "culture"],
    "Cook" : ["cooking", "food"],
    "Nurse" : ["med", "medicine", "doctor", "nursing","care","healthcare"],
    "Teacher" : ["kids","teaching","sub",],
    "Translator" : ["language"]
}
```
