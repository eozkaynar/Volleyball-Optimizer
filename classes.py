class Player:
    def __init__(self,name,from_,to_, base_cost,power = 0):
        self.name       = name
        self.power      = power # Daha sonra takım oluşturmada kullanılabilir
        self.from_      = from_
        self.to_        = to_
        self.base_cost  = base_cost
        self.distance   = 0
        self.cost       = 0

        # Calculate the distance based on location selection
        self.distance += self.calculate_distance(self.from_)
        self.distance += self.calculate_distance(self.to_)

    def calculate_distance(self, location):
        if location == "100.":
            return 12
        elif location == "asti":
            return 6.5
        elif location == "dikmen":
            return 17.5
        else:
            try:
                return float(location)  # Handle manual numeric input
            except ValueError:
                return 0  # Default to 0 if invalid input
    def info(self):
        """Return player's information as a formatted string."""
        return f"Player name: {self.name}, Distance: {self.distance} km"

    def setTotalDistance(self,manuel_distance):
        self.distance = manuel_distance


    def setExtraCost(self,cost):
        self.cost = cost
    
    def setTotalCost(self):
        if self.cost is None:
            self.total_cost = self.base_cost
        else:
            self.total_cost = self.cost + self.base_cost

class Service(Player):
    def __init__(self, name, from_, to_, base_cost, passengers, fuel_cons, power=0):
        super().__init__(name, from_, to_, base_cost, power)
        self.passengers = passengers
        self.fuel_cons  = fuel_cons

    def CalculateKM(self,fuel_price):
        max_km          = 0
        total_distance  = 0 
        for player in self.passengers:
            if(player.distance > max_km):
                max_km = player.distance
            total_distance += player.distance # Total passenger distance
        total_distance += self.distance       # Add service distance

        fuel_cost     = max_km*self.fuel_cons*fuel_price
        print(total_distance)
        self.cost     = (fuel_cost * self.distance/total_distance) - fuel_cost
        for player in self.passengers:
            cost = fuel_cost*player.distance/total_distance
            player.setExtraCost(cost)