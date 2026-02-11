from django.contrib import admin
from .models import (
    User,
    FeatureFlag,
    UserFeatureOverride,
    GroupFeatureOverride,
    RegionFeatureOverride,
    Movie
)

admin.site.register(User)
admin.site.register(FeatureFlag)
admin.site.register(UserFeatureOverride)
admin.site.register(GroupFeatureOverride)
admin.site.register(RegionFeatureOverride)


admin.site.register(Movie)


# Register your models here.
