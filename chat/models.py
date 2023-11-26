import datetime
import ormar
from
from pydantic import condecimal typing import Optional, List, Union, Dict
from db import MainMata


class User(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    username: str = ormar.String()
    password: str = ormar.String()
    name: str = ormar.String()


    def __str__(self):
        return f'{self.name}'