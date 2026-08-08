"""Database initialization and seeding script"""
from app.start import app
from app.extensions import db
from app.models import User, Department
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database and create tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Seed departments
        departments = [
            {"name": "Education", "description": "Educational institutions, schools, colleges", "email": "education@gov.in"},
            {"name": "Healthcare", "description": "Hospitals, clinics, medical facilities", "email": "health@gov.in"},
            {"name": "Infrastructure", "description": "Roads, bridges, public works", "email": "infrastructure@gov.in"},
            {"name": "Transport", "description": "Public transport, traffic issues", "email": "transport@gov.in"},
            {"name": "Water Supply", "description": "Water supply and drainage", "email": "water@gov.in"},
            {"name": "Electricity", "description": "Power supply and electrical issues", "email": "electricity@gov.in"},
            {"name": "Public Safety", "description": "Police, fire, emergency services", "email": "safety@gov.in"},
            {"name": "Others", "description": "Miscellaneous grievances", "email": "general@gov.in"}
        ]
        
        for dept_data in departments:
            existing = Department.query.filter_by(name=dept_data["name"]).first()
            if not existing:
                dept = Department(**dept_data)
                db.session.add(dept)
        
        db.session.commit()
        print(f"✅ Seeded {len(departments)} departments!")
        
        # Create admin user
        admin_email = "admin@grievance.gov.in"
        existing_admin = User.query.filter_by(email=admin_email).first()
        if not existing_admin:
            admin = User(
                name="System Admin",
                email=admin_email,
                password=generate_password_hash("admin123", method='pbkdf2:sha256'),
                role="admin",
                phone="9876543210"
            )
            db.session.add(admin)
            db.session.commit()
            print(f"✅ Created admin user: {admin_email} / admin123")
        else:
            print("ℹ️  Admin user already exists")
        
        print("\n🎉 Database initialization complete!")

if __name__ == "__main__":
    init_database()
