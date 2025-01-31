import sys
from json import JSONDecodeError
from typing import List, Dict
import numpy as np
from PIL import Image
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions
import json

import time


def create_hand_pose_image(image_height: int, image_width: int,
                           normalized_positions: List[Dict[str, float]]) -> np.ndarray:
    image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    landmark_list = landmark_pb2.NormalizedLandmarkList()
    landmark_list.landmark.extend([
        landmark_pb2.NormalizedLandmark(
            x=landmark['x'], y=landmark['y'], z=landmark['z']
        ) for landmark in normalized_positions
    ])

    solutions.drawing_utils.draw_landmarks(
        image,
        landmark_list,
        solutions.hands.HAND_CONNECTIONS,
        solutions.drawing_styles.get_default_hand_landmarks_style(),
        solutions.drawing_styles.get_default_hand_connections_style())

    return image


def save_hand_pose_image(image: np.ndarray, filepath: str) -> str:
    image = Image.fromarray(image, mode='RGB')
    if filepath[-4:] != ".png":
        filepath += ".png"
    image.save(filepath, compress_level=0, transparency=(0, 0, 0))
    return filepath


def main():
    """
    Command line arguments:
        filepath:       path to where the generated image will be saved including the filename
        image_height:   height of the generated image in pixels
        image_width:    width of the generated image in pixels
        positions:      hand pose's normalized positions in json string format
    """

    start_time = time.time()
    usage = f"Usage: python {sys.argv[0]} <filepath> <image_height> <image_width> <positions> " + main.__doc__
    if len(sys.argv) != 5:
        raise ValueError("Invalid number of arguments. " + usage)
    if not sys.argv[2].isdecimal():
        raise ValueError(f"Invalid image height argument. " + usage)
    if not sys.argv[3].isdecimal():
        raise ValueError(f"Invalid image width argument. " + usage)
    try:
        normalized_positions = json.loads(sys.argv[4])
    except JSONDecodeError:
        raise ValueError(f"Invalid <positions> argument. " + usage)

    filepath = sys.argv[1]
    height = int(sys.argv[2])
    width = int(sys.argv[3])

    image = create_hand_pose_image(height, width, normalized_positions)
    save_hand_pose_image(image, filepath)
    print("total skript time: " + str(time.time() - start_time))


if __name__ == "__main__":
    main()
