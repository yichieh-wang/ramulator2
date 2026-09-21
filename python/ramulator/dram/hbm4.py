import math

from ramulator.dram.spec import DRAMStandard, TimingConstraint


class HBM4(DRAMStandard):
    name = "HBM4"
    internal_prefetch_size = 8
    data_payload_bytes = 32  # One pseudochannel
    tick_multiplier = 2
    read_latency = "nCL + nBL"

    levels = {
        "Channel":        "N_A",
        "PseudoChannel":  "N_A",
        "Sid":            "N_A",
        "BankGroup":      "N_A",
        "Bank":           "Closed",
        "Row":            "Closed",
        "Column":         "N_A",
    }

    commands = [
        "ACT", "PREpb", "PREab",
        "RD", "WR", "RDA", "WRA",
        "REFab", "REFpb",
        "RFMab", "RFMpb",
    ]

    command_cycles = {
        "ACT": 1.5,
        "PREpb": 0.5, "PREab": 0.5,
        "REFab": 0.5, "REFpb": 0.5,
        "RFMab": 0.5, "RFMpb": 0.5,
    }

    row_commands = ["ACT", "PREpb", "PREab", "REFab", "REFpb", "RFMab", "RFMpb"]
    column_commands = ["RD", "WR", "RDA", "WRA"]

    states = ["Opened", "Closed", "N_A"]

    timing_params = [
        "rate", "nBL", "nCL", "nRCDRD", "nRCDWR",
        "nRP", "nRAS", "nRC", "nWR", "nRTP", "nCWL",
        "nCCDS", "nCCDL", "nCCDR",
        "nRRDS", "nRRDL",
        "nWTRS", "nWTRL", "nRTW",
        "nFAW", "nPPD",
        "nRFC", "nRFCpb", "nRFMab", "nRFMpb",
        "nRREFD",
        "nREFI", "nREFIpb",
        "tCK_ps",
    ]

    supported_requests = {"Read": "RD", "Write": "WR"}

    timing_constraints = [
        # Pseudochannel timing
        TimingConstraint(level="PseudoChannel", preceding=["RD", "RDA"], following=["RD", "RDA"], latency="nBL"),
        TimingConstraint(level="PseudoChannel", preceding=["WR", "WRA"], following=["WR", "WRA"], latency="nBL"),
        TimingConstraint(level="PseudoChannel", preceding=["RD", "RDA"], following=["WR", "WRA"], latency="nRTW"),
        TimingConstraint(level="PseudoChannel", preceding=["WR", "WRA"], following=["RD", "RDA"], latency="nCWL + nBL + nWTRS"),
        TimingConstraint(level="PseudoChannel", preceding=["RD", "RDA"], following=["PREab"], latency="nRTP"),
        TimingConstraint(level="PseudoChannel", preceding=["WR", "WRA"], following=["PREab"], latency="nCWL + nBL + nWR"),
        TimingConstraint(level="PseudoChannel", preceding=["ACT"], following=["ACT"], latency="nRRDS"),
        TimingConstraint(level="PseudoChannel", preceding=["ACT", "REFpb", "RFMpb"], following=["ACT", "REFpb", "RFMpb"], latency="nFAW", window=4, shared_window=True),
        TimingConstraint(level="PseudoChannel", preceding=["ACT"], following=["PREab"], latency="nRAS"),
        TimingConstraint(level="PseudoChannel", preceding=["PREab"], following=["ACT"], latency="nRP"),
        TimingConstraint(level="PseudoChannel", preceding=["ACT"], following=["REFab"], latency="nRC"),
        TimingConstraint(level="PseudoChannel", preceding=["PREpb", "PREab"], following=["REFab"], latency="nRP"),
        TimingConstraint(level="PseudoChannel", preceding=["PREpb", "PREab"], following=["PREpb", "PREab"], latency="nPPD"),
        TimingConstraint(level="PseudoChannel", preceding=["RDA"], following=["REFab"], latency="nRP + nRTP"),
        TimingConstraint(level="PseudoChannel", preceding=["WRA"], following=["REFab"], latency="nCWL + nBL + nWR + nRP"),
        # JESD270-4A Table 38.
        TimingConstraint(level="PseudoChannel", preceding=["REFab"], following=["ACT", "PREab", "REFab", "REFpb", "RFMab", "RFMpb"], latency="nRFC"),
        TimingConstraint(level="PseudoChannel", preceding=["REFpb"], following=["REFpb", "RFMpb", "ACT"], latency="nRREFD"),
        TimingConstraint(level="PseudoChannel", preceding=["REFpb"], following=["REFab", "RFMab"], latency="nRFCpb"),
        TimingConstraint(level="PseudoChannel", preceding=["ACT"], following=["REFpb"], latency="nRRDS"),
        TimingConstraint(level="PseudoChannel", preceding=["ACT"], following=["RFMab"], latency="nRC"),
        TimingConstraint(level="PseudoChannel", preceding=["PREpb", "PREab"], following=["RFMab"], latency="nRP"),
        TimingConstraint(level="PseudoChannel", preceding=["RDA"], following=["RFMab"], latency="nRP + nRTP"),
        TimingConstraint(level="PseudoChannel", preceding=["WRA"], following=["RFMab"], latency="nCWL + nBL + nWR + nRP"),
        TimingConstraint(level="PseudoChannel", preceding=["RFMab"], following=["ACT", "PREab", "REFab", "REFpb", "RFMab", "RFMpb"], latency="nRFMab"),
        TimingConstraint(level="PseudoChannel", preceding=["RFMpb"], following=["REFpb", "RFMpb", "ACT"], latency="nRREFD"),
        TimingConstraint(level="PseudoChannel", preceding=["RFMpb"], following=["REFab", "RFMab"], latency="nRFMpb"),
        TimingConstraint(level="PseudoChannel", preceding=["ACT"], following=["RFMpb"], latency="nRRDS"),

        # SID timing
        TimingConstraint(level="Sid", preceding=["RD", "RDA"], following=["RD", "RDA"], latency="nCCDS"),
        TimingConstraint(level="Sid", preceding=["WR", "WRA"], following=["WR", "WRA"], latency="nCCDS"),
        TimingConstraint(level="Sid", preceding=["RD", "RDA"], following=["RD", "RDA"], latency="nCCDR", sibling=True),
        TimingConstraint(level="Sid", preceding=["WR", "WRA"], following=["WR", "WRA"], latency="nCCDS", sibling=True),

        # Bank-group timing
        TimingConstraint(level="BankGroup", preceding=["RD", "RDA"], following=["RD", "RDA"], latency="nCCDL"),
        TimingConstraint(level="BankGroup", preceding=["WR", "WRA"], following=["WR", "WRA"], latency="nCCDL"),
        TimingConstraint(level="BankGroup", preceding=["WR", "WRA"], following=["RD", "RDA"], latency="nCWL + nBL + nWTRL"),
        TimingConstraint(level="BankGroup", preceding=["ACT"], following=["ACT"], latency="nRRDL"),
        TimingConstraint(level="BankGroup", preceding=["ACT"], following=["REFpb", "RFMpb"], latency="nRRDL"),
        TimingConstraint(level="BankGroup", preceding=["REFpb", "RFMpb"], following=["ACT"], latency="nRRDL"),

        # Bank timing
        TimingConstraint(level="Bank", preceding=["ACT"], following=["ACT"], latency="nRC"),
        TimingConstraint(level="Bank", preceding=["ACT"], following=["RD", "RDA"], latency="nRCDRD"),
        TimingConstraint(level="Bank", preceding=["ACT"], following=["WR", "WRA"], latency="nRCDWR"),
        TimingConstraint(level="Bank", preceding=["ACT"], following=["PREpb"], latency="nRAS"),
        TimingConstraint(level="Bank", preceding=["PREpb"], following=["ACT"], latency="nRP"),
        TimingConstraint(level="Bank", preceding=["RD"], following=["PREpb"], latency="nRTP"),
        TimingConstraint(level="Bank", preceding=["WR"], following=["PREpb"], latency="nCWL + nBL + nWR"),
        TimingConstraint(level="Bank", preceding=["RDA"], following=["ACT", "REFpb", "RFMpb"], latency="nRTP + nRP"),
        TimingConstraint(level="Bank", preceding=["WRA"], following=["ACT", "REFpb", "RFMpb"], latency="nCWL + nBL + nWR + nRP"),
        TimingConstraint(level="Bank", preceding=["REFpb"], following=["REFpb", "RFMpb", "ACT"], latency="nRFCpb"),
        TimingConstraint(level="Bank", preceding=["ACT"], following=["REFpb"], latency="nRC"),
        TimingConstraint(level="Bank", preceding=["PREpb"], following=["REFpb"], latency="nRP"),
        TimingConstraint(level="Bank", preceding=["RFMpb"], following=["REFpb", "RFMpb", "ACT"], latency="nRFMpb"),
        TimingConstraint(level="Bank", preceding=["ACT"], following=["RFMpb"], latency="nRC"),
        TimingConstraint(level="Bank", preceding=["PREpb"], following=["RFMpb"], latency="nRP"),
    ]

    @classmethod
    def resolve_secondary_timings(cls, timing_dict, org_dict):
        # A preset states what it knows and leaves the rest here. Every value below is filled only
        # when the preset did not state it, so a preset off the JEDEC tables — a column channel,
        # whose density and rate no table lists — can name its own refresh and its own tCCD
        # instead of being handed a -1.
        tCK_ps = timing_dict["tCK_ps"]

        def unsaid(name):
            return name not in timing_dict

        if unsaid("nRC"):
            timing_dict["nRC"] = timing_dict["nRAS"] + timing_dict["nRP"]
        if unsaid("nCCDL"):
            timing_dict["nCCDL"] = cls._resolve_nCCDL(tCK_ps)
        if unsaid("nCCDR"):
            timing_dict["nCCDR"] = cls._resolve_nCCDR(
                timing_dict["rate"], tCK_ps, org_dict["sid"], timing_dict["nCCDS"]
            )
        if unsaid("nRTW"):
            timing_dict["nRTW"] = cls._resolve_nRTW(timing_dict, tCK_ps)
        if unsaid("nRFC"):
            timing_dict["nRFC"] = cls._resolve_nRFC(
                org_dict["die_density"], org_dict["stack_height"],
                org_dict["channel_density"], tCK_ps,
            )
        if unsaid("nRFCpb"):
            timing_dict["nRFCpb"] = cls._resolve_nRFCpb(
                org_dict["die_density"], tCK_ps
            )
        if unsaid("nRFMab"):
            timing_dict["nRFMab"] = timing_dict["nRFC"]
        if unsaid("nRFMpb"):
            timing_dict["nRFMpb"] = timing_dict["nRFCpb"]
        if unsaid("nREFI"):
            timing_dict["nREFI"] = cls._resolve_nREFI(tCK_ps)
        if unsaid("nREFIpb"):
            timing_dict["nREFIpb"] = cls._resolve_nREFIpb(
                tCK_ps,
                org_dict["bank"],
                org_dict["bankgroup"],
                org_dict["sid"],
            )
        if unsaid("nRREFD"):
            timing_dict["nRREFD"] = cls._resolve_nRREFD(tCK_ps)

    @staticmethod
    def _resolve_nCCDL(tCK_ps):
        # JESD270-4A Table 108: max(4 nCK, 2.5 ns).
        # This resolves to 5 CK at HBM4-8000, preventing full throughput.
        # So we set to 4 here
        # return max(4, math.ceil(2_500 / tCK_ps))
        return 4

    @staticmethod
    def _resolve_nCCDR(rate, tCK_ps, num_sids, nCCDS):
        # JESD270-4A Table 108 Note 17 specifies tCCDR only for multi-SID
        # stacks.
        offset = {
            (8_000, 500, 1): 0,
            # === Ramulator Guesstimate ===
            (8_000, 500, 2): 2,
            (8_000, 500, 4): 2,
            (16_000, 250, 1): 0,
            # =============================
        }.get((rate, tCK_ps, num_sids))
        return nCCDS + offset if offset is not None else -1

    @staticmethod
    def _resolve_nRTW(timing_dict, tCK_ps):
        if timing_dict["rate"] == 8_000 and tCK_ps == 500:
            # JESD270-4A Tables 107 and 108, Note 18.
            base_cycles = (
                timing_dict["nCL"] + timing_dict["nBL"] - timing_dict["nCWL"]
            )
            analog_numerator = 5 * tCK_ps + 10 * (2_500 - 100)
            return base_cycles + math.ceil(analog_numerator / (10 * tCK_ps))
        if timing_dict["rate"] == 16_000 and tCK_ps == 250:
            return 50  # Ramulator guesstimate
        return -1

    @staticmethod
    def _resolve_nRFC(die_density, stack_height, channel_density, tCK_ps):
        # JESD270-4A Table 108.
        tRFC_ns = {
            (24576, 4, 3072): 360,
            (24576, 8, 6144): 410,
            (24576, 12, 9216): 450,
            (24576, 16, 12288): 490,
            (32768, 4, 4096): 400,
            (32768, 8, 8192): 450,
            (32768, 12, 12288): 490,
            (32768, 16, 16384): 530,
        }.get((die_density, stack_height, channel_density))
        if tRFC_ns is None:
            return -1
        return math.ceil(tRFC_ns * 1000 / tCK_ps)

    @staticmethod
    def _resolve_nRFCpb(die_density, tCK_ps):
        # JESD270-4A Table 108.
        tRFCpb_ns = {24576: 240, 32768: 280}.get(die_density)
        if tRFCpb_ns is None:
            return -1
        return math.ceil(tRFCpb_ns * 1000 / tCK_ps)

    @staticmethod
    def _resolve_nREFI(tCK_ps):
        # JESD270-4A Table 108 specifies a maximum interval of 3.9 us.
        return 3_900_000 // tCK_ps

    @staticmethod
    def _resolve_nREFIpb(tCK_ps, num_banks, num_bankgroups, num_sids):
        # JESD270-4A Table 108: tREFIpb = tREFI / banks per pseudo-channel.
        return 3_900_000 // (num_banks * num_bankgroups * num_sids * tCK_ps)

    @staticmethod
    def _resolve_nRREFD(tCK_ps):
        # HBM4 tRREFD = MAX(3*tCK, 8 ns)
        return max(3, math.ceil(8_000 / tCK_ps))



HBM4.org_presets = {
    # HBM CA already takes BL into account
    # One preset is one 64-bit JEDEC channel split into two 32-bit
    # pseudo-channels (JESD270-4A Table 4).
    "HBM4_32Gb_4Hi":  {"die_density": 32768, "channel_density": 4096,  "stack_height": 4,  "dq": 32, "channel_width": 64, "pseudochannel": 2, "sid": 1, "bankgroup": 2, "bank": 8, "row": 1 << 14, "column": (1 << 5) << 3},
    "HBM4_32Gb_8Hi":  {"die_density": 32768, "channel_density": 8192,  "stack_height": 8,  "dq": 32, "channel_width": 64, "pseudochannel": 2, "sid": 2, "bankgroup": 2, "bank": 8, "row": 1 << 14, "column": (1 << 5) << 3},
    "HBM4_32Gb_16Hi": {"die_density": 32768, "channel_density": 16384, "stack_height": 16, "dq": 32, "channel_width": 64, "pseudochannel": 2, "sid": 4, "bankgroup": 2, "bank": 8, "row": 1 << 14, "column": (1 << 5) << 3},
}

HBM4.timing_presets = {
    "HBM4_8000Mbps": {
        "rate": 8000, "nBL": 2,
        "nCCDS": 2,
        # === Ramulator Guesstimate ===
        "nCL": 20, "nCWL": 10,
        "nRAS": 57, "nRP": 33,
        "nRCDRD": 39, "nRCDWR": 19,
        "nRRDL": 7, "nRRDS": 5, "nFAW": 30,
        "nRTP": 12, "nWR": 42,
        "nWTRL": 13, "nWTRS": 9,
        # =============================
        "nPPD": 2, "tCK_ps": 500,
    },
    "HBM4_16000Mbps": {
        "nCWL": -1,
        # === Ramulator Guesstimate ===
        "rate": 16000, "nBL": 2, "nCL": 40,
        "nRAS": 114, "nRP": 66,
        "nRCDRD": 78, "nRCDWR": 38,
        "nRRDL": 14, "nRRDS": 10, "nFAW": 60,
        "nRTP": 24, "nWR": 84, "nCCDS": 2,
        "nWTRL": 26, "nWTRS": 18,
        "nPPD": 2, "tCK_ps": 250,
        # =============================
    },
}


# ---- The column channel ---------------------------------------------------------------------
#
# A DRAM stack bonded face to face on the compute reticle. A channel there is the column of
# banks under one tile — one bank a DRAM layer — reached over bonded pads instead of a PHY, so it
# is wide and slow: the whole channel width moves in one beat at the array's own clock. None of
# HBM's packaging levels are in a column, so pseudo-channel, SID and bank group all count 1, which
# is as simple as the HBM4 level list allows (the C++ carries all seven levels either way, and a
# level of count 1 costs one address bit of nothing). The array is HBM4's, so the timings are
# HBM4-8000's own nanoseconds (below), stated in whole cycles of whatever clock the column runs at.

# The array timings a column keeps are HBM4-8000's own, read off the preset above (cycles at its
# tCK, turned into nanoseconds) so there is one place they are written; ramulator2 marks that
# preset's values a guesstimate, and a column inherits that. Refresh is not in the preset — the
# resolver looks it up by die density — so the two refresh times are stated here from the JEDEC
# table for the 16-high 32 Gb stack (JESD270-4A Table 108): all-bank 530 ns, per-bank 280 ns. A
# column is refreshed a bank at a time, so it is nRFCpb the streams feel.
COLUMN_ARRAY_FROM = "HBM4_8000Mbps"
COLUMN_ARRAY_KEYS = ("nCL", "nCWL", "nRAS", "nRP", "nRCDRD", "nRCDWR", "nRRDL", "nRRDS", "nFAW", "nRTP", "nWR", "nWTRL", "nWTRS", "nPPD")
COLUMN_REFRESH_NS = {"nRFC": 530.0, "nRFCpb": 280.0}


def column_array_ns():
    """HBM4's array timings in nanoseconds, from the preset they are kept in."""
    preset = HBM4.timing_presets[COLUMN_ARRAY_FROM]
    ns = {name: preset[name] * preset["tCK_ps"] / 1000 for name in COLUMN_ARRAY_KEYS}
    ns.update(COLUMN_REFRESH_NS)
    return ns


def column_org(channel_width_bits, banks, rows, row_bytes=1024):
    """A column's organization: `channel_width_bits` data bits under one tile, `banks` banks (one a
    layer) of `rows` rows, each row `row_bytes` wide. One beat of the channel is one transaction,
    so data_payload_bytes is the channel width in bytes and the column count is the row's worth of
    beats times the standard's prefetch — the address mapper drops prefetch column bits, one
    transaction covering them all. None of HBM's packaging levels are in a column: pseudo-channel,
    SID and bank group count 1."""
    beat = channel_width_bits // 8
    if channel_width_bits % 8 or beat <= 0:
        raise ValueError(f"a column channel of {channel_width_bits} bits is no whole number of bytes a beat")
    if row_bytes % beat:
        raise ValueError(f"a row of {row_bytes} bytes is no whole number of {beat}-byte beats")
    beats_per_row = row_bytes // beat
    for name, count in (("banks", banks), ("rows", rows), ("beats a row", beats_per_row)):
        if count <= 0 or count & (count - 1):
            raise ValueError(f"a column channel's {name} must be a power of two, and {count} is not — the address mapper cuts whole bits")
    channel_mbit = banks * rows * row_bytes * 8 // (1 << 20)
    return {
        "die_density": channel_mbit // banks, "channel_density": channel_mbit, "stack_height": banks,
        "dq": channel_width_bits, "channel_width": channel_width_bits,
        "pseudochannel": 1, "sid": 1, "bankgroup": 1, "bank": banks,
        "row": rows, "column": beats_per_row * HBM4.internal_prefetch_size,
        "data_payload_bytes": beat,
    }


def column_timing(line_rate_gbps):
    """A column's timing at `line_rate_gbps` a pin: one bit a pin a cycle, so the cycle is the pin's,
    and one beat — one transaction — is one cycle. The array numbers are HBM4's nanoseconds
    rounded up to whole cycles. Nothing but the bus separates two column commands in a column, so
    tCCD is the beat, over bank groups and SIDs that are not there."""
    rate = int(round(line_rate_gbps * 1000))
    if 1_000_000 % rate:
        raise ValueError(f"{line_rate_gbps} Gbps a pin is not a whole number of picoseconds a cycle")
    tCK_ps = 1_000_000 // rate
    timing = {name: math.ceil(ns * 1000 / tCK_ps) for name, ns in column_array_ns().items()}
    timing["rate"] = rate
    timing["tCK_ps"] = tCK_ps
    timing["nBL"] = 1
    timing["nCCDS"] = timing["nCCDL"] = timing["nCCDR"] = timing["nBL"]
    # JESD270-4A Tables 107 and 108, Note 18, at this column's cycle.
    timing["nRTW"] = timing["nCL"] + timing["nBL"] - timing["nCWL"] + math.ceil(0.5 + 2_400 / tCK_ps)
    return timing


# The design point: the 16-high column over a tile, 512 data bits at 1 GHz, 1 KiB rows, 1 GiB a
# channel. `render_column` in the harness's configs starts from these two and overrides whatever
# the design it is given states differently.
HBM4.org_presets["Column_16Hi_512b"] = column_org(512, banks=16, rows=1 << 16)
HBM4.timing_presets["Column_1000Mbps"] = column_timing(1.0)
