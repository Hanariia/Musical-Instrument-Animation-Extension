# Musical Instrument Animation Reference Extension
A Blender add-on designed to display a reference video and visualize hand pose data 
from a JSON file in form of an overlay, using output from the [Hand Capture](https://github.com/KubakCz/mediapipe-hand-tracking) web 
application. 

The add-on is intended to be an extension for the [Musical Instrument Animation](https://github.com/KubakCz/MusicalInstrumentCapture) 
Blender add-on. This add-on enhances the original add-on by helping
the animator quickly identify the incorrectly estimated hand poses, find the cause of 
errors in the animation, as well as providing a video reference of the desired hand poses.


## Installation

**Requirements:** Blender 4.0.0–4.3.2

Before using the add-on, it is necessary to install the [Pillow](https://pillow.readthedocs.io/en/stable/index.html) 
library either directly into Blender's Python installation (requires administrator rights) or into the
user site-packages.

To install the Pillow library you can use the following command:

`pip --python <path_to_blenders_python_executable> install Pillow --target <path_to_user_site_pkgs>`

To easily find the necessary paths for the command, attempt installing and enabling the add-on without the Pillow 
library. This should result in an error that shows the exact command needed to install the library.

Finally, to install the add-on in Blender go to ***Edit > Preferences > Add-ons***. There, click the drop-down button 
in the top right corner, choose ***Install from Disk...***, select the add-on's .zip file and confirm the installation.

## Usage
The add-on is operated through two different panels. The first panel, named _Estimated Hand Poses Reference_, is located 
in the sidebar of the 3D Viewport in the Musical Instrument Animation category and contains the general controls for 
operating the add-on. The second panel _Overlay Settings_ can be found in Video Reference category in the sidebar of the
Preview where the reference is shown to the user.

### To set up the reference:
1) Make sure the full-body motion capture animation is imported first. (Only necessary if you wish to sync the reference with the animation.)
2) In the _Estimated Hand Poses Reference_ panel, click the _Setup Video Reference_ button to import the video and open the Preview.
3) Import the estimated hand poses JSON file through the _Import Hand Poses_ button.


### Mitigating playback slowdown:
To temporarily increase playback speed when the overlay is not needed, you can:
- Disable the visibility of hands in the _Overlay Settings_ panel. 
- Pause overlay generation in the _Estimated Hand Poses Reference_ panel.

