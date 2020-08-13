from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseRecipeAttr(viewsets.GenericViewSet,
                     mixins.ListModelMixin, mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serilizer):
        serilizer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttr):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttr):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecepeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrive':
            return serializers.RecipeDetailSerializer
        return self.serializer_class

    def perform_create(self, serial):
        serial.save(user=self.request.user)
