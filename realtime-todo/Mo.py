"""With Mo you can chronologically add your tasks, modify them and mark if they have been completed.
  A cleanup feature enables you to delete completed tasks which are more than a week old - unless
  you have flagged them as 'protected'."""

from collections import OrderedDict
import datetime
import os
from peewee import *
import time
from time import sleep

db = SqliteDatabase('to_do_list.db')
print("Mo [Version 1.0.0.1] | © 2019 Nomeon Apps | All rights reserved. ")
print("\n")
user=input("Name please: ")
print("\n")
print("Hi", user, "! I'm Mocli. A to-do list manager for your work. ")
time.sleep(1)


time.sleep(1)
class ToDo(Model):
    """Model for creating to-do items. 'done' indicates that it's been completed,
    'protected' makes it immune to cleanup"""
    task = CharField(max_length=255)
    timestamp = DateTimeField(default=datetime.datetime.now)
    done = BooleanField(default=False)
    protected = BooleanField(default=False)

    class Meta:
        database = db


def clear():
    """Clear the display: """
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize():
    """Connect to database, build tables if they don't exist"""
    db.connect()
    db.create_tables([ToDo], safe=True)


def view_entries(index, entries, single_entry):
    """"View to-do list"""
    clear()

    index = index % len(entries)  # determines which entry is selected for modification
    if single_entry:  # to see only 1 entry
        entries = [entries[index]]
        index = 0
    else:
        print('-' * 20)
        print('Stuff to do: ')
        print('-' * 20)
    prev_timestamp = None

    for ind, entry in enumerate(entries):
        timestamp = entry.timestamp.strftime('[Date: %d/%B/%Y]')
        print("\n")
        if timestamp != prev_timestamp:  # same timestamps get printed only once
            print(timestamp)
            print('-' * 20)
            prev_timestamp = timestamp

        if ind == index:  # placing the selection tick
            tick = '>>>  '
        else:
            tick = ' '
        print('{}{}'.format(tick, entry.task), end='')
        if entry.done:
            print(' (Item action complete)', end='')
        if entry.protected:
            print('  - [protected]', end='')
        else:
            print(" - [not protected]", end='')    
        print('')
        
        

    return entries  # so that we can modify the given entry if needed
    print('-' * 20)
def add_entry(index, entries):
    """Add a new item."""

    new_task = input('To do: ')
    print('\n')
    if input('Protect [y/n]? ').lower().strip() == 'y':
        protect = True
    else:
        protect = False
        
    ToDo.create(task=new_task,
                protected=protect)


def modify_entry(index, entries):
    """Modify selected item."""
    entry = view_entries(index, entries, True)[0]
    print('\n')

    for key, value in sub_menu.items():
        print('{}) {}'.format(key, sub_menu[key].__doc__))
    print('q) Back to Main. ')
    print('\n')
    next_action = input('Action: ')
    print('\n')
    
    if next_action.lower().strip() in sub_menu:
        sub_menu[next_action](entry)
    else:
        return


def cleanup_entries(index, entries):
    """Clean: Delete completed and Non-protected items that are older than a week."""
    if (input('Have you protected the important items? [y/n] ').lower().strip() == 'y'):
        print('\n')
        now = datetime.datetime.now()
        for entry in entries:
            if now - entry.timestamp > datetime.timedelta(7, 0, 0) and entry.done and not entry.protected:
                entry.delete_instance()
                


def modify_task(entry):
    """Edit/modify item. """
    new_task = input('Edit item to: ')
    entry.task = new_task
    entry.save()
    print('\n')


def delete_entry(entry):
    """Erase item. """
    if (input('Are you sure ?! - this action is permanent [y/n] ').lower().strip() == 'y'):
        print('\n')
        entry.delete_instance()


def toggle_done(entry):
    """Annotate item as 'Completed'."""
    entry.done = not entry.done
    entry.save()


def toggle_protection(entry):
    """Change the 'Protected' status of an item."""
    entry.protected = not entry.protected
    entry.save()


def menu_loop():
    choice = None
    index = 0  # shows which entry is selected
    entries = ToDo.select().order_by(ToDo.timestamp.asc())
    while choice != 'q':
        if len(entries) != 0:
            view_entries(index, entries, False)

            print('\n' + '-' * 20 + '\n')
            print("p) Previous item.")
            print("n) Next item.")
        for key, value in main_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        print('q) Quit.')
        choice = input('\nAction: ')
        print('\n')
        if choice in main_menu:
            try:
                main_menu[choice](index, entries)
            except ZeroDivisionError:
                continue
            entries = ToDo.select().order_by(ToDo.timestamp.asc())  # update entries after operations

        elif choice == 'n':
            index += 1
        elif choice == 'p':
            index -= 1

main_menu = OrderedDict([
    ('a', add_entry),
    ('m', modify_entry),
    ('c', cleanup_entries)
])

sub_menu = OrderedDict([
    ('m', modify_task),
    ('c', toggle_done),
    ('p', toggle_protection),
    ('e', delete_entry)
])
print('\n')
if __name__ == '__main__':
    initialize()
    menu_loop()
    db.close()
        

          
    
