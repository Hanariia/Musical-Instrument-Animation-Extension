from bisect import bisect_left
from enum import Enum
import json
from typing import List, Dict


class HandType(Enum):
    RIGHT = 0
    LEFT = 1


class HandPose:
    index: int
    hand_type: HandType
    timestamp: float
    image_filename: str
    normalized_positions: List[Dict[str, float]]
    world_positions: List[Dict[str, float]]

    def __init__(self, index: int, hand_type: HandType, timestamp: float,
                 normalized_positions: List[Dict[str, float]], world_positions: List[Dict[str, float]]):
        self.index = index
        self.hand_type = hand_type
        self.timestamp = timestamp
        self.normalized_positions = normalized_positions
        self.world_positions = world_positions  # maybe useful to view for the user?


class EstimatedHandPoses:
    left_hand_poses: List[HandPose]
    right_hand_poses: List[HandPose]

    def __init__(self, filepath):
        with open(filepath, "r") as hand_data_file:
            hand_data = json.load(hand_data_file)

            # process up to 1 hand of each type
            for hand in hand_data:
                if hand["type"] == "Right" and self.right_hand_poses is None:
                    self.right_hand_poses = self.__create_hand_poses_list(hand['type'], hand['animationData'])
                elif hand["type"] == "Left" and self.left_hand_poses is None:
                    self.left_hand_poses = self.__create_hand_poses_list(hand['type'], hand['animationData'])
                if self.right_hand_poses is not None and self.left_hand_poses is not None:
                    break

    @staticmethod
    def __create_hand_poses_list(hand_type: str, animation_data) -> List[HandPose]:
        hand_poses_list: List[HandPose] = []
        for i, hand_pose in enumerate(animation_data):
            hand_poses_list.append(HandPose(
                i,
                HandType[hand_type.upper()],
                hand_pose['timestamp'],
                hand_pose['normalizedPositions'],
                hand_pose['worldPositions']
            ))
        return hand_poses_list

    def find_hand_pose(self, timestamp, hand_type: HandType):
        hand_poses_list = self.get_hand_pose_list(hand_type)
        index = bisect_left(hand_poses_list, timestamp, key=lambda pose: pose.timestamp)
        if index != 0:
            return hand_poses_list[index - 1]
        return hand_poses_list[0]

    def get_hand_pose_list(self, hand_type: HandType):
        return self.right_hand_poses if hand_type == HandType.RIGHT else self.left_hand_poses
