######################## IMPORTANT ########################
""" Do not rename the variables or functions.
Do not change the function parameters.
Do not add input() calls inside airport_manager.py.
The file must be importable by the tests. """
###########################################################


airport_info = ("OUL", 1, "14-09-2026")

allowed_gates = {"A1", "A2", "A3", "A4", "B1", "B2"}

restricted_destinations = {"Moscow", "Pyongyang"}

flights = {
    "AY450": {
        "destination": "Helsinki",
        "departure": "08:30",
        "gate": "A2",
        "capacity": 5,
        "passengers": ["Alice Wong", "David Kim", "Fatima Ali"],
    },
    "SK271": {
        "destination": "Stockholm",
        "departure": "10:15",
        "gate": "B1",
        "capacity": 4,
        "passengers": ["Chen Wei", "George Smith"],
    },
    "LH2491": {
        "destination": "Munich",
        "departure": "12:40",
        "gate": "A4",
        "capacity": 5,
        "passengers": ["Hana Lee", "Maria Garcia", "Noah Wilson"],
    },
}


def _normalized_text(value):
    """Return a trimmed, case-folded value for case-insensitive comparisons."""
    if not isinstance(value, str):
        return ""
    return " ".join(value.split()).casefold()


## Logic to find if a flight exists
def find_flight(flights, flight_number):
    wanted = _normalized_text(flight_number)

    for stored_number in flights:
        if _normalized_text(stored_number) == wanted:
            return stored_number

    return None


## Logic to find if a passenger exists
def passenger_exists(passengers, passenger_name):
    wanted = _normalized_text(passenger_name)
    return any(_normalized_text(name) == wanted for name in passengers)


## Logic to check in a passenger
def check_in_passenger(
    flights,
    flight_number,
    passenger_name,
    restricted_destinations
):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    cleaned_name = " ".join(passenger_name.split()) if isinstance(passenger_name, str) else ""
    if not cleaned_name:
        return "EMPTY_NAME"

    flight = flights[flight_key]
    if passenger_exists(flight["passengers"], cleaned_name):
        return "DUPLICATE"

    if len(flight["passengers"]) >= flight["capacity"]:
        return "FULL"

    restricted = {_normalized_text(destination) for destination in restricted_destinations}
    if _normalized_text(flight["destination"]) in restricted:
        return "RESTRICTED"

    flight["passengers"].append(cleaned_name.title())
    return "OK"


## Logic to remove a passenger from a flight
def remove_passenger(
    flights,
    flight_number,
    passenger_name
):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    passengers = flights[flight_key]["passengers"]
    wanted = _normalized_text(passenger_name)

    for index, stored_name in enumerate(passengers):
        if _normalized_text(stored_name) == wanted:
            passengers.pop(index)
            return "OK"

    return "PASSENGER_NOT_FOUND"


# Logic to change the gate of a flight
def change_gate(
    flights,
    flight_number,
    new_gate,
    allowed_gates
):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    normalized_gate = "" if not isinstance(new_gate, str) else new_gate.strip().upper()
    valid_gates = {
        gate.strip().upper()
        for gate in allowed_gates
        if isinstance(gate, str)
    }
    if normalized_gate not in valid_gates:
        return "INVALID_GATE"

    flights[flight_key]["gate"] = normalized_gate
    return "OK"


# Logic to get the status of a flight
def flight_status(flight):
    passenger_count = len(flight["passengers"])
    capacity = flight["capacity"]

    if passenger_count >= capacity:
        return "FULL"
    if passenger_count / capacity >= 0.75:
        return "ALMOST FULL"
    return "AVAILABLE"



# Logic to get the sorted manifest of a flight
def sorted_manifest(
    flights,
    flight_number
):
    flight_key = find_flight(flights, flight_number)
    if flight_key is None:
        return None

    return sorted(flights[flight_key]["passengers"])


# Logic to get the total number of passengers across all flights
def total_passengers(flights):
    return sum(len(flight["passengers"]) for flight in flights.values())


# Logic to check if any flight is full
def any_full_flight(flights):
    return any(
        len(flight["passengers"]) >= flight["capacity"]
        for flight in flights.values()
    )



# Logic to check if all flights have at least one passenger
def all_flights_have_passengers(flights):
    return all(len(flight["passengers"]) > 0 for flight in flights.values())
