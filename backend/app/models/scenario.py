from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    scenario_number = Column(Integer, nullable=False)  # 1-4
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    timeline = Column(String, nullable=True)
    key_assumptions = Column(Text, nullable=True)
    likelihood = Column(Float, nullable=True)  # 0.0 to 1.0
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    analysis = relationship("Analysis", back_populates="scenarios")
    strategies = relationship("Strategy", back_populates="scenario", cascade="all, delete-orphan")

