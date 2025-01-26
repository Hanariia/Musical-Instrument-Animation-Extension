from bisect import bisect_left
from enum import Enum
import json
from typing import List, Dict


class EstimatedHandPoses:
    left_hand_data = None
    right_hand_data = None

    def __init__(self, filepath):
        with open(filepath, "r") as hand_data_file:
            hand_data = json.load(hand_data_file)

            # process up to 1 hand of each type
            for hand in hand_data:
                if hand["type"] == "Right" and self.right_hand_data is None:
                    self.right_hand_data = HandData(hand['type'], hand['animationData'])
                elif hand["type"] == "Left" and self.left_hand_data is None:
                    self.left_hand_data = HandData(hand['type'], hand['animationData'])
                if self.right_hand_data is not None and self.left_hand_data is not None:
                    break


class HandType(Enum):
    RIGHT = 0
    LEFT = 1


class HandPose:
    timestamp = None
    image_filename: str = None
    normalized_positions: List[Dict[str, float]] = None
    world_positions: List[Dict[str, float]] = None

    def __init__(self, timestamp, normalized_positions, world_positions):
        self.timestamp = timestamp
        self.normalized_positions = normalized_positions
        self.world_positions = world_positions  # maybe useful to view for the user?


class HandData:
    hand_type: HandType = None
    hand_poses_list: List[HandPose] = []

    def __init__(self, hand_type: str, animation_data):
        self.hand_type = HandType[hand_type.upper()]
        for hand_pose in animation_data:
            self.hand_poses_list.append(HandPose(
                hand_pose['timestamp'],
                hand_pose['normalizedPositions'],
                hand_pose['worldPositions']
            ))

    def find_hand_pose(self, timestamp):
        index = bisect_left(self.hand_poses_list, timestamp, key=lambda pose: pose.timestamp)
        if index != 0:
            return self.hand_poses_list[index - 1]
        return self.hand_poses_list[0]
