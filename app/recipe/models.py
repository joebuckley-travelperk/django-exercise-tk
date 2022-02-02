from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)