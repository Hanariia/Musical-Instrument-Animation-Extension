import json
import os
import subprocess
from dataclasses import dataclass
from math import floor
from typing import Tuple, List, Optional

from .estimated_hand_poses import EstimatedHandPoses, HandPose, HandType


HAND_POSES_DIRECTORY = "tmp/hand_poses"


@dataclass
class ImageStripData:
    """
    Data class for holding image strip data.
    If <end_frame> is None the image strip is the last strip
    of the reference video and should last till the video's end.
    """
    start_frame: int
    end_frame: Optional[int]
    filename: str
    hand_type: HandType


class HandPoseImageManager:
    def __init__(self, image_size: Tuple[int, int], hand_poses_filepath: str):
        self.image_size: Tuple[int, int] = image_size  # height, width
        self.estimated_hand_poses: EstimatedHandPoses = EstimatedHandPoses(filepath=hand_poses_filepath)
        if os.path.isdir(HAND_POSES_DIRECTORY):
            for file in os.listdir(HAND_POSES_DIRECTORY):
                os.remove(os.path.join(HAND_POSES_DIRECTORY, file))
        else:
            os.makedirs(HAND_POSES_DIRECTORY)

    def get_frames_image_strip_data(self, frame, fps, previous_frames_count, next_frames_count):
        # todo: implement adjacent frames processing, maybe use queue instead of list?
        image_strips = []
        timestamp = frame / fps
        for hand_type in [HandType.RIGHT, HandType.LEFT]:
            hand_poses_list = self.estimated_hand_poses.get_hand_pose_list(hand_type)
            hand_pose = self.estimated_hand_poses.find_hand_pose(timestamp, hand_type)
            if hand_pose.image_filename is None:
                strip = self.create_image_strip_data(hand_pose, hand_poses_list, fps)
                image_strips.append(strip)
        return image_strips

    def create_image_strip_data(self, hand_pose: HandPose, hand_poses_list: List[HandPose],
                                fps: float) -> ImageStripData:
        start_frame = int(floor(hand_pose.timestamp * fps))
        end_frame = None
        if hand_pose.index + 1 < len(hand_poses_list):
            end_frame = int(floor(hand_poses_list[hand_pose.index + 1].timestamp * fps))
        return ImageStripData(
            start_frame,
            end_frame,
            self.__get_image(hand_pose),
            hand_pose.hand_type)

    def __get_image(self, hand_pose: HandPose) -> str:
        if hand_pose.image_filename is None:
            filename = f"hand_pose{hand_pose.index}{hand_pose.hand_type.name}.png"
            subprocess.run(['python', "draw_handmarks.py",
                            os.path.join(HAND_POSES_DIRECTORY, filename),
                            str(self.image_size[0]),
                            str(self.image_size[1]),
                            json.dumps(hand_pose.normalized_positions)])
            hand_pose.image_filename = filename
        return hand_pose.image_filename
