from typing import List

from ydk.models.cisco_ios_xr import Cisco_IOS_XR_segment_routing_ms_cfg as sr_config

from src.backend.model.candidatePath import CandidatePath
from src.backend.model.label import Label
from src.backend.model.policy import Policy
from src.backend.model.segmentList import SegmentList


def parse_policy(sr_config_mapping) -> List[Policy]:
    """Parses policy objects"""
    segments = parse_segment_list(sr_config_mapping)
    return list(map(lambda policy:
                    Policy(policy.policy_name, policy.policy_color_endpoint.color,
                           parse_candidate_path(policy, segments))
                    , sr_config_mapping.traffic_engineering.policies.policy))


def parse_candidate_path(policy, segments: List[SegmentList]) -> List[CandidatePath]:
    """Parses a candidate path"""
    return list(map(
        lambda preference: CandidatePath(preference.path_index, parse_segment(preference, segments)),
        policy.candidate_paths.preferences.preference
    ))


def parse_segment(preference, segments: List[SegmentList]) -> List[SegmentList]:
    """Add segments to policy according to different pathinfo"""
    result: List[SegmentList] = []
    for pathinfo in preference.path_infos.path_info:
        result.extend(filter(lambda segment: segment.name == pathinfo.segment_list_name, segments))
    return result


def parse_segment_list(sr: sr_config.Sr) -> List[SegmentList]:
    """Parse actual segment list which will be referenced afterwards"""
    return list(map(
        lambda segment: SegmentList(segment.path_name, list(map(
            lambda label: Label(label.mpls_label, label.segment_type), segment.segments.segment))),
        sr.traffic_engineering.segments.segment))
