from rest_framework import mixins, viewsets

from recipe.models import Recipe
from recipe.serializer import RecipeSerializer

class RecipeView(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        search = self.request.GET.get('name')
        queryset = Recipe.objects.all()
        if search is not None:
            queryset = Recipe.objects.filter(name__startswith=search)
        return queryset
