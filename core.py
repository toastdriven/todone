#!/usr/bin/en python
import datetime
import os
import unittest


TODO_FILENAME = 'todo.txt'
DONE_FILENAME = 'done.txt'
PROJECT_PREPEND_STRING = '@'


class ToDo(object):
    def __init__(self, data_path):
        self.data_path = os.path.expanduser(data_path)
        self.todotxt_path = os.path.join(self.data_path, TODO_FILENAME)
        self.donetxt_path = os.path.join(self.data_path, DONE_FILENAME)
        self.todos = []
        
        self.load_todo()
    
    def setup(self):
        """Ensure the data directory is in place."""
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)
        
        if not os.path.exists(self.todotxt_path):
            # 'Touch' the file. Works regardless of the file's existence (unlike os.utime).
            open(self.todotxt_path, 'a').close()
        
        if not os.path.exists(self.donetxt_path):
            # 'Touch' the file. Works regardless of the file's existence (unlike os.utime).
            open(self.todotxt_path, 'a').close()
    
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
    
    def verify_item_string(self, item_string):
        if not isinstance(item_string, basestring):
            raise AttributeError('Todo items must be strings.')
        
        if not item_string:
            raise AttributeError('Please provide todo item text.')
    
    def get(self, number, project=None):
        """Gets a todo item from the todo list by index."""
        todos = self.list(project=project)
        self.check_todo_number(number, todos)
        return todos[number]
    
    def add(self, item):
        """Appends a new todo item onto the todo list."""
        self.verify_item_string(item)
        self.todos.append(item)
        self.save_todo()
    
    def check_todo_number(self, number, todos=None):
        """Ensure the todo item number falls within the todo list."""
        if not todos:
            todos = self.todos
        
        if number < 0 or number > len(todos) - 1:
            raise RuntimeError('That todo item number is not within the todo list.')
    
    def get_true_offset(self, item_string):
        for index, item in enumerate(self.todos):
            if item == item_string:
                return index
        
        raise RuntimeError('The requested item no longer appears in the list. Data corruption?')
    
    def done(self, number, project=None):
        """Mark a todo item as complete."""
        self.check_todo_number(number)
        
        # If a project is specified, get the true offset (from the full list) to mark as complete.
        done_item = self.get(number, project)
        true_offset = self.get_true_offset(done_item)
        
        self.delete(true_offset)
        self.save_to_done(done_item)
    
    def delete(self, number, project=None):
        """Removes a todo item from the todo list permanently."""
        self.check_todo_number(number)
        
        # If a project is specified, get the true offset (from the full list) to mark as complete.
        delete_item = self.get(number, project)
        true_offset = self.get_true_offset(delete_item)
        
        del(self.todos[true_offset])
        self.save_todo()
    
    def edit(self, number, item, project=None):
        """Edits todo item within the todo list."""
        self.verify_item_string(item)
        self.check_todo_number(number)
        
        # If a project is specified, get the true offset (from the full list) to mark as complete.
        edit_item = self.get(number, project)
        true_offset = self.get_true_offset(edit_item)
        
        self.todos[true_offset] = item
        self.save_todo()
    
    def list(self, project=None):
        todos = []
        
        # DRL_TODO: Perhaps add date filtering?
        if project:
            project_filter = project
            
            if not project_filter.startswith(PROJECT_PREPEND_STRING):
                project_filter = "%s%s " % (PROJECT_PREPEND_STRING, project_filter)
            
            for item in self.todos:
                if item.startswith(project_filter):
                    todos.append(item)
        else:
            # Assume all todos are to be shown.
            todos = self.todos
        
        return todos


class TestToDo(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join('/tmp', 'todone_test')
        self.nuke_test_dir()
        self.todo = ToDo(self.data_path)
        self.sample_todos = ['One', 'Two', '@work Three', '@home Four', '@work Five']
    
    def nuke_test_dir(self):
        for filename in os.listdir(self.data_path):
            os.remove(os.path.join(self.data_path, filename))
        
        os.rmdir(self.data_path)
    
    def test_setup(self):
        self.todo.setup()
        self.assertEqual(os.path.exists(self.data_path), True)
    
    def test_save_to_done(self):
        self.todo.save_to_done("This is a test.")
        
        done_file_contents = open(os.path.join(self.data_path, DONE_FILENAME)).read()
        self.assert_(done_file_contents.startswith("This is a test. COMPLETED:"))
    
    def test_check_todo_number(self):
        self.todo.todos = self.sample_todos
        self.assertEqual(self.todo.check_todo_number(0), None)
        self.assertRaises(RuntimeError, self.todo.check_todo_number, -1)
        self.assertRaises(RuntimeError, self.todo.check_todo_number, 5)
    
    def test_list_tasks(self):
        # Check empty.
        self.assertEqual(self.todo.list(), [])
        
        self.todo.todos = self.sample_todos
        self.assertEqual(self.todo.list(), ['One', 'Two', '@work Three', '@home Four', '@work Five'])
        
        # Check project filtering.
        self.assertEqual(self.todo.list(project='work'), ['@work Three', '@work Five'])
        self.assertEqual(self.todo.list(project='home'), ['@home Four'])
        
        # Check non-existent project.
        self.assertEqual(self.todo.list(project='foo'), [])
    
    def test_add_task(self):
        self.todo.add('First Task')
        self.assertEqual(self.todo.list(), ['First Task'])

        self.todo.add('Second Task')
        self.assertEqual(self.todo.list(), ['First Task', 'Second Task'])
        
        self.todo.add('@work Third Task')
        self.assertEqual(self.todo.list(), ['First Task', 'Second Task', '@work Third Task'])
        
        # Fail if nothing provided.
        self.assertRaises(AttributeError, self.todo.add, '')
        
        # Fail on incorrect type.
        self.assertRaises(AttributeError, self.todo.add, ['foo', 'bar'])
    
    def test_load_todo(self):
        mock_todo_file_contents = "First\nSecond\nThird\n"
        mock_todo_file = open(os.path.join(self.data_path, TODO_FILENAME), 'w')
        mock_todo_file.write(mock_todo_file_contents)
        mock_todo_file.close()
        
        self.todo.load_todo()
        self.assertEqual(self.todo.list(), ['First', 'Second', 'Third'])
    
    def test_save_todo(self):
        self.nuke_test_dir()
        self.todo.todos = self.sample_todos
        self.todo.save_todo()
        
        todo_file_contents = open(os.path.join(self.data_path, TODO_FILENAME)).read()
        self.assertEqual(todo_file_contents, 'One\nTwo\n@work Three\n@home Four\n@work Five\n')
    
    def load_sample_todos(self):
        for item in self.sample_todos:
            self.todo.add(item)
    
    def test_edit_task(self):
        self.load_sample_todos()
        self.todo.edit(0, 'First Edited Task')
        self.assertEqual(self.todo.list(), ['First Edited Task', 'Two', '@work Three', '@home Four', '@work Five'])
        
        # Edit within a project.
        self.todo.edit(0, '@work Three Edited Task', project='work')
        self.assertEqual(self.todo.list(), ['First Edited Task', 'Two', '@work Three Edited Task', '@home Four', '@work Five'])
        
        # Fail if non-existent.
        self.assertRaises(RuntimeError, self.todo.edit, -1, 'Please Fail')
        self.assertRaises(RuntimeError, self.todo.edit, 5, 'Please Fail')
        self.assertRaises(RuntimeError, self.todo.edit, -1, 'Please Fail', 'work')
        self.assertRaises(RuntimeError, self.todo.edit, 2, 'Please Fail', 'work')
    
    def test_mark_task_done(self):
        self.load_sample_todos()
        self.todo.done(0)
        self.assertEqual(self.todo.list(), ['Two', '@work Three', '@home Four', '@work Five'])
        
        # Done within a project.
        self.todo.done(0, project='work')
        self.assertEqual(self.todo.list(), ['Two', '@home Four', '@work Five'])
        
        # Fail if non-existent.
        self.assertRaises(RuntimeError, self.todo.done, -1)
        self.assertRaises(RuntimeError, self.todo.done, 5)
        self.assertRaises(RuntimeError, self.todo.done, -1, 'work')
        self.assertRaises(RuntimeError, self.todo.done, 1, 'work')
    
    def test_delete_task(self):
        self.load_sample_todos()
        self.todo.delete(1)
        self.assertEqual(self.todo.list(), ['One', '@work Three', '@home Four', '@work Five'])
        
        # Delete within a project.
        self.todo.delete(0, project='work')
        self.assertEqual(self.todo.list(), ['One', '@home Four', '@work Five'])
        
        # Fail if non-existent.
        self.assertRaises(RuntimeError, self.todo.delete, -1)
        self.assertRaises(RuntimeError, self.todo.delete, 5)
        self.assertRaises(RuntimeError, self.todo.delete, -1, 'work')
        self.assertRaises(RuntimeError, self.todo.delete, 1, 'work')
    
    def test_get(self):
        self.load_sample_todos()
        
        # Test all.
        self.assertEqual(self.todo.get(0), 'One')
        self.assertEqual(self.todo.get(1), 'Two')
        self.assertEqual(self.todo.get(2), '@work Three')
        self.assertEqual(self.todo.get(3), '@home Four')
        self.assertEqual(self.todo.get(4), '@work Five')
        
        # Test within project.
        self.assertEqual(self.todo.get(0, project='work'), '@work Three')
        self.assertEqual(self.todo.get(1, project='work'), '@work Five')
        
        # Fail on non-existent.
        self.assertRaises(RuntimeError, self.todo.get, -1)
        self.assertRaises(RuntimeError, self.todo.get, 5)
        self.assertRaises(RuntimeError, self.todo.get, -1, 'work')
        self.assertRaises(RuntimeError, self.todo.get, 2, 'work')


if __name__ == '__main__':
    unittest.main()
    