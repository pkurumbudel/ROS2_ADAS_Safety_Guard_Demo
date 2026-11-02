import math
from safety_guard_demo.guard_logic import Proposal, ProposalGuard, Policy, Verdict
NOW=1_000_000_000

def p(seq=1,delay_ms=0,dec=4.0,confidence=.9,valid=True):
    return Proposal(seq,NOW-int(delay_ms*1_000_000),dec,confidence,valid)

def test_nominal_and_replay():
    g=ProposalGuard();assert g.check(p(),NOW,clock_trusted=True)==Verdict.ACCEPT
    assert g.check(p(),NOW,clock_trusted=True)==Verdict.REPLAY

def test_stale_rejected():
    assert ProposalGuard().check(p(delay_ms=150),NOW,clock_trusted=True)==Verdict.STALE

def test_nan_rejected():
    assert ProposalGuard().check(p(dec=math.nan),NOW,clock_trusted=True)==Verdict.INVALID

def test_clock_health_fail_closed():
    assert ProposalGuard().check(p(),NOW,clock_trusted=False)==Verdict.CLOCK_UNTRUSTED

def test_too_strong_request_rejected():
    assert ProposalGuard().check(p(dec=12.),NOW,clock_trusted=True)==Verdict.OUT_OF_RANGE

def test_future_timestamp_rejected():
    q=Proposal(1,NOW+100_000_000,4.0,.8,True)
    assert ProposalGuard().check(q,NOW,clock_trusted=True)==Verdict.FUTURE_TIMESTAMP
