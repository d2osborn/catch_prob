"""
takes the statcast positioning data and merges them by the filters used at the site into one master csv per set of filters
statcast url: https://baseballsavant.mlb.com/visuals/fielder-positioning
"""
import pandas as pd
from pathlib import Path

def load_positioning_data():
    positioning_ = ['all_situations', 
                    'lhh_000_shift', 'lhh_000_no_shift', 
                    'lhh_001_shift', 'lhh_001_no_shift',
                    'lhh_else_shift', 'lhh_else_no_shift', 
                    'rhh_000_no_shift', 'rhh_000_shift', 
                    'rhh_001_shift', 'rhh_001_no_shift',
                    'rhh_else_shift', 'rhh_else_no_shift', 
                    ]
    dfs = {}
    
    script_dir = Path(__file__).parent
    
    for folder in positioning_:
        folder_path = script_dir / 'data' / folder
        folder_dfs = []
        for csv in folder_path.glob('*.csv'):
            folder_dfs.append(pd.read_csv(csv))
        dfs[folder] = pd.concat(folder_dfs, ignore_index=True)

    all_situations_df = dfs['all_situations']

    lhh_000_no_shift_df = dfs['lhh_000_no_shift']
    lhh_000_shift_df = dfs['lhh_000_shift']
    lhh_001_no_shift_df = dfs['lhh_001_no_shift']
    lhh_001_shift_df = dfs['lhh_001_shift']
    lhh_else_no_shift_df = dfs['lhh_else_no_shift']
    lhh_else_shift_df = dfs['lhh_else_shift']

    rhh_000_no_shift_df = dfs['rhh_000_no_shift']
    rhh_000_shift_df = dfs['rhh_000_shift']
    rhh_001_no_shift_df = dfs['rhh_001_no_shift']
    rhh_001_shift_df = dfs['rhh_001_shift']
    rhh_else_no_shift_df = dfs['rhh_else_no_shift']
    rhh_else_shift_df = dfs['rhh_else_shift']

    return all_situations_df, \
        lhh_000_shift_df, lhh_000_no_shift_df, \
            lhh_001_shift_df, lhh_001_no_shift_df, \
                lhh_else_shift_df, lhh_else_no_shift_df, \
                    rhh_000_shift_df, rhh_000_no_shift_df, \
                        rhh_001_shift_df, rhh_001_no_shift_df, \
                            rhh_else_shift_df, rhh_else_no_shift_df

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'data' / 'processed_positioning'    
    output_dir.mkdir(parents=True, exist_ok=True)   

    keys = ['all_situations', 
            'lhh_000_shift', 'lhh_000_no_shift',
            'lhh_001_shift', 'lhh_001_no_shift',
            'lhh_else_shift', 'lhh_else_no_shift',
            'rhh_000_shift', 'rhh_000_no_shift',
            'rhh_001_shift', 'rhh_001_no_shift',
            'rhh_else_shift', 'rhh_else_no_shift',
            ]
    positioning_dfs = dict(zip(keys, load_positioning_data()))

    for name, df in positioning_dfs.items():
        df.to_csv(output_dir / f"{name}.csv", index=False)