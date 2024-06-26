from rest_framework import serializers

from .models import Achievement, AchievementCat, Cat, Owner


class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = ('id', 'name')


class CatSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    achievement = AchievementSerializer(many=True)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner')

    def create(self, validated_data):
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
                achivement=current_achievement, cat=cat
            )


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')
