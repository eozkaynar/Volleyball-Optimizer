from classes import Player,Service

import tkinter as tk
from tkinter import simpledialog, messagebox, OptionMenu, StringVar

# GUI application for cost calculation
class CostCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Service Cost Calculator")

        # Predefined locations for the dropdown menu
        self.locations = ["100.", "asti", "dikmen", "Manual"]

        # Create labels and input fields
        tk.Label(root, text="Court Price:").grid(row=0, column=0)
        self.court_price = tk.Entry(root)
        self.court_price.grid(row=0, column=1)

        tk.Label(root, text="Number of Total Players:").grid(row=1, column=0)
        self.num_players = tk.Entry(root)
        self.num_players.grid(row=1, column=1)

        tk.Label(root, text="Number of Services:").grid(row=2, column=0)
        self.num_services = tk.Entry(root)
        self.num_services.grid(row=2, column=1)

        # Button to create player and service inputs
        tk.Button(root, text="Enter Player Info", command=self.create_player_fields).grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="Enter Service Info", command=self.create_service_fields).grid(row=4, column=0, columnspan=2)

        # Button to calculate costs
        tk.Button(root, text="Calculate Costs", command=self.calculate_costs).grid(row=5, column=0, columnspan=2)

        # Output area
        self.output = tk.Text(root, height=30, width=100)
        self.output.grid(row=6, column=0, columnspan=2)

        # Initialize variables to store players and services
        self.players = []
        self.services = []

    def create_player_fields(self):
        try:
            self.num_services_val = int(self.num_services.get())
            self.court_price_val = float(self.court_price.get())
            self.num_players_val = int(self.num_players.get())
            self.base_cost = self.court_price_val / self.num_players_val

            # Create player inputs
            for i in range(self.num_players_val-self.num_services_val):
                player_name = simpledialog.askstring("Player Name", f"Enter name for Player {i + 1}:")

                # Create a new window to place dropdowns in a better position
                popup = tk.Toplevel(self.root)
                popup.title(f"Player {i+1} Info")

                tk.Label(popup, text=f"From Location for {player_name}:").grid(row=0, column=0)
                from_var = StringVar(popup)
                from_var.set(self.locations[0])  # Default option
                from_menu = OptionMenu(popup, from_var, *self.locations)
                from_menu.grid(row=0, column=1)

                tk.Label(popup, text=f"To Location for {player_name}:").grid(row=1, column=0)
                to_var = StringVar(popup)
                to_var.set(self.locations[0])  # Default option
                to_menu = OptionMenu(popup, to_var, *self.locations)
                to_menu.grid(row=1, column=1)

                tk.Button(popup, text="Confirm", command=popup.destroy).grid(row=2, column=0, columnspan=2)

                self.root.wait_window(popup)  # Wait for user to close the popup

                from_loc = from_var.get()
                to_loc = to_var.get()

                # Handle manual entry if selected
                if from_loc == "Manual":
                    from_loc = simpledialog.askstring("Manual Entry", "Enter manual 'from' distance:")
                if to_loc == "Manual":
                    to_loc = simpledialog.askstring("Manual Entry", "Enter manual 'to' distance:")

                # Create Player object
                player = Player(player_name, from_loc, to_loc, self.base_cost)
                self.players.append(player)

                self.output.insert(tk.END, player.info() + "\n")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid court price and number of players.")

    def create_service_fields(self):
        try:
            self.num_services_val = int(self.num_services.get())

            # Create service inputs
            for i in range(self.num_services_val):
                service_name = simpledialog.askstring("Service Name", f"Enter name for Service {i + 1}:")
                service_fuel_cons = float(simpledialog.askstring("Fuel Consumption", f"Enter fuel consumption for Service {i + 1} (liters/km):"))

                # Create a new window to place dropdowns for service to/from locations
                popup = tk.Toplevel(self.root)
                popup.title(f"Service {i+1} Info")

                tk.Label(popup, text=f"From Location for {service_name}:").grid(row=0, column=0)
                from_var = StringVar(popup)
                from_var.set(self.locations[0])  # Default option
                from_menu = OptionMenu(popup, from_var, *self.locations)
                from_menu.grid(row=0, column=1)

                tk.Label(popup, text=f"To Location for {service_name}:").grid(row=1, column=0)
                to_var = StringVar(popup)
                to_var.set(self.locations[0])  # Default option
                to_menu = OptionMenu(popup, to_var, *self.locations)
                to_menu.grid(row=1, column=1)

                tk.Button(popup, text="Confirm", command=popup.destroy).grid(row=2, column=0, columnspan=2)

                self.root.wait_window(popup)  # Wait for user to close the popup

                from_loc = from_var.get()
                to_loc = to_var.get()

                # Handle manual entry if selected
                if from_loc == "Manual":
                    from_loc = simpledialog.askstring("Manual Entry", "Enter manual 'from' distance:")
                if to_loc == "Manual":
                    to_loc = simpledialog.askstring("Manual Entry", "Enter manual 'to' distance:")

                # Select specific passengers for the service
                passengers = []
                passenger_names = simpledialog.askstring("Passengers", f"Enter comma-separated player names for {service_name}:")
                selected_passengers = passenger_names.split(',')

                for player_name in selected_passengers:
                    player_name = player_name.strip()
                    for player in self.players:
                        if player.name == player_name:
                            passengers.append(player)

                # Create Service object
                service = Service(service_name, from_loc, to_loc, self.base_cost, passengers, service_fuel_cons)
                self.services.append(service)

                self.output.insert(tk.END, f"Service {service_name} created with {len(passengers)} passengers.\n")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid values for services.")

    def calculate_costs(self):
        try:
            # Fuel price asked via pop-up
            fuel_price = float(simpledialog.askstring("Fuel Price", "Enter fuel price (currency per liter):"))

            # Calculate cost for each service
            for service in self.services:
                service.CalculateKM(fuel_price)
                service.setTotalCost()
                self.output.insert(tk.END, f"\nService {service.name}, Total Cost: {service.total_cost:.2f}\n")

            for player in self.players:
                player.setTotalCost()
                self.output.insert(tk.END, f"{player.info()}, Total Cost: {player.total_cost:.2f}\n")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid values for fuel price.")


# Main GUI loop
root = tk.Tk()
app = CostCalculatorGUI(root)
root.mainloop()
