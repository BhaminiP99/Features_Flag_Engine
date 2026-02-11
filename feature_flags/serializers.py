from rest_framework import serializers


class CreateFeatureSerializer(serializers.Serializer):
    name = serializers.CharField()
    default_state = serializers.BooleanField()


class UserOverrideSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    feature = serializers.CharField()
    enabled = serializers.BooleanField()


class GroupOverrideSerializer(serializers.Serializer):
    group_name = serializers.CharField()
    feature = serializers.CharField()
    enabled = serializers.BooleanField()


class RegionOverrideSerializer(serializers.Serializer):
    region = serializers.CharField()
    feature = serializers.CharField()
    enabled = serializers.BooleanField()


class CheckFeatureSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    feature = serializers.CharField()
class SubscribeUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    plan_days = serializers.IntegerField(required=False, default=365)
