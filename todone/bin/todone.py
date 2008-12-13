#!/usr/bin/env python
"""A command-line front-end for todone."""
import datetime
import os
import sys
from core import ToDo, PROJECT_PREPEND_STRING


def usage():
    print """Usage: %(filename)s <command> [options]
    
Available Commands:
    add <todo item text>
        Adds a new todo item to the list.
    
    delete <todo number from list> [project name]
        Permanently deletes a todo item from the list. You probably want "done" instead.
        Prepend the "project name" with an '%(project_prepend)s'.
    
    done <todo number from list> [project name]
        Marks a todo item as complete and archives it.
        Prepend the "project name" with an '%(project_prepend)s'.
    
    edit <todo number from list> [project name] <todo item text>
        Edits a todo item within the list.
        Prepend the "project name" with an '%(project_prepend)s'.
    
    list [project name]
        Without the "project name" option, shows all todo items.
        With the "%(project_prepend)sproject name" option, shows only todo items within that project.
    """ % {'filename': os.path.basename(sys.argv[0]), 'project_prepend': PROJECT_PREPEND_STRING}
    sys.exit()


def add_item(todo, remaining_args):
    item = " ".join(remaining_args)
    todo.add(item)
    print "TODO: Added '%s'." % item
    print


def delete_item(todo, remaining_args):
    number = int(remaining_args.pop(0))
    correct_offset = number - 1
    project = None
    
    if remaining_args:
        project = remaining_args.pop(0)
        
        if project.startswith(PROJECT_PREPEND_STRING):
            project = project.replace(PROJECT_PREPEND_STRING, '')
    
    old_item = todo.get(correct_offset, project)
    todo.delete(correct_offset, project)
    print "TODO: Deleted #%s '%s'." % (number, old_item)
    print


def mark_item_as_done(todo, remaining_args):
    number = int(remaining_args.pop(0))
    correct_offset = number - 1
    project = None
    
    if remaining_args:
        project = remaining_args.pop(0)
        
        if project.startswith(PROJECT_PREPEND_STRING):
            project = project.replace(PROJECT_PREPEND_STRING, '')
    
    old_item = todo.get(correct_offset, project)
    todo.done(correct_offset, project)
    print "TODO: Marked #%s '%s' as done." % (number, old_item)
    print


def edit_item(todo, remaining_args):
    number = int(remaining_args.pop(0))
    correct_offset = number - 1
    item = " ".join(remaining_args)
    project = None
    
    if remaining_args:
        # Note that we're not popping, just checking it.
        project_filter = remaining_args[0]
        
        if project_filter.startswith(PROJECT_PREPEND_STRING):
            project = project_filter.replace(PROJECT_PREPEND_STRING, '')
    
    todo.edit(correct_offset, item, project)
    print "TODO: Edited #%s '%s'." % (number, item)
    print


def list_todos(todo, remaining_args):
    project_filter = None
    
    if remaining_args:
        project_filter = remaining_args.pop(0).replace(PROJECT_PREPEND_STRING, '')
        todos = todo.list(project=project_filter)
    else:
        todos = todo.list()
    
    if not todos:
        print "No todo items found."
        print
        return
    
    if project_filter:
        project_header = "Project: %s" % project_filter
        print project_header
        print "-" * len(project_header)
    
    for index, todo in enumerate(todos):
        if project_filter:
            todo = todo.replace("%s%s " % (PROJECT_PREPEND_STRING, project_filter), '')
        
        print "%s. %s" % (index + 1, todo)
    
    print


def process_command(todo, command, remaining_args):
    commands = {
        'add': add_item,
        'delete': delete_item,
        'done': mark_item_as_done,
        'edit': edit_item,
        'list': list_todos,
    }
    
    if not command in commands:
        print "Unrecognized command."
        usage()
    
    try:
        commands[command](todo, remaining_args)
    except (RuntimeError, AttributeError, IndexError), e:
        print "Command failed: %s" % e.args
        print


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        usage()
    
    data_path = os.path.join('~', '.todone')
    todo = ToDo(data_path)
    
    command = sys.argv[1]
    remaining_args = sys.argv[2:]
    
    process_command(todo, command, remaining_args)
