from .models import (
    FeatureFlag,
    UserFeatureOverride,
    GroupFeatureOverride,
    RegionFeatureOverride,
)

def is_feature_enabled(feature_name, user):
    try:
        feature = FeatureFlag.objects.get(name=feature_name)
    except FeatureFlag.DoesNotExist:
        return False

    #  Check user override
    user_override = UserFeatureOverride.objects.filter(
        user=user, feature=feature
    ).first()

    if user_override:
        return user_override.enabled

    #  Check group override (prime users)
    if user.subscription_status:
        group_override = GroupFeatureOverride.objects.filter(
            group_name="prime_users", feature=feature
        ).first()

        if group_override:
            return group_override.enabled

    #  Check region override
    region_override = RegionFeatureOverride.objects.filter(
        region=user.region, feature=feature
    ).first()

    if region_override:
        return region_override.enabled

    # Fallback to global default
    return feature.default_state
