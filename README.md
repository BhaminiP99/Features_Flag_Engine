# Everest Engineering Challenge – Feature Flag Engine

## Project Overview

This project is a Django-based Feature Flag Engine designed to dynamically control feature access for users based on multiple factors such as subscription status, user-specific overrides, group overrides, and regional configurations.

The system demonstrates how modern applications manage features dynamically, allowing them to be enabled, disabled, or customized without redeploying the application.

Users can:

* Access features based on subscription
* Receive region-specific feature access
* Be assigned custom feature access through overrides
* Lose access automatically when subscriptions expire

The project also includes runtime feature evaluation, REST APIs, an admin dashboard, and unit testing.

---

## Directory Structure

```bash
feature_flag_project/
│
├── feature_flag_project/         # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── feature_flags/                # Core app implementing feature logic
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                 # User, FeatureFlag, Overrides
│   ├── serializers.py            # API serializers
│   ├── views.py                  # Feature evaluation & UI logic
│   ├── tests.py                  # Unit tests for feature engine
│   ├── migrations/
│
├── templates/                    # HTML UI
│   ├── dashboard.html
│   ├── login.html
│   └── my_features.html
│
├── static/                       # CSS/JS assets
│--initial_data.json              # This is the database dump , whwere it creates the data necessory for the feature flag creations required for this project
├── manage.py
└── requirements.txt

```

---

## CHALLENGE #1: FEATURE FLAG DEFINITION

### Required Data

* Feature name
* Global default state (enabled/disabled)

### Assumptions Made

1. Every feature has a default global state.
2. Default state applies if no overrides exist.
3. Feature names are unique.
4. Features can be enabled or disabled at runtime.

---

## CHALLENGE #2: FEATURE OVERRIDES & MUTATIONS

### Required Data

* User-specific overrides
* Group-level overrides
* Region-level overrides

### Assumptions Made

1. User override has highest priority.
2. Group override applies to all subscribed users.
3. Region override applies to users based on location.
4. Overrides can be created/updated through admin or API.
5. Duplicate overrides are prevented using unique constraints.

---

## CHALLENGE #3: RUNTIME FEATURE EVALUATION

### Required Data

* User identity
* Feature name
* Subscription status
* Region

### Evaluation Logic

Feature is enabled based on priority:

```
1. Subscription check
2. User override
3. Group override
4. Region override
5. Global default
```

---

## CHALLENGE #4: SUBSCRIPTION MANAGEMENT

### Assumptions Made

1. Prime features are accessible only to subscribed users.
2. Subscription expiry automatically removes access.
3. Expiry date is auto-generated when subscription is activated.
4. Non-subscribers cannot access premium features.

---

## Points to Note

* Admin can dynamically enable/disable features.
* No redeployment required for feature rollout.
* Supports production-level control patterns.
* Real-time feature evaluation engine implemented.
* Subscription expiry handled automatically.

---

## Installation and Running the Project

### Prerequisites

* Python 3.x
* MySQL installed
* pip available

### Step 1: Clone Repository

```
git clone https://github.com/BhaminiP99/Features_Flag_Engine.git
cd feature_flag_project
```

### Step 2: Create Virtual Environment

```
python -m venv venv311_new
venv311_new\Scripts\activate
```

### Step 3: Install Dependencies

```
pip install -r requirements.txt
```

### Step 4: Configure MySQL

Update `settings.py`:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'featuree_flag_db',
        'USER': '<username>',  		#update the correct username
        'PASSWORD': '<password>',	#update the correct password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
#create a database in MySQL
create database featuree_flags_db; #cli command

# Create a superuser
python manage.py createsuperuser
give username,email address,password



### Step 5: Run Migrations

```
python manage.py makemigrations
python manage.py migrate
```

### Add the dumped data to database using the below command (This creates the necessary feature flags data and avoids the creation time for testing purpose)

python manage.py loaddata initial_data.json
(If encountered any error UTF-16 L error , please change the encoding to UTF-8)


### Step 6: Start Server

```
python manage.py runserver
```
http://127.0.0.1:8000/admin

--give credentials that you created as superuser
(Verify if the features that are created under Feature_Flags and also verify if the data exists inside the features that are loaded using the initial_data.json)


## Using the Application

### Dashboard---http://127.0.0.1:8000/dashboard/           ----> Landing page

* Create users
* Activate subscription -> to avail the extra features
* Login using user credentials

For Non Subscribed users 
* Login using user credentials
	
### Login--http://127.0.0.1:8000/login-user/

* View available features
* View delivery access
* View movie access
* Subscription expiry alerts

---

## Feature Flag Test Suite

This project includes a comprehensive test suite validating:

* Default feature behavior
* User override priority
* Group override logic
* Region override logic
* Subscription expiry handling
* Non-subscriber restrictions

### Running Tests

```
python manage.py test
```

---

## Test Files Overview

### tests.py

* Tests default feature behavior
* Tests override priority
* Tests subscription expiry
* Tests access control

---

## Design Decisions

* Subscription acts as entry gate for premium features.
* Override hierarchy ensures flexible feature rollout.
* Model constraints prevent duplicate overrides.
* Feature engine reusable across UI and APIs.

---

## Real-World Applications

* Feature rollout control
* Premium service enablement
* Emergency feature shutdown
* Region-specific access

---

## Future Improvements

* Caching feature evaluation
* Audit logging
* Multi-tier subscription plans
* Performance optimization



=================================================================================================================================
## Admin Panel Demo (Feature Flag Management with Examples)

This project includes a Django Admin dashboard to manage features, subscriptions, and overrides without writing code.

### 1) Access Admin

Start server:

```
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/admin/
```

Login using superuser credentials.

---

## 2) Create a Feature Flag (Example)

Go to: **Feature Flags → Feature flags → Add**

Example:

* Feature name → `one_day_delivery`
* Default state → Disabled

Save.

Now this feature exists globally but is OFF by default.

---

## 3) Create a User (Example)

Go to: **Feature Flags → Users → Add**

Example:

* Name → `Alex`
* Password → `abc123`
* Region → `India`

Save.

---

## 4) Activate Subscription

Open user **Alex**

* Enable → Subscription status ✔
* Subscription expiry → future date #automatically updates

Save.

Now Alex becomes a Prime user.

---

## 5) Add Group Override (Example)

Go to: **Feature Flags → Group feature overrides → Add**

Example:

* Group name → `prime_users`
* Feature → `one_day_delivery`
* Enabled → True

Save.

Meaning:
All Prime users get one-day delivery enabled.

---

## 6) Add Region Override (Example)

Go to: **Feature Flags → Region feature overrides → Add**

Example:

* Region → `India`
* Feature → `prime_movie_access`
* Enabled → True

Save.

Meaning:
Users from India will get movie access even if global default is OFF.

---

## 7) Add User Override (Example – Disable Feature)

Go to: **Feature Flags → User feature overrides → Add**

Example:

* User → `Alex`
* Feature → `one_day_delivery`
* Enabled → False

Save.

Meaning:
Even though Prime group enables delivery, it is disabled ONLY for Alex.

(User override has highest priority.)

---



### What this Demo Shows

* Feature created via admin
* Subscription activation working
* Group-level rollout functioning
* Region-based access working
* User-specific override priority working
* Runtime evaluation engine behaving correctly
