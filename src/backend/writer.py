from typing import List

from ydk.models.cisco_ios_xr import Cisco_IOS_XR_segment_routing_ms_cfg as sr_config

from src.backend.model.candidatePath import CandidatePath
from src.backend.model.policy import Policy
from src.backend.model.segmentList import SegmentList


def write_policy(config: sr_config.Sr, policy: Policy):
    for paths in policy.paths:
        write_segments(config, paths.hops)  # Write segment list

    color: sr_config.Sr.traffic_engineering.OnDemandColors.OnDemandColor = sr_config.Sr.traffic_engineering.OnDemandColors.OnDemandColor()
    color.color = policy.color
    rule: sr_config.Sr.traffic_engineering.policies.policy = sr_config.Sr.traffic_engineering.policies.Policy()
    rule.policy_name = policy.name
    rule.policy_color_endpoint = color
    for path in policy.paths:
        write_candidate_path(path, config)
    return rule


def write_segments(config: sr_config.Sr, segments: List[SegmentList]):
    for segment in segments:
        config.traffic_engineering.segments.segment.append(write_segment(segment))


def write_segment(segment: SegmentList):
    result: List[sr_config.Sr.traffic_engineering.segments.Segment] = []
    for label in segment.labels:
        segment = sr_config.Sr.traffic_engineering.segments.Segment()
        segment.mpls_label = label.label
        segment.segment_type = label.type
        result.append(segment)
    return result


def write_candidate_path(path: CandidatePath, config: sr_config.Sr):
    preference: sr_config.Sr.traffic_engineering.policies.policy.candidate_paths.preferences.Preference()
    preference.path_index = path.preference
    info = preference.path_infos.Path_info()
    info.segment_list_name = path.hops[0].name
    preference.path_infos.path_info.append(info)
