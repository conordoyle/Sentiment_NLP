


import plotly.graph_objects as go
import pandas as pd

def _code_mapping(df, src, targ):
    """ Set labels and codes by linking source values to target values
    df: dataframe
    src (str): name of source series
    targ (str): name of target series
    """

    # Get distinct labels
    labels = sorted(list(set(list(df[src]) + list(df[targ]))))

    # Get integer codes
    codes = list(range(len(labels)))

    # Create label to code mapping
    lc_map = dict(zip(labels, codes))

    # Substitute names for codes in dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels

def _stack_columns(df, cols, threshold, vals=None):
    """ stack column pairs
    df: dataframe
    cols: a list of columns
    threshold (int): filter out vals based on threshold (for visual appeal)
    vals (str): the values series in df
    """

    # if vals column is not given
    if vals==None:
        stacked_df = pd.DataFrame({'src': [], 'target': []})

        for i in range(len(cols) - 1):
            # pair columns and aggregate data
            new_df = df[[cols[i], cols[i + 1]]]
            new_df = new_df.groupby([cols[i], cols[i + 1]]).size().reset_index(name = 'vals')

            new_df.columns = ['src', 'target', 'vals']

            # implement threshold
            new_df = new_df[new_df['vals'] >= threshold]

            # concatenate the two df
            stacked_df = pd.concat([stacked_df, new_df], axis=0)

    # if vals column is given
    else:
        stacked_df = pd.DataFrame({'src': [], 'target': [], 'vals': []})

        for i in range(len(cols) - 1):
            # pair columns and aggregate data
            new_df = df[[cols[i], cols[i + 1]]]
            new_df = new_df.groupby([cols[i], cols[i + 1]]).sum(vals).reset_index()

            new_df.columns = ['src', 'target', 'vals']

            # implement threshold
            new_df = new_df[new_df['vals'] >= threshold]

            # concatenate the two df
            stacked_df = pd.concat([stacked_df, new_df], axis=0)

    return stacked_df


def make_sankey(df, cols, threshold, vals=None, **kwargs):
    """ Create a sankey diagram that takes in a list of columns, linking source values to
    target values with thickness vals
    df: dataframe
    cols (list): a list of columns in df
    threshold (int): a value to filter the vals count (for visual appeal)
    vals (str): the name of value series in df
    """

    # stack columns in pairs
    df = _stack_columns(df, cols, threshold, vals)

    # link source values to target values
    df, labels = _code_mapping(df, 'src', 'target')

    link = {'source': df['src'], 'target': df['target'], 'value': df.vals}
    pad = kwargs.get('pad', 20)

    # configure sankey diagram
    node = {'label': labels, 'pad': pad}
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)

    # set sankey dimensions
    width = kwargs.get('width', 1500)
    height = kwargs.get('height', 750)
    fig.update_layout(
        autosize = False,
        width = width,
        height = height)

    fig.show()
