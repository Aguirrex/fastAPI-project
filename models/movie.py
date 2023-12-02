from config.database import Base
from sqlalchemy import Colum, Integer, String, Float

class Movie(Base):
    __tablename__ = "movies"

    id = Colum(Integer,primary_key=True,index=True)
    title = Colum(String)
    overview  = Colum(String)
    year = Colum()
    rating = Colum()
    category = Colum()