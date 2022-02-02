from django.test import TestCase

from recipe.models import Recipe, Ingredient

class ModelTests(TestCase):

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
        self.recipe_pizza = self.create_database_item()

    def test_create_recipe(self):
        """Test for creating recipe"""
        payload_recipe = {'name': 'Pizza',
                          'description': 'Put it in the oven',
                          }
        recipe = Recipe.objects.create(**payload_recipe)
        payload_ingredient = {
            'name': "cheese",
            'recipe': recipe
        }
        ingredient = Ingredient.objects.create(**payload_ingredient)

        self.assertEqual(recipe.name, payload_recipe['name'])
        self.assertEqual(ingredient.name, payload_ingredient['name'])


    def test_delete_recipe(self):
        """Test delete record and ingrdients deleted"""
        Recipe.objects.filter(pk = self.recipe_pizza.pk).delete()
        recipe_exists = Recipe.objects.all().exists()
        ingredient_exists = Ingredient.objects.all().exists()

        self.assertFalse(recipe_exists)
        self.assertFalse(ingredient_exists)