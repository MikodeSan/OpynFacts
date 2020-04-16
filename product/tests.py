from django.test import TestCase


# Index page
    # test that index page returns a 200

class IndexPageTestCase(TestCase):
    def test_index_page(self):
        self.assertEqual('a', 'a')
        
# Detail Page
    # test that detail page returns a 200 if the item exists
    # test that detail page returns a 404 if the item does not exist

# Booking Page
    # test that a new booking is made
    # test that a booking belongs to a contact
    # test that a booking belongs to an album
    # test that an album is not available after a booking is made