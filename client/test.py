from static import *
from enum import Enum
# from pydantic import BaseModel
# dict_test = {
#         COST: {
#             STONE: 100,
#         },
#         PLACE: '.',
#         TYPE: DYNAMIC,
#         NAME: WHEAT_FIELD,
#         RESOURCES_CREATE: {
#             WHEAT: 2,
#         },
#         RESOURCES_USE: None,
#         MAX_WORKERS: 3,
#         IMAGE: (416, 0)
# }

# class DictToClass(BaseModel):
#     cost: dict
#     place: str
#         # for key in my_dict:
#         #     setattr(self, key, my_dict[key])

# if __name__ == '__main__':
#     d = DictToClass(**dict_test)
#     print(d.place)

# class MyEnum(Enum):
#     COST = 'cost'


# print(COST == MyEnum.COST.value)