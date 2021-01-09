import datetime
import io
import os
import re

import boto3
import pandas as pd

from monday_stats.monday_model import MondayModel


def summary_handler(event, context):
    """Monday handler."""
    board_ids = os.environ["MONDAY_BOARD_IDS"].split(",")
    groups = os.environ["MONDAY_BOARD_GROUPS"].split(",")
    group_key = os.environ["MONDAY_BOARD_GROUP_KEY"]
    s3_dir = os.environ["S3_DIR"]

    mm = MondayModel()
    for board_id in board_ids:
        board = mm.board_with_items(board_id)
        df = board_summary(board, group_key, groups)
        s3path = f'{s3_dir}/{datetime.datetime.today().strftime("%Y%m%d")}_{board.name}.csv'
        s = io.StringIO()
        df.to_csv(s)
        write_s3(s.getvalue(), s3path)


def board_summary(board, group_key, groups=[]):
    """Summarize board.

    Args:
        board (monday.board.Board): monday Board class.
        group_key (str): group key which need to be one of board columns.
        groups (`list` of `str`): monday group title list.

    Returns:
        pandas.DataFrame: summarized dashboard.

    """
    dfs = board.groups_dataframes()
    value_texts = os.environ["MONDAY_BOARD_VALUES"].split(",")
    columns = os.environ["MONDAY_BOARD_COLUMNS"].split(",")
    existing_groups = set(groups).intersection(dfs.keys())
    if not dfs:
        return pd.DataFrame()
    df = pd.concat([dfs[g] for g in existing_groups])
    summary = pd.concat(
        [
            summarize_group(gdf, group_id, value_texts=value_texts, columns=columns)
            for group_id, gdf in df.groupby("Position")
        ]
    )
    output_index = pd.MultiIndex.from_product([df[group_key].unique(), value_texts])
    return summary.reindex(output_index).fillna(0).astype(int)


def summarize_group(gdf, group_id, columns, value_texts):
    """Summarize group df.

    Args:
        gdf (pd.DataFrame): items in the group.
        group_id (str): monday group id.
        columns (`list` of `str`): target columns
        value_texts (`list` of `str`): target values.

    Returns:
        pd.DataFrame: group summary.

    """
    summary = gdf[columns].apply(pd.value_counts).reindex(value_texts)
    summary.index = summary.index.map(lambda x: (group_id, x))
    return summary


def write_s3(text, s3path):
    """Write text to s3.

    Args:
        text (str): text.
        s3path(str): s3 file path.

    """
    obj = get_s3_object(s3path)
    return obj.put(Body=text, ContentEncoding="utf-8", ContentType="text/plane")


def get_s3_object(s3path):
    """Get s3 object.

    Args:
        s3path (str): s3 path to file.
        s3: boto3.resources.factory.s3.ServiceResource: s3 resource

    Returns:
        S3.Object: s3 access object.

    """
    s3 = boto3.resource("s3")
    bucket_name, key_name = get_bucket_key(s3path)
    return s3.Object(bucket_name, key_name)


def get_bucket_key(s3path):
    """Extract bucket name and key name from s3 path.

    Args:
        s3path (str): s3 path to file.

    Returns:
        string, string: bucket name and key name

    Examples:
            >>> get_bucket_key('s3://3idea-dev/foo/bar/baz')
            ('3idea-dev', 'foo/bar/baz')

    """
    bucket_name, key_name = re.match(r"(s3://)(.+?)/(.*)", s3path).group(2, 3)
    return bucket_name, key_name


if __name__ == "__main__":
    summary_handler({}, {})
