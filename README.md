How To Build Command Line Applications with Python
========================================

Adapted by Peter Turner from [How To Build Command Line Applications with Node.js](https://www.digitalocean.com/community/tutorials/how-to-build-command-line-applications-with-node-js) by Chris Ganga

In this tutorial you'll build two small CLI applications in Python:

1. Quote Of the Day tool that retrieves quotes of the day from [https://quotes.rest/qod](https://quotes.rest/qod)
2. A To-Do List app that uses JSON to save data.

## Prerequisites

To complete this tutorial, you will need:

- A local development environment for Python. Follow [Properly Installing Python](https://docs.python-guide.org/starting/installation/)

## Step 1 — Understanding the Shebang

Whenever you look at any scripting file, you'll see characters like these in the beginning of the file:

file.sh
```bash
#!/usr/bin/env sh
```
Or this:

file.js
```bash
#!/usr/bin/env node
```

They serve as a way for your operating system program loader to locate and use toe parse the correct interpreter for your executable file. This only works in Unix Systems though.

From [Wikipedia](https://en.wikipedia.org/wiki/Shebang_(Unix)):
> In computing, a shebang is the character sequence consisting of the characters number sign and exclamation mark (#!) at the beginning of a script.

Python has its own supported shebang characters

Create a new file in your editor called `logger.py`:

```
$ nano logger.py
```

Add the following code:

```python
#!/usr/bin/env python

print("I am a logger")
```

The first line tells the program loader to parse this file with Python. The second line prints text to the screen.

You can try and run the file by typing this in your terminal. You’ll get a permission denied for execution.

```
$ ./logger.py
```
Output
```
zsh: permission denied: ./logger.py
```

You need to give the file execution permissions. You can do that with:

```
$ chmod +x logger.py
```
Then when you run:

```
$ ./logger.py
```

you'll see the output:

```
I am a logger
```

You could have run this program with `python logger`, but adding the shebang and making the file executable on its own lets you avoid typing `python` to run it.

## Creating the Quote of the Day App

Let's create a directory and call it `qod`.

```
$ mkdir qod
$ cd qod
```

Next, we know we need to make requests to the quotes server, so we can use an existing library to do just this. We'll use [requests](https://requests.kennethreitz.org/en/master/)

```
$ pip install requests
```

We'll also add [pyfancy](https://github.com/ilovecode1/Pyfancy-2), a library to help us print color in the terminal.

```
$ pip install pyfancy
```

We then write the logic needed to retrieve these quotes.

Create a new file called `qod.py`

```
$ touch qod.py
```

Open `qod.py` in your favorite text editor, and add the following code to specify the shebang, load the libraries, and store the API URL:

```python
#!/usr/bin/env python

import requests
from pyfancy.pyfancy import pyfancy

url = "https://quotes.rest/qod"
```

Next, add this code to make a `GET` request to the API:

```python
res = requests.get(url)
data = res.json()
if res.status_code == 200:
  quote = data["contents"]["quotes"][0]["quote"]
  author = data["contents"]["quotes"][0]["author"]
  print(pyfancy().green(quote + " - " + author).get())
else:
  print(pyfancy().red(data["error"]["message"]).get())
```

Save the file.

Change the file permissions so the file is executable:

```
$ chmod +x qod.py
```

Then run the application.

```
$ ./qod.py
```

You'll see a quote:

```
Logic will get you from A to B. Imagination will take you everywhere. - Albert Einstein
```

This example shows you can use external libraries in your CLI applications.

Now let's create a CLI program that saves data.

## Creating a To-Do List

This will be a bit more complex, as it will involve data storage and retrieval. Here's what we're trying to achieve.

1. We need to have a command called `todo`
2. The command will take in four arguments: `new`, `get`, `complete`, and `help`.

So the available commands will be

```
./todo new // create a new todo
./todo get // get a list of all your todos
./todo complete // complete a todo item
./todo help // print the help text
```

For this program, we're going to be using [Pipenv](https://pipenv.pypa.io/en/latest/), which is a tool for Python projects, similar to NPM for NodeJS, to keep the dependencies required by different projects in separate places.

First of all, install `Pipenv` with:

```
$ brew install pipenv
```

Then, create a `todo` folder, and instantiate a Python 3 virtual environment using `Pipenv`

```
$ mkdir todo
$ cd todo
$ pipenv --three
```

You'll see that `Pipenv` created `Pipfile` and `Pipfile.lock` files. These help `Pipenv` keep track of dependencies for this program

Next, install `pyfancy` again, so that you can print with colors.

```
$ pipenv install pyfancy
```

Next, create the file `todo.py`

```
$ touch todo.py
```

Open `todo.py` in your text editor, and add this to the file:

```python
#!/usr/bin/env pipenv run python

import sys

print(str(sys.argv))
```

Notice the different shebang at the beginning of the file. Since we're using `Pipenv`, we use it's `pipenv run python` command as the context in which to run our `todo.py`

Back in the terminal, give the file executable permissions, and run it with a `new` command:

```
$ chmod +x ./todo.py
$ ./todo.py new
```

You're going to get this output:

```
['./todo.py', 'new']
```

Notice that the first string in the array is the program file itself, but the rest of the array contains the arguments passed; in this case it's `new`.

To be safe, let's restrict these, so that we can only accept the correct number of arguments, which is one, and they can only be `new`, `get`, `complete`, and `help`

In `todo.py`:

```python
#!/usr/bin/env pipenv run python

import sys
from pyfancy.pyfancy import pyfancy

args = sys.argv

# usage represents the help guide
def usage():
  usageText = """
  todo helps you manage your todo tasks

  usage:
    todo <command>

  commands can be:

  new:      used to create a new todo
  get:      used to retrieve your todos
  complete: used to mark a todo as complete
  help:     used to print the usage guide
  """

  print(usageText)

# used to log errors to the console in red color
def errorLog(error):
  print(pyfancy().red(error).get())

# we make sure the length of the arguments is exactly two
if len(args) > 2:
  errorLog("only one argument can be accepted")
  usage()
```

We've first assigned the command line argument to a variable, and then we check at the bottom that the length is not greater than three.

We've also added a `usage` string, that will print what the command line app expects. Run the app with wrong parameters like below

```
$ ./todo.py new todo
```

Output:

```
only one argument can be accepted

  todo helps you manage your todo tasks

  usage:
    todo <command>

  commands can be:

  new:      used to create a new todo
  get:      used to retrieve your todos
  complete: used to mark a todo as complete
  help:     used to print the usage guide
```

If you run it with one parameter, it will not print anything, which means the code passes.

Next, we need to make sure only the four commands are expected, and everything else will be printed as invalid.

We'll check the command, and only act on ones we recognize. We'll add an `else:` clause to the length check we just wrote, plus logic to recognize each command:

```python
# we make sure the length of the arguments is exactly two
if len(args) > 2:
  errorLog("only one argument can be accepted")
  usage()
else:
  # check that the passed in command is one we recognize
  if len(args) > 1:
    arg = args[1]
    if arg == "help":
      usage()
    elif arg == "new":
      pass
    elif arg == "get":
      pass
    elif arg == "complete":
      pass
    else:
      errorLog("invalid command passed")
      usage()
```

Now, if we run the app with an invalid command, we get this:

```
$ ./todo.py ne
```

Output:

```
invalid command passed

  todo helps you manage your todo tasks

  usage:
    todo <command>

  commands can be:

  new:      used to create a new todo
  get:      used to retrieve your todos
  complete: used to mark a todo as complete
  help:     used to print the usage guide
```

We have set up an `if` statement which will call functions based on what command has been passed in. If you look closely, you'll notice the `help` case just calls the `usage()` function.

The `new` command will create a new todo item and save it in a JSON file. The library we will use is [flata](https://github.com/harryho/flata)

Let's install `flata` and add initialization code to `todo.py` under our other imports at the top of the file.

```
$ pipenv install flata
```

todo.py

```python
#...
from flata import Flata, where
from flata.storages import JSONStorage
db = Flata('db.json', storage=JSONStorage)
db.table('todos')
#...
```

Next, we'll add a function to prompt the user to input data. Add this in `todo.py` where other functions are defined, before the if statements

```python
#...
def newTodo():
  print(pyfancy().blue("Type in your todo\n").get())
  for line in sys.stdin:
    print(line)
    break
#...
```

We're using `pyfancy` to get the blue color for the prompt. And `sys.stdin` to read the user's input, then we'll log the result.

To use this new function, call it in our program flow `if` statement under `elif arg == "new":`, replacing the existing `pass` keyword

```python
  # check that the passed in command is one we recognize
  if len(args) > 1:
  #...
    elif arg == "new":
      newTodo()
  #...
```

When you run the app now with the `new` command, you will be prompted to add in a tood. Type and press enter, and the program will print back what you entered.

```
$ ./todo.py new
```

Output

```
Type in your todo
This is my todo  aaaaaaw yeah
This is my todo  aaaaaaw yeah
```

Notice also, that a `db.json` file has been created in your file system, and it has a todos property

Next, let's add in the logic for adding a todo. Modify the `newTodo` function:

```python
#...
def newTodo():
  print(pyfancy().blue("Type in your todo\n").get())
  for line in sys.stdin:
    db.get('todos').insert({
        'title': line.rstrip(),
        'complete': False
      })
    break
#...
```

Run the code again

```
$ ./todo.py new
```
Output:
```
Type in your todo
Take a Scotch course
```

If you look at your `db.json`, you'll see the todo added. Add two more, so that we can retrieve them in the next `get` command. Here's what the db.json file looks like with more records:

```json
{
  "todos": [{
    "title": "Take a Scotch course",
    "complete": false,
    "id": 1
  }, {
    "title": "Travel the world",
    "complete": false,
    "id": 2
  }, {
    "title": "Rewatch Avengers",
    "complete": false,
    "id": 3
  }]
}
```

After creating the `new` command, you should already have an idea of how to implement the `get` command.

Create a function that will retrieve the todos.

```python
#...
def getTodos():
  todos = db.get('todos')
  for todo in todos:
    print(str(todo["id"]) + '. ' + todo["title"])
#...

  # check that the passed in command is one we recognize
  if len(args) > 1:
  #...
    elif arg == "get":
      getTodos()
  #...
```

Run the command again:

```
$ ./todo.py get
```

Output

```
1. Take a Scotch course
2. Travel the world
3. Rewatch Avengers
```

You can make the color green by using `print(pyfancy().green(str(index) + '. ' + todo["title"]).get())`

Next, add the `complete` command, which is a little bit complicated.

You can do it in two ways:

1. Whenever a user types in `./todo.py complete`, we could list all the todos, and then ask them to type in the number/key for the todo to mark as complete.
2. We can add in another parameter, so that a user can type in `./todo.py get`, and then choose the task to mark as complete with a parameter, such as `./todo.py complete 1`.

Since you learned how to do the first method when you implemented the `new` command, we'll look at option 2.

With this option, the command `./todo.py complete 1` will fail our validity check for the number of commands given. We therefore first need to handle this. Change the function that checks the length of arguments to this:

```python
#...
# we make sure the length of the arguments is exactly two
if len(args) > 2 and args[1] != "complete":
  errorLog("only one argument can be accepted")
  usage()
#...
```

This approach uses truth tables wgre `True and False` will equal `False` and the code will be skipped when `complete` is passed.

We'll then grab the value of the new argument and make the value of todo as completed. Add this code to `todo.py` where other functions are defined.

```python
#...
def completeTodo():
  # check that length
  if len(args) != 3:
    errorLog("invalid number of arguments passed for complete command")
  else:
    try:

      # check if the value is a number
      n = int(args[2])
      todosLength = len(db.get('todos'))

      # check if the correct length of values has been passed
      if (n > todosLength):
        errorLog("invalid number passed for complete command")
      else:

        # update the todo item marked as complete
        db.get('todos').update({'complete': True}, where('id') == n)
    except ValueError:
      errorLog("please provide a valid number for complete command")
#...
```

Also, update the `if` block to call this function when the `complete` command is passed in, by replacing `pass` with `completeTodo()`

```python
#...
    elif arg == "complete":
      completeTodo()
#...
```

When you run this with `./todo.py complete 2`, you'll notice your `db.json` has changed to this, marking the second task as complete:

```json
{
  "todos": [{
    "title": "Take a Scotch course",
    "complete": false,
    "id": 1
  }, {
    "title": "Travel the world",
    "complete": true,
    "id": 2
  }, {
    "title": "Rewatch Avengers",
    "complete": false,
    "id": 3
  }]
}
```

The last thing we need to do is change `./todo.py get` to indicate which tasks are completed. We'll use an emoji checkmark for this. Modify `getTodos()` with this code:

```python
#...
def getTodos():
  todos = db.get('todos')
  for todo in todos:
    todoText = str(todo["id"]) + ". " + todo["title"]
    if todo["complete"] == True:
      print(pyfancy().dim(todoText + ' ✔').get()) # add a check mark
    else:
      print(pyfancy().green(todoText).get())
#...
```

When you now type in the `./todo.py get` you'll see this:

```
1. Take a Scotch course
2. Travel the world ✔
3. Rewatch Avengers
```

## Conclusion

You've written two CLI applications in Python.

Once your app is working, you can create a symbolic link to it in a folder that's in your PATH, so you can run it from anywhere.

The command to run would take this form:

```
$ ln -s /full/path/to/todo.py /full/path/to/command/todo
```

Where the path to the command `todo` is a folder that's in your `PATH` environment variable.

For me, with MacOS and Python 3.7 installed via Homebrew, it ends up being:

```
$ ln -s ~/Code/todo/todo.py ~/Library/Python/3.7/bin/todo
```

Your paths may differ, but once the symlink is created, you should be able to run the program from any folder using simply `todo` instead of `./todo.py`

```
$ todo complete 1
$ todo get
```

Output:

```
1. Take a Scotch course ✔
2. Travel the world ✔
3. Rewatch Avengers
```

As an additional exercise, try to expand the `todo` app, perhaps by adding a `delete` command.