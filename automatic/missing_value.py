import pandas as pd
import os


class AutomaticProcess():
    def __init__(self):
        r"""
        drop_features: 어떠한 Case로 드랍되었는지를 딕셔너리로 나타내고,
                        경우에 해당하는 Key에 대해서 리스트에 append한다.

        """
        self.drop_features = {
            'drop_column': [],
            'drop_row': [],
        }

    def missing_value_process(self,
                              df: pd.DataFrame,
                              upper_threshold: float = 0.5,
                              lower_threshold: float = 0.1):
        r"""
        Args
            df: Missing Value를 처리할 DataFrame,
            lower_threshold: 해당 기준 값 이하는 
        """
        for col in df.columns:
            missing_value_ratio = df[col].isnull().sum()/len(df[col])
            if missing_value_ratio >= upper_threshold:
                df.drop(col, axis=1, inplace=True)
                self.drop_features['drop_column'].append(col)
            elif missing_value_ratio <= lower_threshold:
                df.drop(axis=0, inplace=True)
                self.drop_features['drop_row'].append(col)
            else:
                pass


if __name__ == '__main__':
    ap = AutomaticProcess()
    print(os.getcwd())
    df = pd.read_csv(r'../data/AirQualityUCI.csv')

    print(df.info())
    ap.missing_value_process(df)
    print(df.info())
