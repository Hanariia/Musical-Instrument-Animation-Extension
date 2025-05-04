import os
from dataclasses import dataclass
from typing import Tuple, List, Optional
import bpy

from .draw_handmarks import create_hand_pose_image
from .miae_utils import get_abs_addon_dir
from .estimated_hand_poses import EstimatedHandPoses, HandPose, HandType


HAND_POSES_DIRECTORY = os.path.join(get_abs_addon_dir(), "tmp/hand_poses")
MAX_IMAGE_STRIP_LENGTH_SECS = 2


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
        image_strips = []
        timestamp = frame / fps
        for hand_type in [HandType.RIGHT, HandType.LEFT]:
            hand_pose = self.estimated_hand_poses.find_hand_pose(timestamp, hand_type)
            adjacent_poses = self.__get_adjacent_poses(hand_pose, previous_frames_count, next_frames_count)
            strips = self.__get_hand_poses_image_strip_data(adjacent_poses, fps)
            image_strips.extend(strips)
        return image_strips

    def __get_hand_poses_image_strip_data(self, adjacent_poses, fps):
        image_strips = []
        for adj_pose in adjacent_poses:
            if adj_pose.image_filename is None:
                self.__create_image(adj_pose)
                strip = self.__create_image_strip_data(adj_pose, fps)
                image_strips.append(strip)
        return image_strips

    def __get_adjacent_poses(self, hand_pose: HandPose, previous_frames_count, next_frames_count) -> List[HandPose]:
        hand_poses_list = self.estimated_hand_poses.get_hand_pose_list(hand_pose.hand_type)
        bottom_index = max(0, hand_pose.index - previous_frames_count)
        top_index = hand_pose.index + next_frames_count
        return hand_poses_list[bottom_index:top_index + 1]

    def __create_image_strip_data(self, hand_pose: HandPose, fps: float) -> ImageStripData:
        if bpy.context.scene.overlay_settings.center_align_hand_poses:
            start_frame, end_frame = self.__get_center_aligned_frames(hand_pose, fps)
        else:
            start_frame, end_frame = self.__get_edge_aligned_frames(hand_pose, fps)

        return ImageStripData(
            start_frame,
            end_frame,
            hand_pose.image_filename,
            hand_pose.hand_type)

    def __get_edge_aligned_frames(self, hand_pose: HandPose, fps: float) -> Tuple[int, Optional[int]]:
        hand_poses_list = self.estimated_hand_poses.get_hand_pose_list(hand_pose.hand_type)
        start_frame = round(hand_pose.timestamp * fps)
        max_end_frame = start_frame + round(MAX_IMAGE_STRIP_LENGTH_SECS * fps)

        # handle edge case (last hand pose)
        if hand_pose.index == len(hand_poses_list) - 1:
            return start_frame, min(max_end_frame, bpy.context.window_manager.video_reference_properties.duration + 1)

        end_frame = round(hand_poses_list[hand_pose.index + 1].timestamp * fps)
        # shorten to max image strip length
        return start_frame, min(end_frame, max_end_frame)

    def __get_center_aligned_frames(self, hand_pose: HandPose, fps: float) -> Tuple[int, Optional[int]]:
        hand_poses_list = self.estimated_hand_poses.get_hand_pose_list(hand_pose.hand_type)
        hand_pose_frame = hand_pose.timestamp * fps
        max_length_frames_half = int((MAX_IMAGE_STRIP_LENGTH_SECS * fps) // 2)

        # START FRAME
        if hand_pose.index == 0:  # handle edge case (first hand pose)
            start_frame = round(hand_pose_frame)
        else:
            prev_frame = hand_poses_list[hand_pose.index - 1].timestamp * fps
            start_frame = int((hand_pose_frame + prev_frame) // 2)

        # END FRAME
        if hand_pose.index == len(hand_poses_list) - 1:  # handle edge case (last hand pose)
            end_frame = round(hand_pose_frame + max_length_frames_half)
            return start_frame, min(end_frame, bpy.context.window_manager.video_reference_properties.duration + 1)
        end_frame = hand_poses_list[hand_pose.index + 1].timestamp * fps
        end_frame = int((hand_pose_frame + end_frame) // 2)

        # shorten to (MAX_IMAGE_STRIP_LENGTH_SECS / 2) seconds from either side
        start_frame = max(start_frame, round(hand_pose_frame) - max_length_frames_half)
        end_frame = min(end_frame, round(hand_pose_frame) + max_length_frames_half)
        return start_frame, end_frame

    def __create_image(self, hand_pose: HandPose) -> None:
        if hand_pose.image_filename is None:
            filename = f"hand_pose{hand_pose.index}{hand_pose.hand_type.name}.png"
            full_path = os.path.join(HAND_POSES_DIRECTORY, filename)
            create_hand_pose_image(self.image_size[0], self.image_size[1], hand_pose.normalized_positions, full_path)
            hand_pose.image_filename = filename
