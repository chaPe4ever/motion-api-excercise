# Motion API

A Django REST Framework (DRF) based social media API that allows users to create posts, follow each other, like posts, and interact with a social feed.

## Features

- **User Management**
  - User registration and authentication using JWT (JSON Web Tokens)
  - Custom user model with email as the username field
  - User profiles with customizable fields (job, avatar, location, phone number, about me, hashtags)

- **Social Features**
  - Create, read, update, and delete posts
  - Follow/unfollow other users
  - Like/unlike posts
  - View posts from users you follow (following feed)
  - View posts you've liked
  - View posts by a specific user

- **Content Management**
  - Text-based posts with content
  - Multiple images per post (via URL)
  - Post likes tracking
  - Timestamps for creation and updates

- **API Documentation**
  - Interactive Swagger UI documentation
  - ReDoc documentation
  - OpenAPI schema support

## Tech Stack

- **Backend Framework**: Django 6.0
- **API Framework**: Django REST Framework (DRF)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (development) / PostgreSQL (production)
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Static Files**: WhiteNoise

## Project Structure

```
motion/
├── motion/              # Main Django project settings
│   ├── settings.py     # Project configuration
│   ├── urls.py         # Main URL routing
│   ├── permissions.py  # Custom permission classes
│   └── authentication.py
├── user/               # User app
│   ├── models.py      # Custom User model (email-based)
│   ├── serializers.py # User serializers
│   ├── views.py       # User API views
│   └── urls.py        # User URL routes
├── user_profile/      # User Profile app
│   ├── models.py      # UserProfile model
│   └── serializers.py # Profile serializers
├── post/              # Post app
│   ├── models.py      # Post model
│   ├── serializers.py # Post serializers
│   ├── views.py       # Post API views
│   └── urls.py        # Post URL routes
├── follow/            # Follow app
│   ├── models.py      # Follow relationship model
│   ├── views.py       # Follow API views
│   └── urls.py        # Follow URL routes
├── image/             # Image app
│   ├── models.py      # Image model
│   └── serializers.py # Image serializers
└── manage.py          # Django management script
```

## Installation

### Prerequisites

- Python 3.12+
- pip
- virtualenv (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd motion
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication

- `POST /backend/api/token/` - Obtain JWT token (email and password)

### Users

- `GET /backend/api/users/` - List all users (admin only)
- `POST /backend/api/users/` - Register a new user (public)
- `GET /backend/api/users/{id}/` - Get user details (public)
- `PUT/PATCH /backend/api/users/{id}/` - Update user (owner/admin only)
- `DELETE /backend/api/users/{id}/` - Delete user (owner/admin only)

### Posts

- `GET /backend/api/posts/` - List all posts (authenticated)
- `POST /backend/api/posts/` - Create a new post (authenticated)
- `GET /backend/api/posts/{id}/` - Get post details (authenticated)
- `PUT/PATCH /backend/api/posts/{id}/` - Update post (owner/admin only)
- `DELETE /backend/api/posts/{id}/` - Delete post (owner/admin only)
- `POST /backend/api/posts/toggle-like/{post_id}/` - Like/unlike a post (authenticated)
- `GET /backend/api/posts/likes/` - Get posts you've liked (authenticated)
- `GET /backend/api/posts/following/` - Get posts from users you follow (authenticated)
- `GET /backend/api/posts/user/{user_id}/` - Get posts by a specific user (public)

### Follow

- `POST /backend/api/followers/toggle-follow/{user_id}/` - Follow/unfollow a user (authenticated)
- `GET /backend/api/followers/followers/` - Get your followers (authenticated)
- `GET /backend/api/followers/following/` - Get users you're following (authenticated)

### Documentation

- `GET /swagger/` - Swagger UI documentation
- `GET /redoc/` - ReDoc documentation
- `GET /swagger.json` - OpenAPI JSON schema
- `GET /swagger.yaml` - OpenAPI YAML schema

## Authentication

Motion API uses JWT (JSON Web Token) authentication. To authenticate:

1. **Get a token** by calling `POST /backend/api/token/` with your email and password:
   ```json
   {
     "email": "user@example.com",
     "password": "yourpassword"
   }
   ```

2. **Use the token** in subsequent requests:
   - In Swagger UI: Click "Authorize" and paste your token
   - In API clients: Include header `Authorization: Bearer YOUR_TOKEN`

## Usage Examples

### Register a New User

```bash
curl -X POST http://localhost:8000/backend/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Get JWT Token

```bash
curl -X POST http://localhost:8000/backend/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### Create a Post

```bash
curl -X POST http://localhost:8000/backend/api/posts/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is my first post!",
    "images": [
      {"image": "https://example.com/image1.jpg"},
      {"image": "https://example.com/image2.jpg"}
    ]
  }'
```

### Follow a User

```bash
curl -X POST http://localhost:8000/backend/api/followers/toggle-follow/2/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Like a Post

```bash
curl -X POST http://localhost:8000/backend/api/posts/toggle-like/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Permissions

The API implements several permission classes:

- **IsAdmin**: Only staff, superusers, or users in "Admins"/"Moderators" groups
- **IsOwnerOrAdmin**: Object owner or admin
- **IsAuthenticated**: Any authenticated user
- **AllowAny**: Public access (for user registration and viewing)

## Models

### User
- Custom user model with email as username
- Fields: email, username, first_name, last_name, created

### UserProfile
- One-to-one relationship with User
- Fields: job, avatar, location, phone_number, about_me, user_hashtags, updated

### Post
- Belongs to a UserProfile
- Fields: content, created, updated
- Many-to-many relationship with User (likes)

### Follow
- Represents follower-following relationships
- Unique constraint on (follower, following)

### Image
- Belongs to a Post
- Fields: image (URL)

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Accessing Admin Panel

Visit `http://localhost:8000/admin/` and log in with your superuser credentials.

## Production Deployment

See `DEPLOYMENT.md` for production deployment instructions.

## Database Schema (ORM)

The following diagram illustrates the relationships between the models in the Motion API:

![Motion ORM Entities](assets/Motion%20ORM%20Entities.svg)

### Entity Relationships

- **User** ↔ **UserProfile**: One-to-One relationship (each user has one profile)
- **User** ↔ **Post**: Many-to-Many relationship through likes (users can like multiple posts)
- **UserProfile** ↔ **Post**: One-to-Many relationship (a profile can have multiple posts)
- **Post** ↔ **Image**: One-to-Many relationship (a post can have multiple images)
- **User** ↔ **Follow**: Self-referential Many-to-Many relationship (users can follow other users)

## License

BSD License


