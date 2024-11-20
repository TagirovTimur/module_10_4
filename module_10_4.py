import threading
from time import sleep
from datetime import datetime
from threading import Thread,Lock
import random
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def run(self):
        sleep(random.randint(1, 10))

class Cafe:
    def __init__(self, *tables):
        self.tables = tables
        self.queue = Queue()

    def is_vacant(self):
        # кафе пустое
        return not any(t.guest for t in self.tables)

    def guest_arrival(self, *guests):
# прибытие гостей
        for guest in guests:
            vacant_table_found = False
            for table in self.tables:
                if not table.guest:
                    table.guest = guest
                    guest.start()
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    vacant_table_found = True
                    break
            if not vacant_table_found:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')


    def discuss_guests(self):
# обслужить гостей
        while not (self.queue.empty() and self.is_vacant()):
            for table in self.tables:
                if not table.guest:
                    if not self.queue.empty():
                        table.guest = self.queue.get()
                        print(f'{table.guest.name} вышел(-ла) из очереди',
                              f'и сел(-а) за стол номер {table.number}')
                        table.guest.start()
                else:
                    if not table.guest.is_alive():
                        print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                        print(f'Стол номер {table.number} свободен')
                        table.guest = None

    # Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
                'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya',
                'Alexandra']
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
