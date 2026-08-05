from dataclasses import dataclass

@dataclass
class ObsConfigInfo:
    obs_username: str
    obs_pw: str

@dataclass
class WebcamInfo:
    webcam_idx: int

@dataclass
class RunConfigInfo:
    is_debug: bool
    render_img: bool
    output_type: str
    input_type: str
    obs_config_info: obsConfigInfo
    webcam_info: webcamInfo
