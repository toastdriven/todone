#!/usr/bin/en python
import datetime
import os
import unittest


class ToDo(object):
    def __init__(self, data_path):
        self.data_path = os.path.expanduser(data_path)
        self.todotxt_path = os.path.join(self.data_path, 'todo.txt')
        self.donetxt_path = os.path.join(self.data_path, 'done.txt')
        self.todos = []
    
    def setup(self):
        """Ensure the data directory is in place."""
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)
    
    def load_todo(self):
        self.setup()
        todo_file = open(self.todotxt_path, 'r')
        self.todos = [line.strip() for line in todo_file.readlines()]
        todo_file.close()
    
    def save_todo(self):
        self.setup()
        todo_file = open(self.todotxt_path, 'w')
        
        for item in self.todos:
            todo_file.write("%s\n" % item)
        
        todo_file.close()
    
    def save_to_done(self, item):
        self.setup()
        completed = datetime.datetime.now().isoformat()
        done_file = open(self.donetxt_path, 'a')
        done_file.write("%s COMPLETED:%s\n" % (item, completed))
        done_file.close()
    
    def add(self, add_string):
        """Appends a new todo item onto the todo list."""
        self.todos.append(add_string)
        self.save_todo()
    
    def check_todo_number(self, number):
        """Ensure the todo item number falls within the todo list."""
        if number < 0 or number > len(self.todos):
            raise RuntimeError('That todo item number is not within the todo list.')
    
    def done(self, number):
        """Mark a todo item as complete."""
        self.check_todo_number(number)
        done_item = self.todos[number]
        self.delete(number)
        self.save_todo()
        self.save_to_done(done_item)
    
    def delete(self, number):
        """Removes a todo item from the todo list permanently."""
        self.check_todo_number(number)
        del(self.todos[number])
        self.save_todo()
    
    def edit(self, number, item):
        """Edits todo item within the todo list."""
        self.check_todo_number(number)
        self.todos[number] = item
        self.save_todo()
    
    def list(self, project=None):
        todos = []
        
        # DRL_TODO: Perhaps add date filtering?
        if project:
            project_filter = project
            
            if not project_filter.startswith('@'):
                project_filter = "@%s " % project_filter
            
            for item in self.todos:
                if item.startswith(project_filter):
                    todos.append(item)
        else:
            # Assume all todos are to be shown.
            todos = self.todos
        
        return todos


class TestToDo(unittest.TestCase):
    def setUp(self):
        # DRL_FIXME: This need mocking to replace file access.
        self.data_path = os.path.join('~', '.todone_test')
        self.todo = ToDo(self.data_path)
        self.sample_todos = ['One', 'Two', '@work Three', '@home Four', '@work Five']
    
    def test_list_tasks(self):
        # Check empty.
        self.assertEqual(self.todo.list(), [])
        
        self.todo.todos = ['One', 'Two', '@work Three', '@home Four', '@work Five']
        self.assertEqual(self.todo.list(), ['One', 'Two', '@work Three', '@home Four', '@work Five'])
        
        # Check project filtering.
        self.assertEqual(self.todo.list(project='work'), ['@work Three', '@work Five'])
        self.assertEqual(self.todo.list(project='home'), ['@home Four'])
    
    def test_add_task(self):
        # DRL_FIXME: Move to a real unit test and create a command-line script.
        # Test.
        self.todo.add('First Task')
        self.assertEqual(self.todo.list(), ['First Task'])

        self.todo.add('Second Task')
        self.assertEqual(self.todo.list(), ['First Task', 'Second Task'])
        
        self.todo.add('@work Third Task')
        self.assertEqual(self.todo.list(), ['First Task', 'Second Task', '@work Third Task'])
    
    def test_load_todo(self):
        # DRL_FIXME: This need mocking to replace file access.
        self.todo.load_todo()
    
    def test_save_todo(self):
        # DRL_FIXME: This need mocking to replace file access.
        self.todo.save_todo()
    
    def load_sample_todos(self):
        for item in self.sample_todos:
            self.todo.add(item)
    
    def test_edit_task(self):
        self.load_sample_todos()
        self.todo.edit(0, 'First Edited Task')
        self.assertEqual(self.todo.list(), ['First Edited Task', 'Two', '@work Three', '@home Four', '@work Five'])
    
    def test_mark_task_done(self):
        self.load_sample_todos()
        self.todo.done(0)
        self.assertEqual(self.todo.list(), ['Two', '@work Three', '@home Four', '@work Five'])
    
    def test_delete_task(self):
        self.load_sample_todos()
        self.todo.delete(1)
        self.assertEqual(self.todo.list(), ['One', '@work Three', '@home Four', '@work Five'])


if __name__ == '__main__':
    unittest.main()
    