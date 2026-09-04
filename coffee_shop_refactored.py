from coffee_shop_exceptions import InvalidCustomizationError, InsufficientPointsError

class MenuItem:
    SIZE_MULTIPLIERS = {'small': 1.0, 'medium': 1.3, 'large': 1.6}
    DRINK_TYPES = {'Latte': 4.50, 'Cappuccino': 4.25, 'Espresso': 3.50, 'Americano': 3.75, 'Mocha': 5.00}

    def __init__(self, name, base_price, available_sizes):
        self.name = name
        self.base_price = base_price
        self.available_sizes = available_sizes

    def calculate_price(self, size):
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

        return self.base_price * self.SIZE_MULTIPLIERS[size]

class Order:
    def __init__(self):
        self.items = []

    def add_item(self, menu_item, size):
        """Add item to order.

        Args:
            menu_item: MenuItem instance
            size: Size of the drink
        """
        price = menu_item.calculate_price(size)
        self.items.append((menu_item.name, size, price))

    def total(self):
        """Calculate total price of the order."""
        return sum(price for _, _, price in self.items)

class Customer:
    def __init__(self, name, member=False):
        self.name = name
        self.member = member
        self.loyalty_points = 0

class LoyaltyProgram:
    POINTS_PER_DOLLAR = 1
    FREE_DRINK_POINTS = 100

    def earn_points(self, customer, amount_spent):
        """Earn loyalty points based on amount spent."""
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

# Extending MenuItem (composition approach)
class Beverage(MenuItem):
    def __init__(self, name, base_price, available_sizes):
        super().__init__(name, base_price, available_sizes)

# Usage - no change to Order class needed
order = Order()
order.add_item(Beverage("Latte", 4.50, ['small', 'medium', 'large']), 'large')

# print everything in the order
for item_name, size, price in order.items:
    print(f"{item_name.title()} ({size}): ${price:.2f}")

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