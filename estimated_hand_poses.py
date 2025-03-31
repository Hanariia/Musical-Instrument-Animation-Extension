from bisect import bisect_left
from enum import Enum
import json
from typing import List, Dict, Optional


class HandType(Enum):
    RIGHT = 0
    LEFT = 1


class HandPose:
    def __init__(self, index: int, hand_type: HandType, timestamp: float,
                 normalized_positions: List[Dict[str, float]]):
        self.index: int = index
        self.hand_type: HandType = hand_type
        self.timestamp: float = timestamp
        self.image_filename: Optional[str] = None
        self.normalized_positions: List[Dict[str, float]] = normalized_positions


class EstimatedHandPoses:
    def __init__(self, filepath):
        self.left_hand_poses: List[HandPose] = []
        self.right_hand_poses: List[HandPose] = []

        with open(filepath, "r") as hand_data_file:
            hand_data = json.load(hand_data_file)

            # process up to 1 hand of each type
            for hand in hand_data:
                if hand["type"] == "Right" and not self.right_hand_poses:
                    self.right_hand_poses = self.__create_hand_poses_list(hand['type'], hand['animationData'])
                elif hand["type"] == "Left" and not self.left_hand_poses:
                    self.left_hand_poses = self.__create_hand_poses_list(hand['type'], hand['animationData'])
                if self.right_hand_poses and self.left_hand_poses:
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
