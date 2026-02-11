from django.db import models

from datetime import date, timedelta

class Movie(models.Model):
    region = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('region', 'name')

    def __str__(self):
        return f"{self.region} - {self.name}"


class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    subscription_status = models.BooleanField(default=False)
    subscription_expiry = models.DateField(null=True, blank=True)
    region = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if self.subscription_status and not self.subscription_expiry:
            self.subscription_expiry = date.today() + timedelta(days=365)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ----------------------------------
# FEATURE FLAG
# ----------------------------------
class FeatureFlag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    default_state = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# ----------------------------------
# USER FEATURE OVERRIDE (NO DUPLICATES)
# ----------------------------------
class UserFeatureOverride(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feature = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE)
    enabled = models.BooleanField()

    class Meta:
        unique_together = ('user', 'feature')   #  prevents duplicates

    def __str__(self):
        return f"{self.user} - {self.feature}"


# ----------------------------------
# GROUP FEATURE OVERRIDE (NO DUPLICATES)
# ----------------------------------
class GroupFeatureOverride(models.Model):
    group_name = models.CharField(max_length=50)
    feature = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE)
    enabled = models.BooleanField()

    class Meta:
        unique_together = ('group_name', 'feature')   #  prevents duplicates

    def __str__(self):
        return f"{self.group_name} - {self.feature}"


# ----------------------------------
# REGION FEATURE OVERRIDE (NO DUPLICATES)
# ----------------------------------
class RegionFeatureOverride(models.Model):
    region = models.CharField(max_length=50)
    feature = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE)
    enabled = models.BooleanField()

    class Meta:
        unique_together = ('region', 'feature')   #  prevents duplicates

    def __str__(self):
        return f"{self.region} - {self.feature}"


