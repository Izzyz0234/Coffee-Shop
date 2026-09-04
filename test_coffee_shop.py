import unittest
from coffee_shop_refactored import MenuItem, Order, Customer, LoyaltyProgram, StaffMember
from coffee_shop_exceptions import InvalidDiscountError, InsufficientPointsError, InvalidCustomizationError

class TestCoffeeShop(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.latte = MenuItem("Latte", 4.50, ['small', 'medium', 'large'], ['Whole', 'Skim', 'Oat', 'Almond'])
        self.latteMedium = MenuItem("Latte", 4.50, ['small', 'medium', 'large'], ['Whole', 'Skim', 'Oat', 'Almond'])
        self.mocha = MenuItem("Mocha", 5.00, ['small', 'medium', 'large'], ['Whole', 'Skim', 'Oat', 'Almond'])
        self.customer = Customer("Alice", member=True)
        self.staffMember = StaffMember("Bob")
        self.loyalty = LoyaltyProgram()

    def test_menu_item_pricing_small(self):
        """Test MenuItem calculates small drink price correctly."""
        price = self.latte.calculate_drink_price('small')
        self.assertEqual(price, 4.50)
    
    def test_menu_item_pricing_medium(self):
        """Test MenuItem calculates medium drink price correctly."""    
        price_medium = self.latteMedium.calculate_drink_price('medium')
        self.assertEqual(price_medium, 4.50 * 1.3)

    def test_menu_item_milk_oat(self):
        """Test MenuItem calculates price with oat milk correctly."""
        oat_milk_surcharge = self.latteMedium.calculate_drink_price('small')
        oat_milk_surcharge = self.latteMedium.calculate_milk_price('Oat')
        self.assertEqual(oat_milk_surcharge, 4.50 + 0.50)

    def test_menu_item_pricing_invalid_size(self):
        """Test MenuItem raises exception for invalid size."""
        with self.assertRaises(InvalidCustomizationError):
            self.latte.calculate_drink_price('extra-large')

    def test_order_total_with_multiple_items(self):
        """Test Order calculates total correctly."""
        multiple_items_order = self.latte.calculate_drink_price('medium')  # $4.50 * 1.3
        multiple_items_order = self.latte.calculate_milk_price('Oat')  # +$0.50
        expected_value = 4.50 * 1.3 + 0.5
        self.assertEqual(multiple_items_order, expected_value)

    def test_member_discount_applied(self):
        """Test member discount is 10%."""
        discount_item = self.latte.calculate_drink_price('medium')  # $4.50 * 1.3
        discount_item = self.latte.calculate_milk_price('Oat')  # +
        discounted = StaffMember.apply_discount(discount_item, discount_item)  # 10% discount
        expected_discounted = discount_item * 0.90
        self.assertEqual(discounted, expected_discounted) 

    def test_loyalty_points_earned(self):
        """Test loyalty points: $1 = 1 point. earn points on a $10 order."""
        # Add implementation
        self.loyalty.earn_points(self.customer, 10)
        self.assertEqual(self.customer.loyalty_points, 10)


    def test_redeem_points_insufficient(self):
        """Test redeeming with insufficient points raises exception."""
        self.loyalty.earn_points(self.customer, 50)  # Customer has 50 points
        with self.assertRaises(InsufficientPointsError):
            self.loyalty.redeem_points(self.customer, points_to_redeem=100)  # Try to redeem 100 points

if __name__ == '__main__':
    unittest.main()