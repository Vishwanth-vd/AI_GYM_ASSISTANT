"""
Database Management Module
Handles all database operations for the AI Fitness Assistant
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import json


class Database:
    """Database manager for user data, profiles, and progress tracking."""
    
    def __init__(self, db_path: str = "user_data/fitness_app.db"):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_database(self):
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                height REAL,
                weight REAL,
                goal_weight REAL,
                goal TEXT,
                experience TEXT,
                activity_level TEXT,
                diet_preference TEXT,
                bmi REAL,
                bmr REAL,
                tdee REAL,
                profile_complete BOOLEAN DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Progress table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                weight REAL,
                body_fat REAL,
                waist REAL,
                chest REAL,
                arms REAL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        conn.close()
    
    # User operations
    def create_user(self, username: str, email: str, password_hash: str) -> Optional[int]:
        """Create a new user and return user ID."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            """, (username, email, password_hash))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return user_id
        except sqlite3.IntegrityError:
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def update_last_login(self, user_id: int):
        """Update user's last login timestamp."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users SET last_login = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (user_id,))
        
        conn.commit()
        conn.close()
    
    # Profile operations
    def create_profile(self, user_id: int, profile_data: Dict) -> bool:
        """Create user profile."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO profiles (
                    user_id, name, age, gender, height, weight, goal_weight,
                    goal, experience, activity_level, diet_preference,
                    bmi, bmr, tdee, profile_complete
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                profile_data.get('name'),
                profile_data.get('age'),
                profile_data.get('gender'),
                profile_data.get('height'),
                profile_data.get('weight'),
                profile_data.get('goal_weight'),
                profile_data.get('goal'),
                profile_data.get('experience'),
                profile_data.get('activity_level'),
                profile_data.get('diet_preference'),
                profile_data.get('bmi'),
                profile_data.get('bmr'),
                profile_data.get('tdee'),
                profile_data.get('profile_complete', True)
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating profile: {e}")
            return False
    
    def get_profile(self, user_id: int) -> Optional[Dict]:
        """Get user profile."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def update_profile(self, user_id: int, profile_data: Dict) -> bool:
        """Update user profile."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE profiles SET
                    name = ?, age = ?, gender = ?, height = ?, weight = ?,
                    goal_weight = ?, goal = ?, experience = ?, activity_level = ?,
                    diet_preference = ?, bmi = ?, bmr = ?, tdee = ?,
                    profile_complete = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (
                profile_data.get('name'),
                profile_data.get('age'),
                profile_data.get('gender'),
                profile_data.get('height'),
                profile_data.get('weight'),
                profile_data.get('goal_weight'),
                profile_data.get('goal'),
                profile_data.get('experience'),
                profile_data.get('activity_level'),
                profile_data.get('diet_preference'),
                profile_data.get('bmi'),
                profile_data.get('bmr'),
                profile_data.get('tdee'),
                profile_data.get('profile_complete', True),
                user_id
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False
    
    # Progress operations
    def add_progress_entry(self, user_id: int, progress_data: Dict) -> bool:
        """Add progress entry."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO progress (
                    user_id, date, weight, body_fat, waist, chest, arms, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                progress_data.get('date'),
                progress_data.get('weight'),
                progress_data.get('body_fat'),
                progress_data.get('waist'),
                progress_data.get('chest'),
                progress_data.get('arms'),
                progress_data.get('notes')
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding progress: {e}")
            return False
    
    def get_progress_history(self, user_id: int) -> List[Dict]:
        """Get all progress entries for a user."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM progress 
            WHERE user_id = ? 
            ORDER BY date DESC
        """, (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_latest_progress(self, user_id: int) -> Optional[Dict]:
        """Get most recent progress entry."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM progress 
            WHERE user_id = ? 
            ORDER BY date DESC 
            LIMIT 1
        """, (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None


# Global database instance
db = Database()
