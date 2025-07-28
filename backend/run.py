#!/usr/bin/env python3
"""
Climate Platform Backend Runner
"""
import os
import structlog
from app import app, db, User

# Get logger
logger = structlog.get_logger()

if __name__ == '__main__':
    # Get configuration from environment variables
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"Starting Climate Platform Backend on {host}:{port}")
    print(f"Debug mode: {debug_mode}")
    
    # Initialize database and create demo user
    with app.app_context():
        try:
            # Create all database tables
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Create demo user if it doesn't exist
            demo_user = User.query.filter_by(email='admin@climate.com').first()
            if not demo_user:
                demo_user = User(email='admin@climate.com')
                demo_user.set_password('admin123')
                db.session.add(demo_user)
                db.session.commit()
                logger.info("Demo user created successfully", email="admin@climate.com")
            else:
                logger.info("Demo user already exists", email="admin@climate.com", is_active=demo_user.is_active)
            
            # Verify demo user can be found
            verify_user = User.query.filter_by(email='admin@climate.com').first()
            if verify_user:
                logger.info("Demo user verification successful", email=verify_user.email, 
                           has_password=bool(verify_user.password_hash))
            else:
                logger.error("Demo user verification failed - user not found after creation")
                
        except Exception as e:
            logger.error("Failed to initialize database", error=str(e))
    
    logger.info("Climate Platform Backend starting...")
    
    app.run(
        debug=debug_mode,
        host=host,
        port=port,
        threaded=True
    )
