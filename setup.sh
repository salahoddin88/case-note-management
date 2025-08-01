#!/bin/bash
# Quick setup script for Case Note Management System

echo "🚀 Setting up Case Note Management System"
echo "========================================"

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Navigate to Django project
cd app

# Create data directory
mkdir -p data

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Seed database
echo "Seeding database with sample data..."
python manage.py seed_data

echo "✅ Backend setup complete!"
echo ""
echo "🧪 Running tests to verify setup..."
python manage.py test
echo ""
echo "🌐 To start the backend server:"
echo "   cd backend/app && source ../venv/bin/activate && python manage.py runserver"
echo ""

# Frontend setup
cd ../../frontend
echo "📦 Setting up frontend..."

# Install dependencies
if command -v npm &> /dev/null; then
    echo "Installing Node.js dependencies..."
    npm install
    echo "✅ Frontend setup complete!"
    echo ""
    echo "🌐 To start the frontend server:"
    echo "   cd frontend && npm run dev"
else
    echo "⚠️  npm not found. Please install Node.js to set up the frontend."
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📚 Documentation:"
echo "   - API docs: http://localhost:8000/api/docs"
echo "   - Django admin: http://localhost:8000/admin"
echo "   - Frontend: http://localhost:3000"
echo ""
echo "🔐 Demo credentials:"
echo "   - Admin: admin / admin123"
echo "   - Caseworker: caseworker1 / password123"