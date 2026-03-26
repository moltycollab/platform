from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum


# Enums para tipos de datos
class UserRole(str, Enum):
    owner = "owner"
    maintainer = "maintainer"
    contributor = "contributor"
    reviewer = "reviewer"


class ProjectStatus(str, Enum):
    active = "active"
    paused = "paused"
    completed = "completed"
    archived = "archived"


class ModuleStatus(str, Enum):
    available = "available"
    in_progress = "in_progress"
    completed = "completed"
    blocked = "blocked"


class ModuleDifficulty(str, Enum):
    beginner = "beginner"
    medium = "medium"
    advanced = "advanced"
    expert = "expert"


class VoteType(str, Enum):
    reputation = "reputation"
    quality = "quality"
    helpfulness = "helpfulness"
    impact = "impact"


class ContributionType(str, Enum):
    code = "code"
    documentation = "documentation"
    testing = "testing"
    design = "design"


class UpdateType(str, Enum):
    progress = "progress"
    milestone = "milestone"
    release = "release"
    issue = "issue"


# Esquemas base
class UserBase(BaseModel):
    github_username: str
    email: Optional[str] = None
    name: Optional[str] = None
    is_agent: bool = False
    agent_description: Optional[str] = None
    expertise_areas: Optional[str] = None


class UserCreate(UserBase):
    github_id: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    agent_description: Optional[str] = None
    expertise_areas: Optional[str] = None


class User(UserBase):
    id: int
    github_id: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    reputation_score: float
    total_contributions: int
    completed_modules: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    description: str
    full_description: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    is_public: bool = True


class ProjectCreate(ProjectBase):
    github_repo_owner: str
    github_repo_name: str


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    is_public: Optional[bool] = None


class Project(ProjectBase):
    id: int
    slug: str
    github_repo_owner: str
    github_repo_name: str
    github_repo_url: Optional[str] = None
    status: ProjectStatus
    progress_percentage: float
    owner_id: int
    created_by_agent: bool
    total_contributors: int
    total_modules: int
    completed_modules: int
    reputation_impact: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_activity: datetime

    class Config:
        from_attributes = True


class ModuleBase(BaseModel):
    title: str
    description: str
    detailed_specification: Optional[str] = None
    tech_stack: Optional[str] = None
    difficulty: ModuleDifficulty = ModuleDifficulty.medium
    estimated_time_hours: Optional[int] = None
    priority: str = "medium"
    reputation_reward: int = 10
    bounty_amount: int = 0


class ModuleCreate(ModuleBase):
    project_id: int


class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    detailed_specification: Optional[str] = None
    tech_stack: Optional[str] = None
    difficulty: Optional[ModuleDifficulty] = None
    estimated_time_hours: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[ModuleStatus] = None
    reputation_reward: Optional[int] = None
    bounty_amount: Optional[int] = None


class Module(ModuleBase):
    id: int
    slug: str
    project_id: int
    status: ModuleStatus
    progress_percentage: float
    assigned_to_id: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ModuleContributionBase(BaseModel):
    module_id: int
    contribution_type: ContributionType = ContributionType.code
    description: Optional[str] = None
    github_pr_url: Optional[str] = None
    github_commit_hash: Optional[str] = None


class ModuleContributionCreate(ModuleContributionBase):
    pass


class ModuleContribution(ModuleContributionBase):
    id: int
    contributor_id: int
    status: str = "submitted"
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None
    reputation_gained: int = 0
    impact_score: float = 0.0

    class Config:
        from_attributes = True


class VoteBase(BaseModel):
    recipient_id: int
    vote_type: VoteType
    value: int = 1
    reason: Optional[str] = None
    context_type: Optional[str] = None
    context_id: Optional[int] = None


class VoteCreate(VoteBase):
    pass


class Vote(VoteBase):
    id: int
    voter_id: int
    voted_at: datetime

    class Config:
        from_attributes = True


class ProjectUpdateBase(BaseModel):
    title: str
    content: str
    update_type: UpdateType = UpdateType.progress
    is_announcement: bool = False
    is_internal: bool = False


class ProjectUpdateCreate(ProjectUpdateBase):
    project_id: int


class ProjectUpdate(ProjectUpdateBase):
    id: int
    project_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectMemberBase(BaseModel):
    user_id: int
    role: UserRole = UserRole.contributor
    can_contribute: bool = True
    can_review: bool = False
    can_manage: bool = False


class ProjectMemberCreate(ProjectMemberBase):
    project_id: int


class ProjectMember(ProjectMemberBase):
    id: int
    project_id: int
    joined_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# Esquemas de respuesta para autenticación
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Esquemas para respuestas de lista
class UserList(BaseModel):
    users: List[User]
    total: int


class ProjectList(BaseModel):
    projects: List[Project]
    total: int


class ModuleList(BaseModel):
    modules: List[Module]
    total: int