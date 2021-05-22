from gym.envs.registration import register

register(
    id="match-the-tiles-v0",
    entry_point="matchthetiles.envs.mtt_4x4_1block:MTT_4x4_1B",
)
