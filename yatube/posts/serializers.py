from rest_framework import serializers
from posts.models import Post, Group, Tag, TagPost

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

class PostSerializer(serializers.ModelSerializer):
    publication_date = serializers.CharField(source='pub_date', read_only=True)
    group = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field='slug',
        required=False,
    )
    tag = TagSerializer(many=True, required=False)
    character_quantity = serializers.SerializerMethodField()
    class Meta:
        model = Post
        read_only_fields = ('author',)
        fields = ('id', 'character_quantity', 'text', 'author', 'publication_date', 'group', 'tag')
    
    def get_character_quantity(self, obj):
        return len(obj.text)

    def create(self, validated_data):
        if 'tag' not in self.initial_data:
            post = Post.objects.create(**validated_data)
            return post
        tags = validated_data.pop('tag')
        post = Post.objects.create(**validated_data)

        for tag in tags:
            current_tag, status = tag.objects.get_or_create(**tag)
            TagPost.objects.create(tag=current_tag, post=post)
        return post
