import pytest

from django.test import TestCase
from django.urls import reverse

# from .models import Album, Artist, Contact, Booking


# Front
class TestFront(TestCase):
    
    def test_front_index_page(self):
        """
        test that index page returns a 200
        """
        response = self.client.get(reverse('product:home'))
        self.assertEqual(response.status_code, 200)

    # def test_front_result_page(self):
    #     """
    #     test that index page returns a 200
    #     """
    #     response = self.client.get(reverse('product:result'))
    #     self.assertEqual(response.status_code, 200)

    # def test_front_favorite_page(self):
    #     """
    #     test that index page returns a 200
    #     """
    #     response = self.client.get(reverse('product:favorite'))
    #     self.assertEqual(response.status_code, 200)

    def test_front_parse_favorite_page(self):
        """
        test that index page returns a 200
        """
        response = self.client.get(reverse('product:parse_favorite'))
        self.assertEqual(response.status_code, 200)

    def test_front_info_page(self):
        """
        test that index page returns a 200
        """
        response = self.client.get(reverse('product:home'))
        self.assertEqual(response.status_code, 200)

    def test_front_notice_page(self):
        """
        test that index page returns a 200
        """
        response = self.client.get(reverse('product:notice'))
        self.assertEqual(response.status_code, 200)

    # def test_index_page_top(self):
    #     """
    #     test that index page returns a 200
    #     """
    #     response = self.client.get(reverse('product:home'))
    #     self.assertIs(False)

#     @pytest.mark.django_db(transaction=False)
#     def test_my_user():
#         me = User.objects.get(username='me')
#         assert me.is_superuser



# # Detail Page
# class DetailPageTestCase(TestCase):

#     def setUp(self):
#         # ran before each test.
    
#         impossible = Album.objects.create(title="Transmission Impossible")
#         self.album = Album.objects.get(title='Transmission Impossible')

#     def test_detail_page_returns_200(self):
#         """
#         test that detail page returns a 200 if the item exists
#         """
#         album_id = self.album.id
#         response = self.client.get(reverse('store:detail', args=(album_id,)))
#         self.assertEqual(response.status_code, 200)

#     def test_detail_page_returns_404(self):
#         # test that detail page returns a 404 if the item does not exist
#         album_id = self.album.id + 1
#         response = self.client.get(reverse('store:detail', args=(album_id,)))
#         self.assertEqual(response.status_code, 404)


# # Booking Page
# class BookingPageTestCase(TestCase):
    
#     def setUp(self):
#         Contact.objects.create(name="Freddie", email="fred@queen.forever")
#         impossible = Album.objects.create(title="Transmission Impossible")
#         journey = Artist.objects.create(name="Journey")
#         impossible.artists.add(journey)
#         self.album = Album.objects.get(title='Transmission Impossible')
#         self.contact = Contact.objects.get(name='Freddie')


#     def test_new_booking_is_registered(self):
#         # test that a new booking is made

#         old_bookings = Booking.objects.count() # count bookings before a request

#         album_id = self.album.id
#         name = self.contact.name
#         email =  self.contact.email
        
#         response = self.client.post(reverse('store:detail', args=(album_id,)), {
#             'name': name,
#             'email': email
#         })

#         new_bookings = Booking.objects.count() # count bookings after
#         self.assertEqual(new_bookings, old_bookings + 1) # make sure 1 booking was added

#     # test that a booking belongs to a contact
#     # test that a booking belongs to an album
#     # test that an album is not available after a booking is made