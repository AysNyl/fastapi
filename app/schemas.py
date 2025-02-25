from pydantic import BaseModel

class BasePost(BaseModel):
    title: str
    content: str
    # published: Optional[bool] = True, tried to supply a null value
    # Python lets you write optional type hints 
    # where you can return either a specified type or None
    # to a column with not null constraint but with Default constraint
    # got an error, Explaination (stackoverflow):
    # DEFAULT is used if no value is passed and only on INSERT. 
    # NULL is a value, an unknown one but a value, 
    # so DEFAULT is not invoked and you trip the NOT NULL constraint. 
    # To get this to work just don't supply a value for the field.
    # conclusion: default is implicit
    published: bool = True


