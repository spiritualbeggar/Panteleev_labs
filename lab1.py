from collections import deque
import random

# Абстрактный тип данных для событий
class EventQueue:
    def __init__(self):
        self.queue = deque()

    def add_event(self, event_type, time):
        # Вставляем событие в правильное место в очереди
        for i, (event_time, _) in enumerate(self.queue):
            if time < event_time:
                self.queue.insert(i, (time, event_type))
                return
        self.queue.append((time, event_type))

    def get_next_event(self):
        return self.queue.popleft() if self.queue else None

# Параметры модели
arrival_rate = 1.0  # Средняя интенсивность прихода клиентов (клиенты в единицу времени)
service_rate = 1.5  # Средняя интенсивность обслуживания (клиенты в единицу времени)
simulation_time = 100.0  # Время моделирования

# Инициализация
event_queue = EventQueue()  # Очередь событий (АТД)
current_time = 0.0
num_lost = 0  # Количество потерянных клиентов
num_served = 0  # Количество обслуженных клиентов
server_busy = False  # Флаг, указывающий, занят ли сервер

# Функция для генерации времени прихода следующего клиента
def generate_arrival_time():
    return random.expovariate(arrival_rate)

# Функция для генерации времени обслуживания клиента
def generate_service_time():
    return random.expovariate(service_rate)

# Инициализация первого события прихода клиента
next_arrival_time = generate_arrival_time()
event_queue.add_event('arrival', next_arrival_time)

# Основной цикл моделирования
while current_time < simulation_time:
    # Получаем следующее событие
    event_time, event_type = event_queue.get_next_event()
    if event_time is None:
        break
    current_time = event_time

    if event_type == 'arrival':
        # Приход нового клиента
        if not server_busy:
            # Сервер свободен, начинаем обслуживание
            service_time = generate_service_time()
            event_queue.add_event('departure', current_time + service_time)
            server_busy = True
        else:
            # Сервер занят, клиент теряется
            num_lost += 1

        # Планируем следующий приход клиента
        next_arrival_time = current_time + generate_arrival_time()
        event_queue.add_event('arrival', next_arrival_time)

    elif event_type == 'departure':
        # Окончание обслуживания клиента
        num_served += 1
        server_busy = False

# Вывод результатов
print(f"Время моделирования: {simulation_time}")
print(f"Количество обслуженных клиентов: {num_served}")
print(f"Количество потерянных клиентов: {num_lost}")
print(f"Коэффициент загрузки сервера: {num_served / (num_served + num_lost)}")