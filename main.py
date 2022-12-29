import json
class Car:
    def __init__(self, make, model, vin, plate, color, year):
        self.make = make
        self.model = model
        self.vin = vin
        self.plate = plate
        self.color = color
        self.year = year
        self.rental_history = []
        self.rental_count = 0

    def rent(self, idnp, date):
        self.rental_history.append((date, idnp))
        self.rental_count += 1
def read_data():
    with open("cars.json", "r") as f:
        data = json.load(f)
        car_list = []
        for car in data:
            new_car = Car(car["make"], car["model"], car["vin"], car["plate"], car["color"], car["year"])
            new_car.rental_history = car["rental_history"]
            new_car.rental_count = car["rental_count"]
            car_list.append(new_car)
        return car_list
def write_data(car_list):
    car_data = []
    for car in car_list:
        car_dict = {
            "make": car.make,
            "model": car.model,
            "vin": car.vin,
            "plate": car.plate,
            "color": car.color,
            "year": car.year,
            "rental_history": car.rental_history,
            "rental_count": car.rental_count
        }
        car_data.append(car_dict)
    with open("cars.json", "w") as f:
        json.dump(car_data, f)
def main_car_menue():
    car_list = read_data()
    while True:
        print("What would you like to do?")
        print("1. Add a new car")
        print("2. Rent a car")
        print("3. View rental history of a car")
        print("0. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_car(car_list)
        elif choice == "2":
            rent_car(car_list)
        elif choice == "3":
            view_history(car_list)
        elif choice == "0":
            break
        else:
            print("Invalid choice")
def add_car(car_list):
    make = input("Enter the make of the car: ")
    model = input("Enter the model of the car: ")
    vin = input("Enter the VIN number of the car: ")
    plate = input("Enter the plate number of the car: ")
    color = input("Enter the color of the car: ")
    year = input("Enter the year of production of the car: ")
    new_car = Car(make, model, vin, plate, color, year)
    car_list.append(new_car)

def rent_car(car_list):
    plate = input("Enter the plate number of the car: ")
    idnp = input("Enter your IDNP: ")
    for car in car_list:
        if car.plate == plate:
            car.rent(idnp)
            print("Car rented successfully")
            return
    print("Car not found")

def view_history(car_list):
    plate = input("Enter the plate number of the car: ")
    for car in car_list:
        if car.plate == plate:
            print("Rental history for car with plate number", plate)
            for rental in car.rental_history:
                print(rental[0], rental[1])
            return
    print("Car not found")

def read_customers():
    with open("customers.json", "r") as f:
        return json.load(f)

def write_customers(customer_list):
    with open("customers.json", "w") as f:
        json.dump(customer_list, f)

def search_customer_by_name(name, customers):
    for customer in customers:
        #print(f'{customer["first_name"].lower()} == {name.lower()} or {customer["last_name"].lower()} == {name.lower()}')
        if customer["first_name"].lower() == name.lower() or customer["last_name"].lower() == name.lower():
            return customer
    return None

def display_last_5_rentals(customer):
    num_rentals = len(customer["rented_cars"])
    if num_rentals == 0:
        print("This customer has not rented any cars.")
    else:
        start_index = max(0, num_rentals - 5)
        for i in range(start_index, num_rentals):
            rental = customer["rented_cars"][i]
            print("VIN:", rental[0], "Date:", rental[1])

def search_customer_by_vin(vin, customers):
    for customer in customers:
        for rental in customer["rented_cars"]:
            if rental[0] == vin:
                return customer

def add_customer(customers):
    first_name = input("Enter the customer's first name: ")
    last_name = input("Enter the customer's last name: ")
    idnp = input("Enter the customer's IDNP: ")
    dob = input("Enter the customer's date of birth (YYYY-MM-DD): ")
    new_customer = {
        "first_name": first_name,
        "last_name": last_name,
        "idnp": idnp,
        "dob": dob,
        "rented_cars": [],
        "last_rented_car": [],
        "total_rentals": 0
    }
    customers.append(new_customer)
    write_customers(new_customer)

def add_car_to_customer(customer, vin, date):
    customer["rented_cars"].append([vin, date])
    customer["last_rented_car"] = [vin, date]
    customer["total_rentals"] += 1


def main_customer_menu():
    customers = read_customers()
    while True:
        print("\nMenu:")
        print("1. Search for customer by name")
        print("2. Display last 5 rentals for a customer")
        print("3. Search for customer by VIN number")
        print("4. Add new customer")
        print("5. Add car to existing customer")
        print("0. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter the customer's name: ")
            customer = search_customer_by_name(name, customers)
            if customer:
                print("Customer found:", customer["first_name"], customer["last_name"])
            else:
                print("Customer not found")
        elif choice == "2":
            idnp = input("Enter the customer's IDNP: ")
            customer = None
            for c in customers:
                if c["idnp"] == idnp:
                    customer = c
                    break
            if customer:
                display_last_5_rentals(customer)
            else:
                print("Customer not found")
        elif choice == "3":
            vin = input("Enter the VIN number: ")
            customer = search_customer_by_vin(vin, customers)
            if customer:
                print("Customer found:", customer["first_name"], customer["last_name"])
            else:
                print("Customer not found")
        elif choice == "4":
            add_customer(customers)
            write_customers(customers)
            print("Customer added successfully")
        elif choice == "5":
            idnp = input("Enter the customer's IDNP: ")
            vin = input("Enter the VIN number of the car: ")
            date = input("Enter the rental date (YYYY-MM-DD): ")
            customer = None
            for c in customers:
                if c["idnp"] == idnp:
                    customer = c
                    break
            if customer:
                add_car_to_customer(customer, vin, date)
                write_customers(customers)
                print("Car added to customer successfully")
            else:
                print("Customer not found")
        elif choice == "0":
            break
        else:
            print("Invalid choice")

    
if __name__ == "__main__":
    #main_car_menue()
    main_customer_menu()
       
