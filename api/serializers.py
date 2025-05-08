from rest_framework import serializers
from challenges.models import Challenge
from entries.models import Entry

class ChallengeSerializer(serializers.ModelSerializer):

    entries = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model  = Challenge
        fields = ['id','title','slug','description','start_date','end_date','tags', 'entries']

    def validate_title(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Title must be at least 2 characters long."
            )
        return value

    def validate(self, data):
        start = data.get('start_date')
        end   = data.get('end_date')
        if start and end and end < start:
            raise serializers.ValidationError({
                'end_date': "End date must be the same or after start date."
            })
        return data

class EntrySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    challenge = serializers.StringRelatedField(read_only=True)

    class Meta:
        model  = Entry
        fields = ['id','challenge','user','title','description','image','submitted_at']
        read_only_fields = ['submitted_at', 'user', 'challenge']

    def validate(self, data):
        challenge = self.context['request'].data.get('challenge')
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        if 'challenge' in request.data:
            from challenges.models import Challenge as C
            slug = request.data['challenge']
            validated_data['challenge'] = C.objects.get(slug=slug)
        return super().create(validated_data)