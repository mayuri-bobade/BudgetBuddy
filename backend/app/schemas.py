from pydantic import BaseModel, EmailStr, field_validator, model_validator
from datetime import date, datetime
from typing import Optional, List
from .models import ExpenseCategory, IncomeCategory


# ─── User Schemas ────────────────────────────────────────────
class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str = ""
    last_name: str = ""


class UserResponse(UserBase):
    id: int
    role: str
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Profile Schemas ─────────────────────────────────────────
class ProfileResponse(BaseModel):
    id: int
    user: UserResponse
    monthly_income: float
    currency: str
    budget_alerts: bool
    savings_reminders: bool
    monthly_report_notifications: bool

    model_config = {"from_attributes": True}


# ─── Registration ────────────────────────────────────────────
class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str
    first_name: str = ""
    last_name: str = ""

    @field_validator("username")
    @classmethod
    def username_min_length(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return v

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    @model_validator(mode="after")
    def passwords_match(self) -> "RegisterRequest":
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self


class RegisterResponse(BaseModel):
    user: UserResponse
    tokens: dict


# ─── Login ───────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access: str
    refresh: str
    user: UserResponse


# ─── Token Refresh ───────────────────────────────────────────
class TokenRefreshRequest(BaseModel):
    refresh: str


class TokenRefreshResponse(BaseModel):
    access: str
    refresh: Optional[str] = None


# ─── Logout ──────────────────────────────────────────────────
class LogoutRequest(BaseModel):
    refresh: str


# ─── Check Auth ──────────────────────────────────────────────
class CheckAuthResponse(BaseModel):
    authenticated: bool
    user: UserResponse


# ─── Expense Schemas ───────────────────────────────────────
class ExpenseCreate(BaseModel):
    amount: float
    category: ExpenseCategory
    description: str = ""
    date: date

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[ExpenseCategory] = None
    description: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v


class ExpenseResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    category: ExpenseCategory
    description: str
    date: date
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ExpenseListResponse(BaseModel):
    expenses: List[ExpenseResponse]
    total: int


# ─── Income Schemas ───────────────────────────────────────
class IncomeCreate(BaseModel):
    amount: float
    source: IncomeCategory
    description: str = ""
    date: date

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v


class IncomeUpdate(BaseModel):
    amount: Optional[float] = None
    source: Optional[IncomeCategory] = None
    description: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v


class IncomeResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    source: IncomeCategory
    description: str
    date: date
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class IncomeListResponse(BaseModel):
    incomes: List[IncomeResponse]
    total: int


# ─── Transaction Schemas ──────────────────────────────────
class TransactionItem(BaseModel):
    id: int
    type: str  # "income" or "expense"
    amount: float
    category: str
    description: str
    date: date
    created_at: datetime

    model_config = {"from_attributes": True}


class TransactionSummary(BaseModel):
    total_income: float
    total_expenses: float
    balance: float
    income_count: int
    expense_count: int


class TransactionListResponse(BaseModel):
    transactions: List[TransactionItem]
    total: int


# ─── Budget Schemas ────────────────────────────────────────
class AllocationInput(BaseModel):
    category: ExpenseCategory
    amount: float

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v


class AllocationResponse(BaseModel):
    id: int
    category: ExpenseCategory
    amount: float

    model_config = {"from_attributes": True}


class BudgetCreate(BaseModel):
    month: int
    year: int
    total_amount: float
    allocations: List[AllocationInput]

    @field_validator("month")
    @classmethod
    def month_valid(cls, v: int) -> int:
        if v < 1 or v > 12:
            raise ValueError("Month must be between 1 and 12")
        return v

    @field_validator("total_amount")
    @classmethod
    def total_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Total amount must be greater than 0")
        return v


class BudgetUpdate(BaseModel):
    total_amount: Optional[float] = None
    allocations: Optional[List[AllocationInput]] = None

    @field_validator("total_amount")
    @classmethod
    def total_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Total amount must be greater than 0")
        return v


class BudgetResponse(BaseModel):
    id: int
    user_id: int
    month: int
    year: int
    total_amount: float
    allocations: List[AllocationResponse]
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class BudgetListResponse(BaseModel):
    budgets: List[BudgetResponse]
    total: int


# ─── Savings Goal Schemas ────────────────────────────────────
class SavingsGoalCreate(BaseModel):
    name: str
    target_amount: float

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Goal name cannot be empty")
        return v.strip()

    @field_validator("target_amount")
    @classmethod
    def target_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Target amount must be greater than 0")
        return v


class SavingsGoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Goal name cannot be empty")
        return v.strip() if v else v

    @field_validator("target_amount")
    @classmethod
    def target_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Target amount must be greater than 0")
        return v


class SavingsGoalProgressUpdate(BaseModel):
    current_saved: float

    @field_validator("current_saved")
    @classmethod
    def saved_not_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Saved amount cannot be negative")
        return v


class SavingsGoalResponse(BaseModel):
    id: int
    user_id: int
    name: str
    target_amount: float
    current_saved: float
    progress_percent: float
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class SavingsGoalListResponse(BaseModel):
    goals: List[SavingsGoalResponse]
    total: int
