import uuid
from datetime import datetime, date
from sqlalchemy import String, UUID, Boolean, Numeric, Text, DateTime, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255))
    price_per_night_bdt: Mapped[float] = mapped_column(Numeric(10, 2))
    max_guests: Mapped[int] = mapped_column()
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("listings.id"))
    guest_name: Mapped[str] = mapped_column(String(255))
    check_in: Mapped[date] = mapped_column(Date)
    check_out: Mapped[date] = mapped_column(Date)
    total_price: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String(50), default="confirmed")

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[str] = mapped_column(String(255), index=True)
    role: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
