# """
# This file demonstrates writing tests using the unittest module. These will pass
# when you run "manage.py test".

# Replace this with more appropriate tests for your application.
# """

# from django.test import TestCase

# class RMUserTestCase(TestCase):

#     def test_is_standard(self):
#         "Is this user a standard account type?"
#         user = models.RMUser()
#         self.assertTrue(user.is_standard)

#     def test_is_standard_advanced(self):
#         user = models.RMUser(account=models.RMUser.ADVANCED)
#         self.assertFalse(user.is_standard)

#     def test_is_standard_premium(self):
#         user = models.RMUser(account=models.RMUser.PREMIUM)
#         self.assertFalse(user.is_standard)

#     def test_upgrade_standard(self):
#         user = models.RMUser()
#         self.assertEqual(models.RMUser.STANDARD, user.account)
#         user.upgrade()
#         self.assertEqual(models.RMUser.ADVANCED, user.account)



# if __name__ == '__main__':
#     unittest.main()
