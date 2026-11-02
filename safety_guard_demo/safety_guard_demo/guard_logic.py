"""Illustrative guard logic - NOT ASIL-capable and NEVER directly actuates a vehicle.

Models three failure classes: stale samples, replayed sequence numbers,
and implausible numeric requests. Timing values below are examples only.
"""
from dataclasses import dataclass
from enum import Enum
from math import isfinite

class Verdict(str, Enum):
    ACCEPT = 'ACCEPT'
    STALE = 'STALE'
    FUTURE_TIMESTAMP = 'FUTURE_TIMESTAMP'
    CLOCK_UNTRUSTED = 'CLOCK_UNTRUSTED'
    REPLAY = 'REPLAY'
    INVALID = 'INVALID'
    OUT_OF_RANGE = 'OUT_OF_RANGE'

@dataclass(frozen=True)
class Proposal:
    sequence: int
    sensor_time_ns: int
    deceleration_mps2: float
    confidence: float
    valid: bool

@dataclass(frozen=True)
class Policy:
    max_age_ns: int = 120_000_000  # DEMO ONLY: derived from no HARA/FTTI
    max_future_skew_ns: int = 5_000_000  # DEMO ONLY
    max_deceleration_mps2: float = 8.0 # DEMO ONLY
    minimum_confidence: float = 0.6    # DEMO ONLY

class ProposalGuard:
    def __init__(self, policy: Policy = Policy()):
        self.policy = policy
        self.last_sequence: int | None = None

    def check(self, proposal: Proposal, now_ns: int, *, clock_trusted: bool) -> Verdict:
        # Must be in one validated time domain; test harness supplies this guarantee.
        if not clock_trusted:
            return Verdict.CLOCK_UNTRUSTED
        age = now_ns - proposal.sensor_time_ns
        if age < -self.policy.max_future_skew_ns:
            return Verdict.FUTURE_TIMESTAMP
        if age > self.policy.max_age_ns:
            return Verdict.STALE
        if self.last_sequence is not None and proposal.sequence <= self.last_sequence:
            return Verdict.REPLAY
        if not proposal.valid or not isfinite(proposal.deceleration_mps2) or not isfinite(proposal.confidence):
            return Verdict.INVALID
        if not (0.0 <= proposal.deceleration_mps2 <= self.policy.max_deceleration_mps2):
            return Verdict.OUT_OF_RANGE
        if not (self.policy.minimum_confidence <= proposal.confidence <= 1.0):
            return Verdict.OUT_OF_RANGE
        self.last_sequence = proposal.sequence
        return Verdict.ACCEPT
