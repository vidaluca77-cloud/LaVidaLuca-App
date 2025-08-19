"""
Enhanced Pydantic models for LaVidaLuca Backend API.
This module provides comprehensive request/response models with examples,
validation, and OpenAPI documentation.
"""

from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum


# Enums for better type safety and documentation
class ActivityCategory(str, Enum):
    """Enumeration of available activity categories."""
    AGRICULTURE = "agriculture"
    TECHNOLOGY = "technology"
    ENVIRONMENT = "environment"
    BUSINESS = "business"
    COMMUNITY = "community"


class DifficultyLevel(str, Enum):
    """Enumeration of difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


# Base response models
class BaseResponse(BaseModel):
    """Base response model with common fields."""
    success: bool = Field(True, description="Whether the operation was successful")
    message: Optional[str] = Field(None, description="Optional response message")


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = Field(False, description="Always false for error responses")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "error": "Validation Error",
                "detail": "Email address is not valid"
            }
        }
    )


# User Models
class UserBase(BaseModel):
    """Base user model with common fields."""
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    full_name: Optional[str] = Field(None, max_length=100, description="User's full name")
    is_active: bool = Field(True, description="Whether the user account is active")


class UserCreate(UserBase):
    """Model for user registration."""
    password: str = Field(..., min_length=8, description="User password (minimum 8 characters)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john.doe@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "password": "securepassword123",
                "is_active": True
            }
        }
    )


class UserUpdate(BaseModel):
    """Model for user profile updates."""
    email: Optional[EmailStr] = Field(None, description="New email address")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="New username")
    full_name: Optional[str] = Field(None, max_length=100, description="New full name")
    is_active: Optional[bool] = Field(None, description="Account status")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "John Smith",
                "email": "john.smith@example.com"
            }
        }
    )


class User(UserBase):
    """Complete user model for responses."""
    id: int = Field(..., description="Unique user identifier")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "john.doe@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-20T14:45:00Z"
            }
        }
    )


class UserResponse(BaseResponse):
    """Response model for user operations."""
    user: User
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "User retrieved successfully",
                "user": {
                    "id": 1,
                    "email": "john.doe@example.com",
                    "username": "johndoe",
                    "full_name": "John Doe",
                    "is_active": True,
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-20T14:45:00Z"
                }
            }
        }
    )


# Authentication Models
class UserLogin(BaseModel):
    """Model for user login credentials."""
    username: str = Field(..., description="Username or email for login")
    password: str = Field(..., description="User password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "password": "securepassword123"
            }
        }
    )


class Token(BaseModel):
    """JWT token response model."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type (always 'bearer')")
    expires_in: Optional[int] = Field(None, description="Token expiration time in seconds")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }
    )


class TokenData(BaseModel):
    """Token data for internal use."""
    username: Optional[str] = None
    user_id: Optional[int] = None


# Activity Models
class ActivityBase(BaseModel):
    """Base activity model with common fields."""
    title: str = Field(..., min_length=3, max_length=200, description="Activity title")
    description: Optional[str] = Field(None, max_length=2000, description="Detailed activity description")
    category: ActivityCategory = Field(..., description="Activity category")
    difficulty_level: DifficultyLevel = Field(DifficultyLevel.BEGINNER, description="Difficulty level")
    duration_minutes: Optional[int] = Field(None, ge=1, le=600, description="Expected duration in minutes")
    location: Optional[str] = Field(None, max_length=200, description="Activity location")
    equipment_needed: Optional[str] = Field(None, max_length=500, description="Required equipment")
    learning_objectives: Optional[str] = Field(None, max_length=1000, description="Learning objectives")
    is_published: bool = Field(False, description="Whether the activity is published")


class ActivityCreate(ActivityBase):
    """Model for creating new activities."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Introduction to Sustainable Farming",
                "description": "Learn the basics of sustainable farming practices including crop rotation, organic fertilizers, and water conservation techniques.",
                "category": "agriculture",
                "difficulty_level": "beginner",
                "duration_minutes": 120,
                "location": "School Farm",
                "equipment_needed": "Notebook, pen, soil samples",
                "learning_objectives": "Understand sustainable farming principles, identify organic fertilizers, practice water conservation",
                "is_published": true
            }
        }
    )


class ActivityUpdate(BaseModel):
    """Model for updating existing activities."""
    title: Optional[str] = Field(None, min_length=3, max_length=200, description="New activity title")
    description: Optional[str] = Field(None, max_length=2000, description="New description")
    category: Optional[ActivityCategory] = Field(None, description="New category")
    difficulty_level: Optional[DifficultyLevel] = Field(None, description="New difficulty level")
    duration_minutes: Optional[int] = Field(None, ge=1, le=600, description="New duration in minutes")
    location: Optional[str] = Field(None, max_length=200, description="New location")
    equipment_needed: Optional[str] = Field(None, max_length=500, description="New equipment requirements")
    learning_objectives: Optional[str] = Field(None, max_length=1000, description="New learning objectives")
    is_published: Optional[bool] = Field(None, description="New publication status")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Advanced Sustainable Farming Techniques",
                "difficulty_level": "intermediate",
                "duration_minutes": 180,
                "is_published": true
            }
        }
    )


class Activity(ActivityBase):
    """Complete activity model for responses."""
    id: int = Field(..., description="Unique activity identifier")
    creator_id: int = Field(..., description="ID of the user who created this activity")
    created_at: datetime = Field(..., description="Activity creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Introduction to Sustainable Farming",
                "description": "Learn the basics of sustainable farming practices including crop rotation, organic fertilizers, and water conservation techniques.",
                "category": "agriculture",
                "difficulty_level": "beginner",
                "duration_minutes": 120,
                "location": "School Farm",
                "equipment_needed": "Notebook, pen, soil samples",
                "learning_objectives": "Understand sustainable farming principles, identify organic fertilizers, practice water conservation",
                "is_published": True,
                "creator_id": 1,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-20T14:45:00Z"
            }
        }
    )


class ActivityListResponse(BaseResponse):
    """Response model for activity lists."""
    activities: List[Activity] = Field(..., description="List of activities")
    total: int = Field(..., description="Total number of activities")
    skip: int = Field(..., description="Number of activities skipped")
    limit: int = Field(..., description="Maximum number of activities returned")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "activities": [
                    {
                        "id": 1,
                        "title": "Introduction to Sustainable Farming",
                        "description": "Learn the basics of sustainable farming practices...",
                        "category": "agriculture",
                        "difficulty_level": "beginner",
                        "duration_minutes": 120,
                        "location": "School Farm",
                        "equipment_needed": "Notebook, pen, soil samples",
                        "learning_objectives": "Understand sustainable farming principles...",
                        "is_published": True,
                        "creator_id": 1,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-20T14:45:00Z"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 100
            }
        }
    )


# Activity Suggestion Models
class ActivitySuggestionBase(BaseModel):
    """Base model for activity suggestions."""
    suggestion_reason: str = Field(..., description="Reason why this activity is suggested")
    ai_generated: bool = Field(True, description="Whether this suggestion was generated by AI")


class ActivitySuggestion(ActivitySuggestionBase):
    """Complete activity suggestion model."""
    id: int = Field(..., description="Unique suggestion identifier")
    user_id: int = Field(..., description="ID of the user receiving the suggestion")
    activity_id: int = Field(..., description="ID of the suggested activity")
    created_at: datetime = Field(..., description="Suggestion creation timestamp")
    activity: Activity = Field(..., description="Complete activity information")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "activity_id": 2,
                "suggestion_reason": "Based on your interest in agriculture and beginner skill level",
                "ai_generated": True,
                "created_at": "2024-01-20T10:30:00Z",
                "activity": {
                    "id": 2,
                    "title": "Organic Composting Basics",
                    "description": "Learn how to create nutrient-rich compost...",
                    "category": "agriculture",
                    "difficulty_level": "beginner",
                    "duration_minutes": 90,
                    "location": "Garden",
                    "equipment_needed": "Gloves, shovel, organic waste",
                    "learning_objectives": "Understand composting process...",
                    "is_published": True,
                    "creator_id": 2,
                    "created_at": "2024-01-18T10:30:00Z",
                    "updated_at": None
                }
            }
        }
    )


class SuggestionRequest(BaseModel):
    """Model for requesting AI-generated suggestions."""
    preferences: Optional[str] = Field(None, max_length=500, description="User preferences and interests")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "preferences": "I'm interested in sustainable farming and environmental conservation. I prefer hands-on activities."
            }
        }
    )


class SuggestionListResponse(BaseResponse):
    """Response model for suggestion lists."""
    suggestions: List[ActivitySuggestion] = Field(..., description="List of activity suggestions")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Suggestions generated successfully",
                "suggestions": [
                    {
                        "id": 1,
                        "user_id": 1,
                        "activity_id": 2,
                        "suggestion_reason": "Based on your interest in agriculture and beginner skill level",
                        "ai_generated": True,
                        "created_at": "2024-01-20T10:30:00Z",
                        "activity": {
                            "id": 2,
                            "title": "Organic Composting Basics",
                            "description": "Learn how to create nutrient-rich compost...",
                            "category": "agriculture",
                            "difficulty_level": "beginner",
                            "duration_minutes": 90,
                            "location": "Garden",
                            "equipment_needed": "Gloves, shovel, organic waste",
                            "learning_objectives": "Understand composting process...",
                            "is_published": True,
                            "creator_id": 2,
                            "created_at": "2024-01-18T10:30:00Z",
                            "updated_at": None
                        }
                    }
                ]
            }
        }
    )


# Generic response models
class MessageResponse(BaseResponse):
    """Simple message response model."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Operation completed successfully"
            }
        }
    )


class CategoryListResponse(BaseResponse):
    """Response model for activity categories."""
    categories: List[str] = Field(..., description="List of available activity categories")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "categories": ["agriculture", "technology", "environment", "business", "community"]
            }
        }
    )