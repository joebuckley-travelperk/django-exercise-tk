from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Recipe, Ingredient


RECIPE_URL = reverse('recipe:recipe-list')

class PublicRecipeApiTests(TestCase):
    """Test for public recipe app"""
    def create_database_item(self):
        """Create database item to test"""
        payload_recipe = {'name': 'Pizza',
                          'description': 'Put it in the oven',
                          }
        recipe_pizza = Recipe.objects.create(**payload_recipe)
        payload_ingredient = {
            'name': "cheese",
            'recipe': recipe_pizza
        }
        Ingredient.objects.create(**payload_ingredient)
        return recipe_pizza

    def setUp(self):
        self.client = APIClient()
        self.recipe_pizza = self.create_database_item()

    def test_create_recipe(self):
        """Test to create a new recipe"""

        payload = {'name': 'Pizza',
                   'description': 'Put it in the oven',
                   'ingredients': [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
                   }
        res = self.client.post(RECIPE_URL, payload, format='json')

        recipe_exist = Recipe.objects.filter(
            name=payload['name']
        ).exists()
        ingredient_exist = Ingredient.objects.filter(
            name=payload['ingredients'][0]['name']
        ).exists()

        self.assertTrue(recipe_exist)
        self.assertTrue(ingredient_exist)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_list_recipes(self):
        """Test to retrieve list of recipes"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], self.recipe_pizza.name)

    def test_get_one_recipe(self):
        """Test to get one recipe"""
        url = RECIPE_URL + str(self.recipe_pizza.id) + '/'
        res = self.client.get(url)
        self.assertEqual(res.data['name'], self.recipe_pizza.name)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_recipe(self):
        url = RECIPE_URL + str(self.recipe_pizza.id) + '/'
        res = self.client.delete(url)

        recipes_exists = Recipe.objects.all().exists()
        ingredients_exists = Ingredient.objects.all().exists()

        self.assertFalse(recipes_exists)
        self.assertFalse(ingredients_exists)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_recipe(self):
        """Update recipe model"""

        payload = {'name': 'Pizza',
                   'description': 'Test update',
                   'ingredients': [{"name": "bread"}]
                   }
        url = RECIPE_URL + str(self.recipe_pizza.pk) + '/'
        res = self.client.put(url, payload, format='json')

        ingredient_old = self.recipe_pizza.ingredients.all()[0]
        self.recipe_pizza.refresh_from_db()
        ingredient_new_exists = self.recipe_pizza.ingredients.filter(name=payload['ingredients'][0]['name']).exists()
        ingredient_old_exists = self.recipe_pizza.ingredients.filter(name=ingredient_old).exists()

        self.assertEqual(self.recipe_pizza.description, payload['description'])
        self.assertTrue(ingredient_new_exists)
        self.assertFalse(ingredient_old_exists)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_search_correct(self):
        """Test search results"""
        url = RECIPE_URL + '?name=Piz'
        res = self.client.get(url)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], self.recipe_pizza.name)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_search_incorrect(self):
        """Test search results"""
        url = RECIPE_URL + '?name=Br'
        res = self.client.get(url)

        self.assertEqual(len(res.data), 0)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

