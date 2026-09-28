import sys


# ---------------- TICKET ----------------

class Ticket:
    def __init__(self, ticket_id, severity, category, priority, order):
        self.id = ticket_id
        self.severity = severity
        self.category = category
        self.priority = priority
        self.order = order
        self.status = "WAITING"


# ---------------- QUEUE ----------------

class QueueNode:
    def __init__(self, ticket):
        self.ticket = ticket
        self.next = None


class TicketQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, ticket):
        new_node = QueueNode(ticket)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        if self.head is None:
            return None

        ticket = self.head.ticket
        self.head = self.head.next

        if self.head is None:
            self.tail = None

        return ticket

    def peek(self):
        if self.head is None:
            return None
        return self.head.ticket

    def isEmpty(self):
        return self.head is None


# ---------------- MAX HEAP ----------------

class BinaryMaxHeap:
    def __init__(self):
        self.data = []

    def isEmpty(self):
        return len(self.data) == 0
  
    def peekMax(self):
        if self.isEmpty():
            return None
        return self.data[0]

    def isBetter(self, first, second):
  
        if first.priority > second.priority:
            return True

        if first.priority < second.priority:
            return False

        # если приорити одинаковый раньше идёт тот кого раньше добавили
        return first.order < second.order

    def insert(self, ticket):
        self.data.append(ticket)
        self.siftUp(len(self.data) - 1)

    def siftUp(self, index):
        while index > 0:
            parent = (index - 1) // 2

            if self.isBetter(self.data[index], self.data[parent]):
                self.data[index], self.data[parent] = self.data[parent], self.data[index]
                index = parent
            else:
                break

    def removeMax(self):
        if self.isEmpty():
            return None

        result = self.data[0]

        last = self.data.pop()

        if len(self.data) > 0:
            self.data[0] = last
            self.siftDown(0)

        return result

    def siftDown(self, index):
        while True:
            left = index * 2 + 1
            right = index * 2 + 2
            best = index

            if left < len(self.data):
                if self.isBetter(self.data[left], self.data[best]):
                    best = left

            if right < len(self.data):
                if self.isBetter(self.data[right], self.data[best]):
                    best = right

            if best == index:
                break

            self.data[index], self.data[best] = self.data[best], self.data[index]
            index = best


# ---------------- HASH TABLE ----------------

class HashNode:
    def __init__(self, ticket_id, ticket):
        self.id = ticket_id
        self.ticket = ticket
        self.next = None


class TicketHashTable:
    def __init__(self, size):
        self.size = size
        self.buckets = [None] * size

    def getIndex(self, ticket_id):
        return ticket_id % self.size

    def put(self, ticket_id, ticket):
        index = self.getIndex(ticket_id)

        new_node = HashNode(ticket_id, ticket)

        new_node.next = self.buckets[index]
        self.buckets[index] = new_node

    def get(self, ticket_id):
        index = self.getIndex(ticket_id)
        current = self.buckets[index]

        while current is not None:
            if current.id == ticket_id:
                return current.ticket

            current = current.next

        return None

    def contains(self, ticket_id):
        if self.get(ticket_id) is None:
            return False

        return True

    def remove(self, ticket_id):
        index = self.getIndex(ticket_id)

        current = self.buckets[index]
        previous = None

        while current is not None:
            if current.id == ticket_id:

                if previous is None:
                    self.buckets[index] = current.next
                else:
                    previous.next = current.next

                return current.ticket

            previous = current
            current = current.next

        return None


# ---------------- CONFIG ----------------

def getConfig(number):
    if number == 0 or number == 5:
        return 7, 3, 1, 2

    if number == 1 or number == 6:
        return 11, 1, 2, 3

    if number == 2 or number == 7:
        return 13, 2, 3, 1

    if number == 3 or number == 8:
        return 17, 3, 2, 1

    return 19, 2, 1, 3


def readId(text):
    if not text.isdigit():
        return None

    ticket_id = int(text)

    if ticket_id < 1 or ticket_id > 1000000000:
        return None

    if len(text) > 10:
        return None

    return ticket_id
def main():
    # Пример ввода: CONFIG 0
    config = input("Введите CONFIG и вариант. Пример: CONFIG 0: ").split()

    variant = int(config[1])

    size, sw, hw, acc = getConfig(variant)

    bonuses = {
        "SW": sw,
        "HW": hw,
        "ACC": acc
    }

    waiting = TicketQueue()
    ready = BinaryMaxHeap()
    table = TicketHashTable(size)

    order = 0

    while True:
        command = input(
            "\nВведите команду:\n"
            "ADD id severity category  пример: ADD 101 3 SW\n"
            "TRIAGE\n"
            "SERVE\n"
            "FIND id                пример: FIND 101\n"
            "CANCEL id              пример: CANCEL 101\n"
            "END\n"
            "Ваш ввод: "
        ).split()

        if not command:
            print("INVALID")
            continue

        action = command[0]

        if action == "END":
            break


        elif action == "ADD":
            ticket_id = int(command[1])
            severity = int(command[2])
            category = command[3]

            if table.contains(ticket_id):
                print("DUPLICATE", ticket_id)
                continue

            priority = severity * 10 + bonuses[category]

            order += 1

            ticket = Ticket(
                ticket_id,
                severity,
                category,
                priority,
                order
            )

            table.put(ticket_id, ticket)
            waiting.enqueue(ticket)

            print("ADDED", ticket_id, "P=" + str(priority))


        elif action == "TRIAGE":
            ticket = waiting.dequeue()

            while ticket and table.get(ticket.id) is not ticket:
                ticket = waiting.dequeue()

            if ticket is None:
                print("EMPTY WAITING")
            else:
                ticket.status = "READY"
                ready.insert(ticket)
                print("TRIAGED", ticket.id, "P=" + str(ticket.priority))


        elif action == "SERVE":
            ticket = ready.removeMax()

            while ticket and table.get(ticket.id) is not ticket:
                ticket = ready.removeMax()

            if ticket is None:
                print("EMPTY READY")
            else:
                table.remove(ticket.id)
                print("SERVED", ticket.id)


        elif action == "FIND":
            ticket_id = int(command[1])
            ticket = table.get(ticket_id)

            if ticket is None:
                print("NOT FOUND", ticket_id)
            else:
                print(
                    "FOUND",
                    ticket.id,
                    ticket.status,
                    "P=" + str(ticket.priority)
                )


        elif action == "CANCEL":
            ticket_id = int(command[1])
            ticket = table.remove(ticket_id)

            if ticket is None:
                print("NOT FOUND", ticket_id)
            else:
                print("CANCELLED", ticket_id)


        else:
            print("INVALID")


main()