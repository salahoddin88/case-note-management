# 📋 Case Note Management System

A modern, production-ready case note management system built with Django and Next.js, featuring JWT authentication, comprehensive error handling, and Docker deployment.

## 🚀 Features

### Backend (Django + Django Ninja)
- **JWT Authentication** with automatic token refresh
- **RESTful API** with OpenAPI documentation
- **Role-based Access Control** - caseworkers only see assigned clients
- **Custom User Model** with additional caseworker fields
- **Comprehensive Admin Panel** with custom dashboards
- **Database Seeding** with realistic sample data
- **Docker Support** for easy deployment
- **SQLite Database** for simplicity and portability

### Frontend (Next.js + TypeScript)
- **Modern React** with TypeScript and Tailwind CSS
- **Automatic Token Management** with refresh handling
- **Comprehensive Error Handling** with error boundaries
- **Auto-logout** on token expiration
- **Responsive Design** with loading states
- **Real-time Validation** and user feedback

### Security & Best Practices
- **JWT Tokens** with automatic refresh
- **CORS Configuration** for secure cross-origin requests
- **Input Validation** on both frontend and backend
- **Error Boundaries** for graceful error handling
- **Clean Architecture** with separation of concerns

## 🏗️ Architecture

```
📁 Project Structure
├── backend/                    # Django Backend
│   ├── app/                   # Django Project
│   │   ├── accounts/          # User Management & Auth
│   │   ├── clients/           # Client Management
│   │   ├── case_notes/        # Case Note Management
│   │   └── config/            # Django Configuration
│   ├── Dockerfile            # Backend Docker config
│   ├── docker-compose.yml    # Multi-service setup
│   └── requirements.txt      # Python dependencies
├── frontend/                  # Next.js Frontend
│   ├── src/
│   │   ├── app/              # Next.js App Router
│   │   ├── components/       # Reusable UI Components
│   │   ├── services/         # API Service Layer
│   │   └── types/            # TypeScript Definitions
│   └── package.json          # Node.js dependencies
└── test_jwt_api.py           # Comprehensive API Tests
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- Docker (optional)

### Quick Start (Development)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd manaaki
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   cd app
   python manage.py migrate
   python manage.py seed_data  # Create sample data
   python manage.py runserver 0.0.0.0:8000
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api
   - API Documentation: http://localhost:8000/api/docs
   - Django Admin: http://localhost:8000/admin

### Docker Deployment

1. **Development with Docker**
   ```bash
   cd backend
   docker-compose up --build
   ```

The Docker setup automatically runs migrations and seeds sample data during the build process!

## 🔐 Authentication & Users

### Demo Credentials

**Caseworkers:**
- Username: `sarah.smith` - `john.doe`
- Password: `password123`

**Admin:**
- Username: `admin`
- Password: `admin123`

### JWT Token Flow
1. **Login**: POST `/api/auth/login` → Returns access & refresh tokens
2. **API Calls**: Include `Authorization: Bearer <access_token>` header
3. **Auto-refresh**: Frontend automatically refreshes expired tokens
4. **Logout**: POST `/api/auth/logout` → Blacklists refresh token

## 📚 API Documentation

### Authentication Endpoints
```
POST /api/auth/login     # Login with username/password
POST /api/auth/logout    # Logout and blacklist token
POST /api/auth/refresh   # Refresh access token
```

### Client Endpoints
```
GET /api/clients/search?q=<query>  # Search assigned clients
```

### Case Note Endpoints
```
POST /api/case-notes/                    # Create case note
GET /api/case-notes/client/{client_id}   # Get client's case notes
```

### Interactive Documentation
Visit http://localhost:8000/api/docs for full OpenAPI documentation with interactive testing.

## 🧪 Testing

### Django Unit Tests
```bash
# Run all tests
cd backend/app && python manage.py test

# Run tests for specific app
python manage.py test accounts
python manage.py test clients
python manage.py test case_notes

# Run with verbose output
python manage.py test --verbosity=2
```

### Integration Tests
```bash
# Run integration tests (includes API, auth, admin tests)
python manage.py test tests

# Run specific integration test classes
python manage.py test tests.test_integration_api.JWTAPIIntegrationTest
python manage.py test tests.test_integration_api.AdminPanelIntegrationTest
```

### Test Coverage
- ✅ **Unit Tests**: Model validation, business logic, API endpoints
- ✅ **Integration Tests**: Complete authentication flow, end-to-end workflows
- ✅ **Security Tests**: Authorization, data privacy, token management
- ✅ **API Tests**: CRUD operations, error handling, response validation

## 🔧 Configuration

### Environment Variables
```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com

# JWT Settings (configured in settings.py)
ACCESS_TOKEN_LIFETIME=1 hour
REFRESH_TOKEN_LIFETIME=7 days
```

### CORS Configuration
Update `CORS_ALLOWED_ORIGINS` in `backend/app/config/settings.py` for production:
```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
]
```

## 🚀 Deployment

### Production Checklist
- [ ] Update `SECRET_KEY` and `DEBUG=False`
- [ ] Update `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`
- [ ] Set up SSL certificates
- [ ] Configure static file serving
- [ ] Set up monitoring and logging
- [ ] Backup SQLite database regularly

### Production Deployment
```bash
# For production, set environment variables
DEBUG=False SECRET_KEY=your-secret-key docker-compose up --build
```

## 🏛️ Architecture Decisions

### Why JWT over Sessions?
- **Stateless**: No server-side session storage required
- **Scalable**: Works across multiple servers/containers
- **Mobile-friendly**: Perfect for mobile app integration
- **Secure**: Automatic token expiration and refresh

### Why Django Ninja over DRF?
- **FastAPI-style**: Modern, intuitive API development
- **Automatic Documentation**: Built-in OpenAPI/Swagger
- **Type Safety**: Full Python type hints support
- **Performance**: Faster than traditional Django views

### Why Consolidated URLs?
- **Simplicity**: All API routes in one place
- **Maintainability**: Easier to see the complete API structure
- **Performance**: Fewer import statements and routing overhead

### Why SQLite over PostgreSQL?
- **Simplicity**: Zero configuration required
- **Portability**: Single file database, easy to backup
- **Performance**: Excellent for small to medium applications
- **Docker-friendly**: No additional services needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django & Django Ninja for the robust backend framework
- Next.js & React for the modern frontend
- Tailwind CSS for beautiful, responsive styling
- JWT for secure, stateless authentication

---

**Built with ❤️ for community service caseworkers**