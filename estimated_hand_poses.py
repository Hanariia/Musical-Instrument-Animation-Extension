from bisect import bisect
from dataclasses import dataclass
from enum import Enum
import json
from typing import List, Dict, Optional


class HandType(Enum):
    RIGHT = 0
    LEFT = 1


@dataclass
class HandPose:
    """A data class for holding the hand pose data.
    The :image_filename: should be an empty string until the hand pose image is created.
    """
    index: int
    hand_type: HandType
    timestamp: float
    normalized_positions: List[Dict[str, float]]
    image_filename: str


class EstimatedHandPoses:
    """A class for deserializing, containing and accessing the estimated hand pose data."""
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
                ""
            ))
        return hand_poses_list

    def find_hand_pose(self, timestamp: float, hand_type: HandType) -> HandPose:
        """Returns a hand pose with the closest timestamp to the left of the given timestamp.
        :param timestamp: the timestamp to which the closest hand pose should be found.
        :param hand_type: the hand type (left/right) of the desired hand pose.
        """
        hand_poses_list = self.get_hand_pose_list(hand_type)
        index = bisect(hand_poses_list, timestamp, key=lambda pose: pose.timestamp)
        if index != 0:
            return hand_poses_list[index - 1]
        return hand_poses_list[0]

    def get_hand_pose_list(self, hand_type: HandType):
        """Returns the hand pose list for the given hand type."""
        return self.right_hand_poses if hand_type == HandType.RIGHT else self.left_hand_poses
