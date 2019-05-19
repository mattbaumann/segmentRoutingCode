from typing import List

from ydk.models.cisco_ios_xr import Cisco_IOS_XR_segment_routing_ms_cfg as sr_config

from src.backend.model.candidatePath import CandidatePath
from src.backend.model.label import Label
from src.backend.model.policy import Policy
from src.backend.model.segmentList import SegmentList


def parse_policy(sr_config_mapping):
    policies = []
    for policy in sr_config_mapping.traffic_engineering.policies.policy:
        paths = []
        for preference in policy.candidate_paths.preferences.preference:
            segments = []
            for pathinfo in preference.path_infos.path_info:
                segments.append(SegmentList(preference.path_index.__str__(),
                                            read_segment_list(sr_config_mapping, pathinfo.segment_list_name)))
            paths.append(CandidatePath(preference.path_index, segments))
        policies.append(Policy(policy.policy_name, policy.policy_color_endpoint.color, paths))
    return policies


def read_segment_list(sr: sr_config.Sr, segment_name: str):
    segments: List[Label] = []
    for segment in sr.traffic_engineering.segments.segment:
        if segment_name == segment.path_name:
            for segmentItem in segment.segments.segment:
                segments.append(Label(segmentItem.mpls_label, segmentItem.segment_type))
    return segments
