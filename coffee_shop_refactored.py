from coffee_shop_exceptions import InvalidSpentError, InvalidCustomer, InvalidDiscountError, InvalidItemError, InvalidCustomizationError, InsufficientPointsError

class MenuItem:
    SIZE_MULTIPLIERS = {'small': 1.0, 'medium': 1.3, 'large': 1.6}
    DRINK_TYPES = {'Latte': 4.50, 'Cappuccino': 4.25, 'Espresso': 3.50, 'Americano': 3.75, 'Mocha': 5.00}
    MILK_TYPES = {'Whole': 0.0, 'Skim': 0.0, 'Oat': 0.50, 'Almond': 0.80}

    def __init__(self, name, base_price, available_sizes, available_milk_types):
        self.name = name
        self.base_price = base_price
        self.available_sizes = available_sizes
        self.available_milk_types = available_milk_types
        self.new_price = 0

    def calculate_drink_price(self, size):
        """Calculate price based on size.

        Args:
            size: Drink size (small, medium, large)

        Returns:
            Price as float

        Raises:
            InvalidCustomizationError: If size not available
        """
        if size not in self.available_sizes:
            raise InvalidCustomizationError(
                f"Size '{size}' not available for {self.name}. "
                f"Available: {', '.join(self.available_sizes)}"
            )
        self.new_price = self.base_price * self.SIZE_MULTIPLIERS[size]
        return self.new_price



    def calculate_milk_price(self, milk_type):
        """Calculate price based on milk type.

        Args:
            milk_type: Type of milk (Whole, Skim, Oat, Almond)

        Returns:
            Price as float

        Raises:
            InvalidCustomizationError: If milk type not available
        """
        if milk_type not in self.available_milk_types:
            raise InvalidCustomizationError(
                f"Milk type '{milk_type}' not available for {self.name}. "
                f"Available: {', '.join(self.available_milk_types)}"
            )
        
        return self.new_price + self.MILK_TYPES[milk_type]


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, menu_item, size):
        """Add item to order.

        Args:
            menu_item: MenuItem instance
            size: Size of the drink
        """
        price = menu_item.calculate_drink_price(size)
        self.items.append((menu_item.name, size, price))

        if size not in self.available_sizes:
            raise InvalidCustomizationError(
                f"Size '{size}' not available for {self.name}. "
                f"Available: {', '.join(self.available_sizes)}"
            )


    def add_milk(self, menu_item, milk_type):
        """Add milk customization to the last item in the order.

        Args:
            menu_item: MenuItem instance
            milk_type: Type of milk
        """
        if not self.items:
            raise ValueError("No items in order to customize.")

        milk_price = menu_item.calculate_milk_price(milk_type)
        last_item = self.items[-1]
        updated_price = last_item[2] + milk_price
        self.items[-1] = (last_item[0], last_item[1], updated_price)

        if menu_item.name not in menu_item.DRINK_TYPES:
            raise InvalidItemError(
                f"Menu item '{menu_item.name}' does not exist."
            )

        if milk_type not in self.available_milk_types:
            raise InvalidCustomizationError(
                f"Milk type '{milk_type}' not available for {self.name}. "
                f"Available: {', '.join(self.available_milk_types)}"
            )

    def total(self):
        """Calculate total price of the order."""
        return sum(price for _, _, price in self.items)

class Customer:
    def __init__(self, name, member=False):
        self.name = name
        self.member = member
        self.loyalty_points = 0

class StaffMember(Customer):
    def __init__(self, name):
        super().__init__(name, member=True)
        self.is_staff = True
        self.loyalty_points = 0

    def apply_discount(self, total):
        """Apply staff discount to total price.

        Args:
            total: Total price before discount

        Returns:
            Total price after discount
        """
        if total < 0:
            raise InvalidDiscountError("Total cannot be negative.")

        return total * (1 - 0.10) 


class LoyaltyProgram:
    POINTS_PER_DOLLAR = 1
    FREE_DRINK_POINTS = 100

    def earn_points(self, customer, amount_spent):
        """Earn loyalty points based on amount spent."""

        if not isinstance(customer, Customer):
            raise InvalidCustomer("Invalid customer instance.")
        
        if amount_spent < 0:
            raise InvalidSpentError("Amount spent cannot be negative.")
        points_earned = int(amount_spent * self.POINTS_PER_DOLLAR)
        customer.loyalty_points += points_earned

    def redeem_points(self, customer, points_to_redeem):
        """Redeem loyalty points for a free drink.

        Raises:
            InsufficientPointsError: If customer doesn't have enough points
        """
        if customer.loyalty_points < points_to_redeem:
            raise InsufficientPointsError(
                f"Customer {customer.name} has insufficient points. "
                f"Available: {customer.loyalty_points}, Required: {points_to_redeem}"
            )
        customer.loyalty_points -= points_to_redeem

class StaffDrink:
    def __init__(self, menu_item, size):
        self.menu_item = menu_item
        self.size = size
        self.price = 0.0  # Staff drinks are free

    def get_receipt(self):
        """Generate receipt for staff drink."""
        if self.size not in self.menu_item.available_sizes:
            raise InvalidCustomizationError(
                f"Size '{self.size}' not available for {self.menu_item.name}. "
                f"Available: {', '.join(self.menu_item.available_sizes)}"
            )

        if self.menu_item.name not in self.menu_item.DRINK_TYPES:
            raise InvalidItemError(
                f"Menu item '{self.menu_item.name}' does not exist."
            )
        
        return f"Staff Drink: {self.menu_item.name.title()} ({self.size}) - Free"

# Usage - no change to Order class needed
# order = Order()
# order.add_item("Latte", 'large')

# # print everything in the order
# for item_name, size, price in order.items:
#     print(f"{item_name.title()} ({size}): ${price:.2f}")

# 1. Class Design (30%)
# Create at least these classes with clear responsibilities:
# MenuItem - Represents one menu item with pricing
# Order - Manages collection of items, calculates totals
# Customer - Holds customer information
# LoyaltyProgram - Manages points earning and redemption
# Custom exception classes (minimum 3)

# 2. Separation of Concerns (25%)
# Business logic separated from I/O
# Pricing logic centralized (not scattered)
# Each class has single, clear responsibility
# No global variables (except perhaps constants)

# 3. Composition & Inheritance (20%)
# Use composition where appropriate (Order HAS-A MenuItem)
# Consider inheritance if types emerge (optional, but think about it)
# Demonstrate understanding of IS-A vs HAS-A

# 4. Error Handling (15%)
# Use custom exceptions (not print statements for errors)
# Appropriate exception messages with context
# Demonstrate exception hierarchy

# 5. Google Docstrings (10%)
# All classes documented
# All public methods documented
# Type hints on method signatures
# Deliverables¶
# coffee_shop_refactored.py - Your OOP solution
# coffee_shop_exceptions.py - Custom exception hierarchy
# test_coffee_shop.py - Unit tests (provided template, you complete)