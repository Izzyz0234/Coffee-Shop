from coffee_shop_exceptions import InvalidCustomerMembershipError, InvalidCustomerStaffStatusError, InvalidSpentError, InvalidCustomer, InvalidDiscountError, InvalidItemError, InvalidCustomizationError, InsufficientPointsError

# Created: 04/09/2026
# By: Isabella

class MenuItem:
    """Represents a menu item with pricing and customization options.
    Args:
        name (str): The name of the menu item.
        base_price (float): The base price of the menu item.
        available_sizes (list): A list of available sizes.
        available_milk_types (list): A list of available milk types.
    Raises:
        InvalidItemError: If the menu item does not exist or base price is incorrect.
        InvalidCustomizationError: If the size or milk type is not available.
    """

    SIZE_MULTIPLIERS = {'small': 1.0, 'medium': 1.3, 'large': 1.6}
    DRINK_TYPES = {'Latte': 4.50, 'Cappuccino': 4.25, 'Espresso': 3.50, 'Americano': 3.75, 'Mocha': 5.00}
    MILK_TYPES = {'Whole': 0.0, 'Skim': 0.0, 'Oat': 0.50, 'Almond': 0.80}

    def __init__(self, name, base_price, available_sizes, available_milk_types):
        self.name = name
        self.base_price = base_price
        self.available_sizes = available_sizes
        self.available_milk_types = available_milk_types
        self.new_price = 0

        if self.name not in self.DRINK_TYPES:
            raise InvalidItemError(f"Menu item '{self.name}' does not exist. Available items: {', '.join(self.DRINK_TYPES.keys())}")
        if self.base_price != self.DRINK_TYPES[self.name]:
            raise InvalidItemError(f"Base price for '{self.name}' is incorrect. Expected: {self.DRINK_TYPES[self.name]}, Got: {self.base_price}")
        if not all(size in self.SIZE_MULTIPLIERS for size in self.available_sizes):
            raise InvalidCustomizationError(f"One or more sizes are invalid. Available sizes: {', '.join(self.SIZE_MULTIPLIERS.keys())}")
        if not all(milk in self.MILK_TYPES for milk in self.available_milk_types):
            raise InvalidCustomizationError(f"One or more milk types are invalid. Available milk types: {', '.join(self.MILK_TYPES.keys())}")

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
    

class Order(MenuItem):
    def __init__(self, name, base_price, available_sizes, available_milk_types):
        super().__init__(name, base_price, available_sizes, available_milk_types)
        self.items = []

    def add_item(self, menu_item, size):
        """Add item to order.

        Args:
            menu_item: MenuItem instance
            size: Size of the drink
        Raises:
            InvalidItemError: If menu item does not exist
            InvalidCustomizationError: If size not available
        """
        if size not in self.available_sizes:
            raise InvalidCustomizationError(
                f"Size '{size}' not available for {self.name}. "
                f"Available: {', '.join(self.available_sizes)}"
            )

        price = menu_item.calculate_drink_price(size)
        self.items.append((menu_item.name, size, price))
        return self.calculate_drink_price(size)


    def add_milk(self, menu_item, milk_type):
        """Add milk customization to the last item in the order.

        Args:
            menu_item: MenuItem instance
            milk_type: Type of milk
        Raises:
            InvalidItemError: If menu item does not exist
            InvalidCustomizationError: If milk type not available
        """
        if menu_item.name not in menu_item.DRINK_TYPES:
            raise InvalidItemError(
                f"Menu item '{menu_item.name}' does not exist."
            )

        if milk_type not in self.available_milk_types:
            raise InvalidCustomizationError(
                f"Milk type '{milk_type}' not available for {self.name}. "
                f"Available: {', '.join(self.available_milk_types)}"
            )

        if not self.items:
            raise ValueError("No items in order to customize.")

        milk_price = menu_item.calculate_milk_price(milk_type)
        last_item = self.items[-1]
        updated_price = last_item[2] + milk_price
        self.items[-1] = (last_item[0], last_item[1], updated_price)
        return self.calculate_milk_price(milk_type)

    def total(self):
        """Calculate total price of the order."""
        return sum(price for _, _, price in self.items)


class Customer:
    """Represents a customer with membership and loyalty points.
    
    Args:
        name: Customer's name
        member: Whether the customer is a member
        loyalty_points: Number of loyalty points the customer has
        is_staff: Whether the customer is a staff member
    Raises:
        InvalidCustomerMembershipError: If membership status is invalid
        InvalidCustomerStaffStatusError: If staff status is invalid
    """

    def __init__(self, name, member=False, loyalty_points=0, is_staff=False):
        self.name = name
        self.member = member
        self.loyalty_points = loyalty_points
        self.is_staff = is_staff

        if is_staff not in [True, False]:
            raise InvalidCustomerStaffStatusError(
                f"Customer '{self.name}' has invalid staff status."
            )

        if member not in [True, False]:
            raise InvalidCustomerMembershipError(
                f"Customer '{self.name}' has invalid membership status."
            )

class StaffMember(Customer):
    """Represents a staff member with special privileges.
    
    Args:
        name: Staff member's name
        member: Whether the staff member is a member
        is_staff: Whether the staff member is a staff member
    Raises:
            InvalidCustomerStaffStatusError: If staff status is invalid
    """
    def __init__(self, name, member=True, is_staff=True):
        super().__init__(name, member=member, loyalty_points=0, is_staff=is_staff)

    def apply_discount(self, total):
        """Apply staff discount to total price.

        Args:
            total: Total price before discount
        Returns:
            Total price after discount
        Raises:
            InvalidCustomerStaffStatusError: If customer is not a staff member
        """
        if self.is_staff == False:
            raise InvalidCustomerStaffStatusError(
                f"Customer '{self.name}' is not a staff member."
            )

        if total < 0:
            raise InvalidDiscountError("Total cannot be negative.")

        return total * (1 - 0.10) 


class LoyaltyProgram:
    """Manages loyalty points for customers.
    Args:
        POINTS_PER_DOLLAR: Points earned per dollar spent
        FREE_DRINK_POINTS: Points required for a free drink
    Raises:
            InvalidCustomer: If customer does not exist
            InvalidSpentError: If amount spent is invalid
    """
    POINTS_PER_DOLLAR = 1
    FREE_DRINK_POINTS = 100

    def earn_points(self, customer, amount_spent):
        """Earn loyalty points based on amount spent."""

        if not isinstance(customer, Customer):
            raise InvalidCustomer("Customer does not exist.")
        
        if amount_spent < 0:
            raise InvalidSpentError("Amount spent cannot be negative.")
        
        points_earned = int(amount_spent * self.POINTS_PER_DOLLAR)
        customer.loyalty_points += points_earned

    def redeem_points(self, customer, points_to_redeem):
        """Redeem loyalty points for a free drink.

        Raises:
            InsufficientPointsError: If customer doesn't have enough points
            InvalidCustomerStaffStatusError: If customer is a staff member
        Args:
            customer: Customer instance
            points_to_redeem: Number of points to redeem
        """
        if StaffMember(customer.name, member=customer.member, is_staff=customer.is_staff).is_staff == True:
            raise InvalidCustomerStaffStatusError(
                f"Staff member '{customer.name}' cannot redeem points."
            )

        if not isinstance(customer, Customer):
            raise InvalidCustomer("Customer does not exist.")

        if customer.loyalty_points < points_to_redeem:
            raise InsufficientPointsError(
                f"Customer {customer.name} has insufficient points. "
                f"Available: {customer.loyalty_points}, Required: {points_to_redeem}"
            )
        
        customer.loyalty_points -= points_to_redeem


class StaffDrink:
    """Represents a free drink for staff members.
    Args:
        menu_item: MenuItem instance
        size: Size of the drink
    Raises:
        InvalidCustomizationError: If size not available
        InvalidItemError: If menu item does not exist
    """
    def __init__(self, menu_item, size):
        self.menu_item = menu_item
        self.size = size
        self.price = 0.0  # Staff drinks are free

        if self.size not in self.menu_item.available_sizes:
            raise InvalidCustomizationError(
                f"Size '{self.size}' not available for {self.menu_item.name}. "
                f"Available: {', '.join(self.menu_item.available_sizes)}"
            )

        if self.menu_item.name not in self.menu_item.DRINK_TYPES:
            raise InvalidItemError(
                f"Menu item '{self.menu_item.name}' does not exist."
            )


    def get_receipt(self):
        """Generate receipt for staff drink.
        Returns:
            Receipt string
        """
        
        return f"Staff Drink: {self.menu_item.name.title()} ({self.size}) - Free"

