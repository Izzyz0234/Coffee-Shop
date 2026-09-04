import unittest
from coffee_shop_refactored import MenuItem, Order, Customer, LoyaltyProgram, StaffDrink, StaffMember
from coffee_shop_exceptions import InvalidDiscountError, InsufficientPointsError, InvalidCustomizationError

class TestCoffeeShop(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.latte = MenuItem("Latte", 4.50, ['small', 'medium', 'large'], ['Whole', 'Skim', 'Oat', 'Almond'])
        self.latteMedium = MenuItem("Latte", 4.50, ['small', 'medium', 'large'], ['Whole', 'Skim', 'Oat', 'Almond'])
        self.mocha = MenuItem("Mocha", 5.00, ['small', 'medium', 'large'], ['Whole', 'Skim', 'Oat', 'Almond'])
        self.customer = Customer("Alice", member=True)
        self.staffMember = StaffMember("Bob")
        self.staffDrink = StaffDrink(self.latte, 'medium')
        self.loyalty = LoyaltyProgram()

    def test_menu_item_pricing_small(self):
        """Test MenuItem calculates small drink price correctly."""
        price = self.latte.calculate_drink_price('small')
        expected_price = 4.50
        print(f"Calculated price for small latte: {price}, Expected: {expected_price}")
        self.assertEqual(price, expected_price)

    def test_menu_item_pricing_medium(self):
        """Test MenuItem calculates medium drink price correctly."""    
        price_medium = self.latteMedium.calculate_drink_price('medium')
        expected_price = 4.50 * 1.3
        print(f"Calculated price for medium latte: {price_medium}, Expected: {expected_price}")
        self.assertEqual(price_medium, expected_price)

    def test_menu_item_milk_oat(self):
        """Test MenuItem calculates price with oat milk correctly."""
        oat_milk_surcharge = self.latteMedium.calculate_drink_price('small')
        oat_milk_surcharge = self.latteMedium.calculate_milk_price('Oat')
        expected_price = 4.50 + 0.50
        print(f"Calculated price with oat milk: {oat_milk_surcharge}, Expected: {expected_price}")
        self.assertEqual(oat_milk_surcharge, expected_price)

    def test_menu_item_pricing_invalid_size(self):
        """Test MenuItem raises exception for invalid size."""
        with self.assertRaises(InvalidCustomizationError):
            self.latte.calculate_drink_price('extra-large')

    def test_order_total_with_multiple_items(self):
        """Test Order calculates total correctly."""
        multiple_items_order = int(self.latte.calculate_drink_price('small'))  # $4.50 * 1.3
        multiple_items_order = int(self.latte.calculate_milk_price('Oat'))  # +$0.50
        expected_value = int(4.50 + 0.5)
        print(f"Calculated order total: {multiple_items_order}, Expected: {expected_value}")
        self.assertEqual(multiple_items_order, expected_value)

    def test_member_discount_applied(self):
        """Test member discount is 10%."""
        discount_item = self.latte.calculate_drink_price('medium')  # $4.50 * 1.3
        discount_item = self.latte.calculate_milk_price('Oat')  # +
        discounted = StaffMember.apply_discount(int(discount_item), int(discount_item))  # 10% discount
        expected_discounted = int(discount_item) * 0.90
        print(f"Discounted price: {discounted}, Expected: {expected_discounted}")
        self.assertEqual(discounted, expected_discounted) 

    def test_loyalty_points_earned(self):
        """Test loyalty points: $1 = 1 point."""
        # Add implementation
        self.loyalty.earn_points(self.customer, 10)
        print(f"Loyalty points after earning: {self.customer.loyalty_points}")
        self.assertEqual(self.customer.loyalty_points, 10)

    def test_redeem_points_insufficient(self):
        """Test redeeming with insufficient points raises exception."""
        with self.assertRaises(InsufficientPointsError):
            self.loyalty.redeem_points(self.customer, points_to_redeem=10)

    def test_get_receipt_for_staff_drink(self):
        """Test receipt generation for staff drink."""
        receipt = self.staffDrink.get_receipt()
        print(receipt)
        self.assertIn("Staff Drink", receipt)

# print

if __name__ == '__main__':
    unittest.main()