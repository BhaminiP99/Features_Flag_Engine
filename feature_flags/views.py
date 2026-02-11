from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Movie, GroupFeatureOverride
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import User, RegionFeatureOverride
from datetime import date, timedelta
from .models import (
    User,
    FeatureFlag,
    UserFeatureOverride,
    GroupFeatureOverride,
    RegionFeatureOverride
)

from .serializers import (
    CreateFeatureSerializer,
    UserOverrideSerializer,
    GroupOverrideSerializer,
    RegionOverrideSerializer,
    CheckFeatureSerializer,
    SubscribeUserSerializer
)

def is_feature_enabled(user, feature):

    # expiry check
    if user.subscription_expiry and user.subscription_expiry < date.today():
        user.subscription_status = False
        user.save()

    #  If NOT subscribed → no prime features
    if not user.subscription_status:
        return False

    #  USER override (highest priority)
    user_override = UserFeatureOverride.objects.filter(user=user, feature=feature).first()
    if user_override:
        return user_override.enabled

    #  GROUP override
    group_override = GroupFeatureOverride.objects.filter(
        group_name="prime_users",
        feature=feature
    ).first()

    if group_override:
        return group_override.enabled

    #  REGION override
    region_override = RegionFeatureOverride.objects.filter(
        region=user.region,
        feature=feature
    ).first()

    if region_override:
        return region_override.enabled

    #  DEFAULT
    return feature.default_state


# -----------------------------
# SUBSCRIPTION API
# -----------------------------
@swagger_auto_schema(method='post', request_body=SubscribeUserSerializer)
@api_view(['POST'])
def subscribe_user(request):

    serializer = SubscribeUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_id = serializer.validated_data['user_id']

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    user.subscription_status = True
    user.subscription_expiry = date.today() + timedelta(days=365)
    user.save()

    return Response({
        "message": "User upgraded to Prime",
        "expiry": user.subscription_expiry
    })

# -----------------------------
# CREATE FEATURE
# -----------------------------
@swagger_auto_schema(method='post', request_body=CreateFeatureSerializer)
@api_view(['POST'])
def create_feature(request):

    serializer = CreateFeatureSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    feature = FeatureFlag.objects.create(
        name=serializer.validated_data['name'],
        default_state=serializer.validated_data['default_state']
    )
    return Response({"message": "Feature created", "feature": feature.name})

# -----------------------------
# USER OVERRIDE
# -----------------------------
@swagger_auto_schema(method='post', request_body=UserOverrideSerializer)
@api_view(['POST'])
def add_user_override(request):

    serializer = UserOverrideSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = User.objects.get(id=serializer.validated_data['user_id'])
    feature = FeatureFlag.objects.get(name=serializer.validated_data['feature'])
    UserFeatureOverride.objects.update_or_create(
    user=user,
    feature=feature,
    defaults={"enabled": serializer.validated_data['enabled']}
    )
    return Response({"message": "User override added"})


# -----------------------------
# GROUP OVERRIDE
# -----------------------------
@swagger_auto_schema(method='post', request_body=GroupOverrideSerializer)
@api_view(['POST'])
def add_group_override(request):

    serializer = GroupOverrideSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    feature = FeatureFlag.objects.get(name=serializer.validated_data['feature'])
    GroupFeatureOverride.objects.update_or_create(
    group_name=serializer.validated_data['group_name'],
    feature=feature,
    defaults={"enabled": serializer.validated_data['enabled']}
    )

    return Response({"message": "Group override added"})


# -----------------------------
# REGION OVERRIDE
# -----------------------------
@swagger_auto_schema(method='post', request_body=RegionOverrideSerializer)
@api_view(['POST'])
def add_region_override(request):

    serializer = RegionOverrideSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    feature = FeatureFlag.objects.get(name=serializer.validated_data['feature'])
    RegionFeatureOverride.objects.update_or_create(
    region=serializer.validated_data['region'],
    feature=feature,
    defaults={"enabled": serializer.validated_data['enabled']}
    )

    return Response({"message": "Region override added"})


# -----------------------------
# FEATURE EVALUATION ENGINE
# -----------------------------
@swagger_auto_schema(method='post', request_body=CheckFeatureSerializer)
@api_view(['POST'])
def check_feature(request):

    serializer = CheckFeatureSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = User.objects.get(id=serializer.validated_data['user_id'])
    feature = FeatureFlag.objects.get(name=serializer.validated_data['feature'])

    #  EXPIRY ENGINE
    if user.subscription_expiry:
        if user.subscription_expiry < date.today():
            user.subscription_status = False
            user.save()

    #  USER override
    user_override = UserFeatureOverride.objects.filter(user=user, feature=feature).first()
    if user_override:
        return Response({"enabled": user_override.enabled, "source": "USER"})

    #  GROUP override (only if subscribed)
    if user.subscription_status:
        group_override = GroupFeatureOverride.objects.filter(
            group_name="prime_users",
            feature=feature
        ).first()

        if group_override:
            return Response({"enabled": group_override.enabled, "source": "GROUP"})

    #  REGION override
    region_override = RegionFeatureOverride.objects.filter(
        region=user.region,
        feature=feature
    ).first()

    if region_override:
        return Response({"enabled": region_override.enabled, "source": "REGION"})

    #  DEFAULT
    return Response({"enabled": feature.default_state, "source": "DEFAULT"})


# -----------------------------
# GET APIs
# -----------------------------
@api_view(['GET'])
def list_users(request):
    users = User.objects.all().values()
    return Response(users)


@api_view(['GET'])
def list_features(request):
    features = FeatureFlag.objects.all().values()
    return Response(features)


@api_view(['GET'])
def list_user_overrides(request):
    data = UserFeatureOverride.objects.all().values()
    return Response(data)


@api_view(['GET'])
def list_group_overrides(request):
    data = GroupFeatureOverride.objects.all().values()
    return Response(data)


@api_view(['GET'])
def list_region_overrides(request):
    data = RegionFeatureOverride.objects.all().values()
    return Response(data)
from django.shortcuts import render

def dashboard(request):
    users = User.objects.all()
    features = FeatureFlag.objects.all()
    group_overrides = GroupFeatureOverride.objects.all()
    region_overrides = RegionFeatureOverride.objects.all()

    return render(request, "dashboard.html", {
        "users": users,
        "features": features,
        
    })
# ----------------------------------
# UI: CREATE USER FROM DASHBOARD
# ----------------------------------
def create_user(request):
    if request.method == "POST":

        name = request.POST.get("name")
        password = request.POST.get("password")
        region = request.POST.get("region")

        # safety check
        if not password:
            return redirect("/dashboard/")

        User.objects.create(
            name=name,
            password=password,
            region=region,
            subscription_status=False
        )

        return redirect("/dashboard/")



# ----------------------------------
# UI: SUBSCRIBE USER FROM DASHBOARD
# ----------------------------------

def subscribe_user_ui(request):

    if request.method == "POST":
        name = request.POST.get("name")

        try:
            user = User.objects.get(name=name)
        except User.DoesNotExist:
            messages.error(request, "User not found. Subscription failed.")
            return redirect("/dashboard/")

        # activate subscription
        user.subscription_status = True
        user.subscription_expiry = date.today() + timedelta(days=365)
        user.save()
        messages.success(request, "Subscription activated successfully!")
    return redirect("/dashboard/")


def login_view(request):

    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")

        try:
            user = User.objects.get(name=name, password=password)
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid login"})

       
        #  Expiry check
        subscription_expired = False

        if user.subscription_expiry:
            if user.subscription_expiry < date.today():
                user.subscription_status = False
                user.save()
                subscription_expired = True

        # MOVIES (available to all users by region)
    
        movies = []

        if is_feature_enabled(user, FeatureFlag.objects.get(name="prime_movie_access")):
            movies_qs = Movie.objects.filter(region__iexact=user.region)
            movies = [m.name for m in movies_qs]
           
        #  PRIME FEATURES → USING FEATURE ENGINE

        prime_features = []

        all_features = FeatureFlag.objects.all()

        for feature in all_features:
            if is_feature_enabled(user, feature):
                prime_features.append(feature.name)
        delivery_access = is_feature_enabled(
            user,
            FeatureFlag.objects.get(name="one_day_delivery")
        )

        # render page
        return render(request, "my_features.html", {
            "user": user,
            "movies": movies,
            "prime_features": prime_features,
            "delivery_access": delivery_access,
            "not_subscribed": not user.subscription_status,
            "subscription_expired": subscription_expired
        })

    return render(request, "login.html")

