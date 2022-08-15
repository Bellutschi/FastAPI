from database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship

# Base ist die Klasse aus der die Struktur metadata.tables geerbt werden
class Post(Base):
    # model (class) attributes
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Foreign key zur users ID aus der anderen Tabelle
    # CASCADE bedeutet, das alle Posts bei löschen des Users entfernt werden
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # zieht sich alle Informationen auf Basis der Beziehung zur Tabelle Users
    owner = relationship("User")



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
