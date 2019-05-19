from typing import List

from ydk.models.cisco_ios_xr import Cisco_IOS_XR_segment_routing_ms_cfg as sr_config

from src.backend.model.segmentList import SegmentList


def write_segments(segments: SegmentList):
    result: List[sr_config.Sr.traffic_engineering.segments.Segment] = []
    for label in segments.labels:
        segment = sr_config.Sr.traffic_engineering.segments.Segment()
        segment.mpls_label = label.label
        segment.segment_type = label.type
        result.append(segment)
    return result
