class CoffeeShopError(Exception):
    """Base exception for all coffee shop errors."""
    pass

class OrderError(CoffeeShopError):
    """Base exception for order-related errors."""
    pass

class InvalidItemError(OrderError):
    """Raised when item doesn't exist on menu."""
    pass

class InvalidCustomizationError(OrderError):
    """Raised when customization not available."""
    pass

class PaymentError(CoffeeShopError):
    """Base exception for payment errors."""
    pass

class InsufficientPointsError(PaymentError):
    """Raised when loyalty points insufficient for redemption."""
    pass

class InvalidDiscountError(PaymentError):
    """Raised when discount can't be applied."""
    pass


# Custom exception classes
class CustomerError(CoffeeShopError):
    """Base exception for customer-related errors."""
    pass
    
class InvalidCustomerMembershipError(CustomerError):
    """Raised when customer membership status is invalid."""
    pass

class InvalidCustomerStaffStatusError(CustomerError):
    """Raised when customer staff status is invalid."""
    pass

class InvalidSpentError(PaymentError):
    """Raised when amount is invalid (e.g., negative)."""
    pass

class InvalidCustomer(CustomerError):
    """Raised when customer information is invalid."""
    pass

