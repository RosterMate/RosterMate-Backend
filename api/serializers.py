from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

class CustomTokenObtainPairSerializer(serializers.Serializer):
    token = serializers.CharField()
    refresh = serializers.CharField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    user_role = serializers.CharField()

    def create(self, validated_data):
        refresh = RefreshToken.for_user(self.user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': self.user.id,
            'username': self.user.username,
            'user_role': self.user.role  # Replace 'role' with the actual field in your user model
        }
        return data
