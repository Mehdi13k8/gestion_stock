
#-*- coding: utf-8 -*-
from django.test import TestCase, Client
from .models import *
from django.utils import timezone
import unittest
from selenium import webdriver
from django.urls import reverse
from .forms import ChoseForm
from .forms import ClientSignUpForm, PartenaireSignUpForm, ConnexionForm,TransporteurSignUpForm
from django.contrib.auth.forms import UserCreationForm

# models test
class ChoseTest(TestCase):


	def create_Chose(self, title="only a test", body="yes, this is only a test"):
		return chose.objects.create(title=title, body=body, Date=timezone.now())

	def test_Chose_creation(self):
		w = self.create_Chose()
		self.assertTrue(isinstance(w, chose))
		self.assertEqual(w.__unicode__(), w.title)


		# views (uses reverse)

	def test_chose_list_view(self):
		w = self.create_Chose()
		url = reverse('chosee')
		resp = self.client.get(url)
		print(w.title)
		self.assertEqual(resp.status_code, 200)
		self.assertIn(w.title, resp.content.decode('utf-8'))

	def test_valid_form(self):
		w = chose.objects.create(title='Foo', body='xwcx')
		data = {'title': w.title, 'body': w.body,}
		form = ChoseForm(data=data)
		self.assertTrue(form.is_valid())
        

	
	def test_invalid_form(self):
		w = chose.objects.create(title='Foo', body='')
		data = {'title': w.title, 'body': w.body,}
		form = ChoseForm(data=data)
		self.assertFalse(form.is_valid())
        


#test formulaire d'inscription client/partenaire/transporteur
class TestSignup(unittest.TestCase):


    def setUp(self):

    	self.driver1 = webdriver.Firefox(executable_path = 'geckodriver')
    
    def test_signupClient_fire(self):
        
        
        self.driver1.get("http:/localhost:8000/flexible/compte/signup/testclient/")
        self.driver1.find_element_by_id('id_username').send_keys("test ")
        self.driver1.find_element_by_id('id_nom').send_keys("test")
        self.driver1.find_element_by_id('id_adresse').send_keys("test ")
        
        
        self.driver1.find_element_by_id('submit').click()
        
        self.assertIn("http://localhost:8000/", self.driver1.current_url)

    def tearDown(self):
        self.driver1.quit



class TestOffre(unittest.TestCase):
   

    def setUp(self):
       
        
        self.driver = webdriver.Firefox(executable_path = 'geckodriver')

    #test de connexion
    def test_offre_create1(self):
        self.driver.get("http:/localhost:8000/flexible/")
        self.driver.find_element_by_id('id_username').send_keys("karim")
        self.driver.find_element_by_id('id_password').send_keys("abdou555") 
        
        self.driver.find_element_by_id('submit').click()
        
        self.assertIn("http://localhost:8000/", self.driver.current_url)

    #test de creation d'offre
    def test_offre_create2(self):
        self.driver.get("http:/localhost:8000/flexible/offre/testclient/")
           
      
        
        self.driver.find_element_by_id('id_designation').send_keys("test ")
        self.driver.find_element_by_id('id_quantité').send_keys(4)
     
        
      
    
        self.driver.find_element_by_id('id_datearrive').send_keys("29/03/2019")
        
        
        self.driver.find_element_by_id('submit2').click()
    
        self.assertIn("http://localhost:8000/", self.driver.current_url)
        
    def tearDown(self):
        self.driver.quit

	
if __name__ == '__main__':
	unittest.main()

