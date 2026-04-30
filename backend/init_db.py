"""
Database Initialization and Setup Script
This script initializes the database with tables and creates a default admin user for testing
"""

import os
import sys
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, MedicalHistory, Session

def init_database():
    """Initialize database with all tables"""
    print("🔧 Initializing database...")
    with app.app_context():
        try:
            # Drop existing tables (optional, comment out to preserve data)
            # db.drop_all()
            
            # Create all tables
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Print table information
            print("\n📋 Created tables:")
            inspector = db.inspect(db.engine)
            for table_name in inspector.get_table_names():
                print(f"  - {table_name}")
                columns = inspector.get_columns(table_name)
                for col in columns:
                    print(f"    • {col['name']} ({col['type']})")
            
            return True
        except Exception as e:
            print(f"✗ Error creating database tables: {str(e)}")
            return False

def create_test_user():
    """Create a test user for development"""
    print("\n👤 Creating test user...")
    with app.app_context():
        try:
            # Check if test user already exists
            existing_user = User.query.filter_by(username='testuser').first()
            if existing_user:
                print("ℹ️  Test user already exists")
                return existing_user
            
            # Create new test user
            test_user = User(
                username='testuser',
                email='testuser@example.com',
                first_name='Test',
                last_name='User',
                age=30,
                gender='M'
            )
            test_user.set_password('password123')
            
            db.session.add(test_user)
            db.session.commit()
            
            print("✓ Test user created successfully")
            print(f"  Username: testuser")
            print(f"  Email: testuser@example.com")
            print(f"  Password: password123")
            
            return test_user
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error creating test user: {str(e)}")
            return None

def add_sample_medical_history(user_id):
    """Add sample medical history record"""
    print("\n📝 Adding sample medical history...")
    with app.app_context():
        try:
            sample_record = MedicalHistory(
                user_id=user_id,
                record_type='general',
                blood_type='O+',
                allergies='Penicillin',
                medications='None',
                blood_pressure='120/80',
                heart_rate=72,
                temperature=98.6,
                weight=70.0,
                height=175.0,
                consultation_notes='Initial health assessment',
                doctor_name='Dr. John Doe'
            )
            
            db.session.add(sample_record)
            db.session.commit()
            
            print("✓ Sample medical history record added")
            return sample_record
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error adding medical history: {str(e)}")
            return None

def show_database_info():
    """Show database information"""
    print("\n📊 Database Information:")
    with app.app_context():
        try:
            user_count = User.query.count()
            history_count = MedicalHistory.query.count()
            
            print(f"  Total Users: {user_count}")
            print(f"  Total Medical Records: {history_count}")
            
            if user_count > 0:
                print("\n  📋 Users:")
                users = User.query.all()
                for user in users:
                    print(f"    - {user.username} ({user.email}) - Created: {user.created_at}")
                    records = MedicalHistory.query.filter_by(user_id=user.id).count()
                    print(f"      Medical Records: {records}")
        except Exception as e:
            print(f"✗ Error retrieving database info: {str(e)}")

def main():
    """Main initialization function"""
    print("=" * 50)
    print("Health AI Database Initialization")
    print("=" * 50)
    
    # Initialize database
    if not init_database():
        print("\n❌ Database initialization failed")
        return False
    
    # Create test user
    test_user = create_test_user()
    
    # Add sample medical history
    if test_user:
        add_sample_medical_history(test_user.id)
    
    # Show database info
    show_database_info()
    
    print("\n" + "=" * 50)
    print("✓ Database initialization completed successfully!")
    print("=" * 50)
    print("\n📚 Next Steps:")
    print("  1. Start the backend server: python app.py")
    print("  2. Test login with:")
    print("     Username: testuser")
    print("     Password: password123")
    print("  3. Access the API at http://localhost:5000")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
