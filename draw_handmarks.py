from enum import Enum

try:
    import sys
    from json import JSONDecodeError
    from typing import List, Dict, Tuple
    from PIL import Image, ImageDraw, ImageColor
    import json
except ImportError as e:
    raise Exception(f"{e.msg}. Please install the missing packages: python -m pip install <missing_package>")

CIRCLE_RADIUS = 4


def create_hand_pose_image(image_height: int, image_width: int, normalized_positions: List[Dict[str, float]],
                           filepath: str):
    image = Image.new("RGB", (image_width, image_height), color="black")
    draw = ImageDraw.Draw(image)

    # draw connection lines
    for group in LandmarkGroup:
        color = tuple([int(c * 0.6) for c in group.group_color])
        connections = [(normalized_positions[i]["x"] * image_width, normalized_positions[i]["y"] * image_height)
                       for i in LandmarkConnections.get_group_connections(group)]
        draw.line(connections, fill=color, width=3)

    # draw joint points
    for i, landmark in enumerate(normalized_positions):
        draw.circle((landmark["x"] * image_width, landmark["y"] * image_height),
                    CIRCLE_RADIUS, fill=HandLandmarks(i).group.group_color)

    # save image
    if filepath[-4:] != ".png":
        filepath += ".png"
    image.save(filepath, compress_level=0, transparency=(0, 0, 0))


class LandmarkGroup(Enum):
    WRIST = 0, ImageColor.getrgb("Sienna")
    THUMB = 1, ImageColor.getrgb("SkyBlue")
    INDEX_FINGER = 2, ImageColor.getrgb("LightGreen")
    MIDDLE_FINGER = 3, ImageColor.getrgb("Khaki")
    RING_FINGER = 4, ImageColor.getrgb("LightCoral")
    PINKY = 5, ImageColor.getrgb("MidnightBlue")

    def __init__(self, group_id: int, color: Tuple[int, int, int]):
        self.group_id = group_id
        self.color = color

    @property
    def group_color(self) -> Tuple[int, int, int]:
        return self.color


class HandLandmarks(Enum):
    WRIST = 0
    THUMB_0 = 1
    THUMB_1 = 2
    THUMB_2 = 3
    THUMB_3 = 4
    INDEX_FINGER_0 = 5
    INDEX_FINGER_1 = 6
    INDEX_FINGER_2 = 7
    INDEX_FINGER_3 = 8
    MIDDLE_FINGER_0 = 9
    MIDDLE_FINGER_1 = 10
    MIDDLE_FINGER_2 = 11
    MIDDLE_FINGER_3 = 12
    RING_FINGER_0 = 13
    RING_FINGER_1 = 14
    RING_FINGER_2 = 15
    RING_FINGER_3 = 16
    PINKY_0 = 17
    PINKY_1 = 18
    PINKY_2 = 19
    PINKY_3 = 20

    @property
    def group(self) -> LandmarkGroup:
        if self.name[-1] == "0" or self.name == "WRIST":
            return LandmarkGroup.WRIST
        return LandmarkGroup[self.name[:-2]]


class LandmarkConnections(Enum):
    WRIST_CONNECTIONS = [0, 1, 5, 9, 13, 17, 0]
    THUMB_CONNECTIONS = [1, 2, 3, 4]
    INDEX_FINGER_CONNECTIONS = [5, 6, 7, 8]
    MIDDLE_FINGER_CONNECTIONS = [9, 10, 11, 12]
    RING_FINGER_CONNECTIONS = [13, 14, 15, 16]
    PINKY_CONNECTIONS = [17, 18, 19, 20]

    @classmethod
    def get_group_connections(cls, group: LandmarkGroup) -> List[int]:
        return cls[group.name + "_CONNECTIONS"].value
