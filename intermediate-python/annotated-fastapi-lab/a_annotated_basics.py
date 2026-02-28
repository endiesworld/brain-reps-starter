from typing import Annotated, get_type_hints, get_origin, get_args

UserId = Annotated[int, "primary key", {"source": "db"}]

def f(user_id: UserId) -> None:
    pass

print("Raw __annotations__:", f.__annotations__)
print("\nget_type_hints (default):", get_type_hints(f))
print("get_type_hints (include_extras=True):", get_type_hints(f, include_extras=True))

ann = get_type_hints(f, include_extras=True)["user_id"]
print("\nOrigin:", get_origin(ann))
print("Args:", get_args(ann))

base_type, *metadata = get_args(ann)
print("\nBase type:", base_type)
print("Metadata:", metadata)