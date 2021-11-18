from importlib.metadata import entry_points
from gym.envs.registration import register

register(
    id="match-the-tiles-v0",
    entry_point="matchthetiles.envs.mtt_4x4_1block:MTT_4x4_1B",
)

register(
    id="match-the-tiles-v1",
    entry_point="matchthetiles.envs.mtt_4x4_2block:MTT_4x4_2B"
)

register(
    id="match-the-tiles-v2",
    entry_point="matchthetiles.envs.mtt_4x4_2block_hard:MTT_4x4_2B_Hard"
)