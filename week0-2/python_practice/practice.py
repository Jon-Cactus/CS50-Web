class Flight():
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []

    def add_passenger(self, name):
        if not self.open_seats():
            return False
        else:
            self.passengers += [name]
        return True

    def open_seats(self):
        return self.capacity - len(self.passengers)
    


flight = Flight(5)
people = ["Ron", "Harry", "Hermione", "Hagrid", "Snape", "Dumbledore"]

for person in people:
    success = flight.add_passenger(person)
    if success:
        print(f"Successfully added {person} to the flight!")
    else:
        print(f"Not enough space for {person}!")

print(flight.passengers)
