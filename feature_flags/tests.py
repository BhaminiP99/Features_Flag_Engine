# Create your tests here.
from django.test import TestCase
from datetime import date, timedelta

from .models import (
    User,
    FeatureFlag,
    UserFeatureOverride,
    GroupFeatureOverride,
    RegionFeatureOverride
)

from .views import is_feature_enabled


class FeatureFlagEngineTest(TestCase):

    def setUp(self):
        # create feature
        self.delivery = FeatureFlag.objects.create(
            name="one_day_delivery",
            default_state=True
        )

        # create user
        self.user = User.objects.create(
            name="alexa",
            password="abc",
            subscription_status=True,
            subscription_expiry=date.today() + timedelta(days=365),
            region="USA"
        )

    #  DEFAULT
    def test_default_feature_enabled(self):
        enabled = is_feature_enabled(self.user, self.delivery)
        self.assertTrue(enabled)

    # USER OVERRIDE PRIORITY
    def test_user_override_priority(self):
        UserFeatureOverride.objects.create(
            user=self.user,
            feature=self.delivery,
            enabled=False
        )

        enabled = is_feature_enabled(self.user, self.delivery)
        self.assertFalse(enabled)

    #  GROUP OVERRIDE
    def test_group_override(self):
        GroupFeatureOverride.objects.create(
            group_name="prime_users",
            feature=self.delivery,
            enabled=False
        )

        enabled = is_feature_enabled(self.user, self.delivery)
        self.assertFalse(enabled)

    #  REGION OVERRIDE
    def test_region_override(self):
        RegionFeatureOverride.objects.create(
            region="USA",
            feature=self.delivery,
            enabled=False
        )

        enabled = is_feature_enabled(self.user, self.delivery)
        self.assertFalse(enabled)

    #  EXPIRY CHECK
    def test_subscription_expired(self):
        self.user.subscription_expiry = date.today() - timedelta(days=1)
        self.user.save()

        enabled = is_feature_enabled(self.user, self.delivery)
        self.assertFalse(enabled)

    #  NON SUBSCRIBER
    def test_non_subscriber_blocked(self):
        self.user.subscription_status = False
        self.user.save()

        enabled = is_feature_enabled(self.user, self.delivery)
        self.assertFalse(enabled)

