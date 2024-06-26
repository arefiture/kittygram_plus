from rest_framework import serializers

from .models import Achievement, AchievementCat, Cat, Owner


class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = ('id', 'name')


class CatSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField(read_only=True)
    achievements = AchievementSerializer(many=True, required=False)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements')

    def create(self, validated_data):
        # Если не пришли ачивки
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat
        # Убираем из общего словаря достижения и сохраняем его
        achievements = validated_data.pop('achievements')
        # Создаем кота
        cat = Cat.objects.create(**validated_data)
        # Для каждого достижения из списка
        for achivement in achievements:
            # Создадим новую запись или получим существующую
            current_achievement, status = Achievement.objects.get_or_create(
                **achivement
            )
            # И привяжем достижения к котику и наоборот =3
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat
            )
        return cat


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')
