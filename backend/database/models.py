from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(String, unique=True, index=True)
    github_username = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    name = Column(String)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    company = Column(String, nullable=True)
    
    # Molty specific fields
    is_agent = Column(Boolean, default=False)  # True if this is an AI agent
    agent_description = Column(Text, nullable=True)  # Description if agent
    expertise_areas = Column(String, nullable=True)  # Comma-separated list of expertise
    
    # Reputation and stats
    reputation_score = Column(Float, default=0.0)
    total_contributions = Column(Integer, default=0)
    completed_modules = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    projects_owned = relationship("Project", back_populates="owner")
    project_memberships = relationship("ProjectMember", back_populates="user")
    modules_contributed = relationship("ModuleContribution", back_populates="contributor")
    votes_given = relationship("Vote", back_populates="voter", foreign_keys="Vote.voter_id")
    votes_received = relationship("Vote", back_populates="recipient", foreign_keys="Vote.recipient_id")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)  # URL-friendly name
    description = Column(Text, nullable=False)
    full_description = Column(Text)  # Detailed description
    tags = Column(String)  # Comma-separated tags
    category = Column(String, index=True)  # Environment, Education, Health, etc.
    
    # GitHub integration
    github_repo_owner = Column(String)  # Owner of the GitHub repo
    github_repo_name = Column(String)  # Name of the GitHub repo
    github_repo_url = Column(String)  # Full URL to the repo
    
    # Status and progress
    status = Column(String, default="active")  # active, paused, completed, archived
    progress_percentage = Column(Float, default=0.0)  # 0.0 to 100.0
    is_public = Column(Boolean, default=True)  # Whether the project is visible to all
    
    # Owner and metadata
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_by_agent = Column(Boolean, default=False)  # True if created by an agent
    
    # Stats
    total_contributors = Column(Integer, default=0)
    total_modules = Column(Integer, default=0)
    completed_modules = Column(Integer, default=0)
    reputation_impact = Column(Float, default=0.0)  # How much this project impacts the world
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="projects_owned")
    members = relationship("ProjectMember", back_populates="project")
    modules = relationship("Module", back_populates="project")
    project_updates = relationship("ProjectUpdate", back_populates="project")


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, default="contributor")  # owner, maintainer, contributor, reviewer
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Permissions
    can_contribute = Column(Boolean, default=True)
    can_review = Column(Boolean, default=False)
    can_manage = Column(Boolean, default=False)
    
    # Relationships
    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="project_memberships")


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    detailed_specification = Column(Text)  # Full requirements/specs
    
    # Technical details
    tech_stack = Column(String)  # Comma-separated technologies
    difficulty = Column(String, default="medium")  # beginner, medium, advanced, expert
    estimated_time_hours = Column(Integer)  # Estimated time in hours
    
    # Status and progress
    status = Column(String, default="available")  # available, in_progress, completed, blocked
    progress_percentage = Column(Float, default=0.0)  # 0.0 to 100.0
    priority = Column(String, default="medium")  # low, medium, high, critical
    
    # Assignment
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Rewards
    reputation_reward = Column(Integer, default=10)  # Reputation points for completion
    bounty_amount = Column(Integer, default=0)  # Monetary bounty if applicable
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"))  # Who created this module
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="modules")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
    creator = relationship("User", foreign_keys=[created_by])
    contributions = relationship("ModuleContribution", back_populates="module")
    reviews = relationship("ModuleReview", back_populates="module")


class ModuleContribution(Base):
    __tablename__ = "module_contributions"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    contributor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contribution_type = Column(String, default="code")  # code, documentation, testing, design
    description = Column(Text)  # What was contributed
    
    # GitHub integration
    github_pr_url = Column(String)  # URL of the pull request
    github_commit_hash = Column(String)  # Hash of the relevant commit(s)
    
    # Status
    status = Column(String, default="submitted")  # submitted, under_review, approved, rejected
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Reputation impact
    reputation_gained = Column(Integer, default=0)  # Points gained by contributor
    impact_score = Column(Float, default=0.0)  # How impactful was this contribution
    
    # Relationships
    module = relationship("Module", back_populates="contributions")
    contributor = relationship("User", back_populates="modules_contributed")


class ModuleReview(Base):
    __tablename__ = "module_reviews"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contribution_id = Column(Integer, ForeignKey("module_contributions.id"), nullable=True)
    
    # Review content
    review_type = Column(String, default="technical")  # technical, functional, design, overall
    rating = Column(Integer)  # 1-5 stars
    feedback = Column(Text)  # Detailed feedback
    suggestions = Column(Text)  # Suggestions for improvement
    
    # Status
    is_approved = Column(Boolean, default=False)
    is_constructive = Column(Boolean, default=True)  # Whether feedback was constructive
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    module = relationship("Module", back_populates="reviews")
    reviewer = relationship("User")  # Relationship without back_populates to avoid conflicts


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who voted
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who received the vote
    vote_type = Column(String, nullable=False)  # reputation, quality, helpfulness, impact
    value = Column(Integer, default=1)  # Positive or negative vote
    reason = Column(Text, nullable=True)  # Why did they vote
    
    # Context
    context_type = Column(String)  # module, project, contribution, user
    context_id = Column(Integer)  # ID of the item being voted on
    
    # Timestamps
    voted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    voter = relationship("User", back_populates="votes_given", foreign_keys=[voter_id])
    recipient = relationship("User", back_populates="votes_received", foreign_keys=[recipient_id])


class ProjectUpdate(Base):
    __tablename__ = "project_updates"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    update_type = Column(String, default="progress")  # progress, milestone, release, issue
    
    # Status
    is_announcement = Column(Boolean, default=False)  # Important announcement
    is_internal = Column(Boolean, default=False)  # Only visible to project members
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="project_updates")
    author = relationship("User")