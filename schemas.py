"""
Database Schemas for AI Founder Command Console

Each Pydantic model corresponds to a MongoDB collection whose name is the lowercase of the class name.
These schemas validate incoming data to the generic CRUD endpoints.
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, HttpUrl
from datetime import date

# Shared enums/aliases
ServiceType = Literal[
    "AI Engine",
    "Prompt",
    "Creative",
    "Audit",
    "Persona",
    "Subscription",
    "Business Ops"
]

StatusType = Literal[
    "Discovery",
    "Scoping",
    "In Progress",
    "In Review",
    "Deliverables Drafted",
    "Awaiting Feedback",
    "Done",
    "Blocked"
]

PriorityType = Literal["Low", "Medium", "High", "Critical"]

class Client(BaseModel):
    name: str = Field(..., description="Client or brand name")
    contact: Optional[str] = Field(None, description="Primary contact name/email")
    services: List[ServiceType] = Field(default_factory=list)
    status: Optional[StatusType] = Field("Discovery")
    next_action: Optional[str] = None
    notes: Optional[str] = None

class Project(BaseModel):
    client_id: Optional[str] = Field(None, description="Reference to client")
    title: str
    service_type: ServiceType
    status: StatusType = "Discovery"
    due_date: Optional[date] = None
    checklist: List[str] = Field(default_factory=list)

class Task(BaseModel):
    title: str
    service_tag: ServiceType
    priority: PriorityType = "Medium"
    due_date: Optional[date] = None
    notes: Optional[str] = None
    client_id: Optional[str] = None
    project_id: Optional[str] = None
    done: bool = False

class Prompt(BaseModel):
    name: str
    target_model: Literal["Internal", "External"] = "External"
    use_case: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    text: str
    variants: List[str] = Field(default_factory=list)
    notes: Optional[str] = None

class PromptSet(BaseModel):
    title: str
    client_id: Optional[str] = None
    service_type: Optional[ServiceType] = None
    prompt_ids: List[str] = Field(default_factory=list)

class EngineBlueprint(BaseModel):
    name: str
    flavor: Literal["Off-the-shelf", "Custom-tailored"]
    purpose: str
    domain: Optional[str] = None
    knowledge_sources: List[str] = Field(default_factory=list)
    persona: Optional[str] = None
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    guardrails: List[str] = Field(default_factory=list)
    client_id: Optional[str] = None

class CreativeBrief(BaseModel):
    project_id: Optional[str] = None
    platforms: List[str] = Field(default_factory=list)
    audience: Optional[str] = None
    goal: Optional[str] = None
    tone_style: Optional[str] = None
    deliverables: List[str] = Field(default_factory=list)
    formats: List[str] = Field(default_factory=list)
    timeline: List[str] = Field(default_factory=list)

class ContentCalendarItem(BaseModel):
    project_id: Optional[str] = None
    title: str
    publish_date: date
    channel: Optional[str] = None

class WorkflowAudit(BaseModel):
    client_id: Optional[str] = None
    tools: List[str] = Field(default_factory=list)
    steps: List[str] = Field(default_factory=list)
    triggers: List[str] = Field(default_factory=list)
    pain_points: List[str] = Field(default_factory=list)
    optimizations: List[str] = Field(default_factory=list)
    report_summary: Optional[str] = None

class PersonaKit(BaseModel):
    client_id: Optional[str] = None
    mission: Optional[str] = None
    values: List[str] = Field(default_factory=list)
    audience: Optional[str] = None
    slogans: List[str] = Field(default_factory=list)
    references: List[HttpUrl] = Field(default_factory=list)
    tone_axes: dict = Field(default_factory=dict)
    how_sound: Optional[str] = None
    how_never_sound: Optional[str] = None
    lexicon_prefer: List[str] = Field(default_factory=list)
    lexicon_avoid: List[str] = Field(default_factory=list)

class SubscriptionTierPlan(BaseModel):
    name: Literal["Entry", "Growth", "Pro"]
    prompt_pack_volume: str
    toolkit_access: List[str] = Field(default_factory=list)
    integration_resources: List[str] = Field(default_factory=list)
    model_library_access: str
    support_components: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
