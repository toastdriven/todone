======
Todone
======

:author: Daniel Lindsley
:date: 2008-12-13


Summary
-------

Todone is essentially todo lists done my way. Strongly influenced by 
http://todotxt.com/ but has a different syntax/commands. It features a stable 
(and well-tested) core that can support virtually any kind of frontend. A CLI 
frontend is included and a GUI frontend is in the works.


Requirements
------------

  * Python 2.5+ (Tested on 2.5 & 2.6)
  * A Unix-like OS (May work on Windows but untested)


Install
-------

From the Cheeseshop:

  * Not yet completed. This will occur once the GUI version is stable (or if 
    people request it sooner).

From source:

  * Place ``todone`` directory someplace on your PYTHONPATH.
  * For convenience, you may wish to copy ``bin/todone.py`` into 
    ``/usr/local/bin`` or elsewhere on your path. Remember to add execute 
    permissions to the script.


Usage
-----

The command-line version is located in the ``bin`` directory. As stated in the 
installation instructions, you may wish to copy this onto your PATH for easy 
access.

The CLI supports the following commands/options:

  ``add <todo item text>``
      Adds a new todo item to the list.
      
      Examples::
      
        todone.py add My first task. # Adds a general task.
        todone.py add @work Build stuff. # Adds the "Build stuff" task to the "work" project.
        todone.py add "This text uses (parentheses) and a single' quote." # Note that you must quote strings to avoid shell interpolation.
  
  
  ``delete <todo number from list> [project name]``
      Permanently deletes a todo item from the list. You probably want "done" instead.
      Prepend the "project name" with an '@'.
      
      Examples::
      
        todone.py delete 1 # Deletes the first task out of all tasks.
        todone.py delete 1 @work # Deletes the first task from the "work" project.
  
  
  ``done <todo number from list> [project name]``
      Marks a todo item as complete and archives it.
      Prepend the "project name" with an '@'.
      
      Examples::
      
        todone.py done 1 # Marks the first task out of all tasks as done.
        todone.py done 1 @work # Marks the first task from the "work" project as done.
  
  ``edit <todo number from list> [project name] <todo item text>``
      Edits a todo item within the list.
      Prepend the "project name" with an '@'.
      
      Examples::
      
        todone.py edit 1 # Edits the first task out of all tasks.
        todone.py edit 1 @work Test stuff thoroughly # Edits the first task from the "work" project.
  
  
  ``list [project name]``
      Without the "project name" option, shows all todo items.
      With the "project name" option, shows only todo items within that project.
      Prepend the "project name" with an '@'.
      
      Examples::
      
        todone.py list # Lists all tasks.
        todone.py list @work # Lists all tasks from the "work" project.
