class MenuItem:
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

        size_multipliers = {'small': 1.0, 'medium': 1.3, 'large': 1.6}
        return self.base_price * size_multipliers[size]




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