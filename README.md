# FastAPI Backend Base

A modern, production-ready Python backend built with FastAPI, featuring MySQL, Redis, JWT authentication, and comprehensive tooling.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **MySQL** - Robust relational database with SQLAlchemy ORM
- **Redis** - High-performance caching and session storage
- **JWT Authentication** - Secure token-based authentication
- **Pydantic** - Data validation and serialization
- **Alembic** - Database migrations
- **Docker** - Containerization support
- **Testing** - Comprehensive test suite with pytest
- **Middleware** - Logging, rate limiting, CORS
- **API Documentation** - Auto-generated OpenAPI/Swagger docs

## 📁 Project Structure

\`\`\`
app/
├── api/                    # API routes
│   └── v1/
│       ├── endpoints/      # API endpoints
│       └── api.py         # API router
├── core/                   # Core functionality
│   ├── config.py          # Settings and configuration
│   ├── database.py        # Database connection
│   ├── redis.py           # Redis connection
│   ├── security.py        # Security utilities
│   └── exceptions.py      # Custom exceptions
├── models/                 # SQLAlchemy models
├── schemas/                # Pydantic schemas
├── middleware/             # Custom middleware
├── utils/                  # Utility functions
└── main.py                # Application entry point

alembic/                    # Database migrations
tests/                      # Test suite
\`\`\`

## 🛠️ Installation

### Using Docker (Recommended)

1. Clone the repository:
\`\`\`bash
git clone <repository-url>
cd fastapi-backend
\`\`\`

2. Copy environment file:
\`\`\`bash
cp .env.example .env
\`\`\`

3. Start with Docker Compose:
\`\`\`bash
docker-compose up -d
\`\`\`

### Manual Installation

1. Install Python 3.11+
2. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Set up MySQL and Redis
4. Configure environment variables in `.env`
5. Run migrations:
\`\`\`bash
alembic upgrade head
\`\`\`

6. Start the application:
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

\`\`\`env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/database
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
\`\`\`

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 🧪 Testing

Run the test suite:
\`\`\`bash
pytest
\`\`\`

Run with coverage:
\`\`\`bash
pytest --cov=app
\`\`\`

## 🗄️ Database Migrations

Create a new migration:
\`\`\`bash
alembic revision --autogenerate -m "Description"
\`\`\`

Apply migrations:
\`\`\`bash
alembic upgrade head
\`\`\`

## 🔐 Authentication

The API uses JWT tokens for authentication:

1. Register: `POST /api/v1/auth/register`
2. Login: `POST /api/v1/auth/login`
3. Use the returned token in the `Authorization: Bearer <token>` header

## 📊 Health Checks

- **API Health**: `GET /api/v1/health/`
- **Database Health**: `GET /api/v1/health/db`
- **Redis Health**: `GET /api/v1/health/redis`

## 🚀 Deployment

### Vercel Deployment

1. Install Vercel CLI:
\`\`\`bash
npm i -g vercel
\`\`\`

2. Deploy:
\`\`\`bash
vercel --prod
\`\`\`

3. Set environment variables in Vercel dashboard:
   - `DATABASE_URL`
   - `REDIS_URL`
   - `SECRET_KEY`
   - `ENVIRONMENT=production`

### Railway Deployment

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on git push

### Render Deployment

1. Connect your GitHub repository to Render
2. Use the `render.yaml` configuration file
3. Set up database and Redis services

### Heroku Deployment

1. Install Heroku CLI
2. Create Heroku app:
\`\`\`bash
heroku create your-app-name
\`\`\`

3. Set environment variables:
\`\`\`bash
heroku config:set DATABASE_URL=your-database-url
heroku config:set REDIS_URL=your-redis-url
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ENVIRONMENT=production
\`\`\`

4. Deploy:
\`\`\`bash
git push heroku main
\`\`\`

### Docker Production

\`\`\`bash
docker build -t fastapi-backend .
docker run -p 8000:8000 -e ENVIRONMENT=production fastapi-backend
\`\`\`

### Environment Variables for Production

Required environment variables:
- `DATABASE_URL` - Your production database URL
- `REDIS_URL` - Your production Redis URL  
- `SECRET_KEY` - A secure secret key
- `ENVIRONMENT=production`
- `DEBUG=false`

Optional:
- `BACKEND_CORS_ORIGINS` - Allowed CORS origins
- `ALLOWED_HOSTS` - Allowed host headers
- Email configuration for notifications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
