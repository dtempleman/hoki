from hoki.statblock import StatBlock, generate_inital_stats, get_df_row

from dataclasses import fields


def test_statblock():
    zero_stats = StatBlock()
    for field in fields(StatBlock):
        assert getattr(zero_stats, field.name) == 0

    rand_stats = generate_inital_stats()
    for field in fields(StatBlock):
        assert getattr(rand_stats, field.name) >= 0 and getattr(rand_stats, field.name) <= 1

    row = get_df_row(rand_stats)
    for idx, field in enumerate(fields(StatBlock)):
        assert getattr(rand_stats, field.name) == row[idx]
