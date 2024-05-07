import pandas as pd
import os


class AutomaticProcess():
    def __init__(self):
        r"""
        drop_features: 어떠한 Case로 드랍되었는지를 딕셔너리로 나타내고,
                        경우에 해당하는 Key에 대해서 리스트에 append한다.

        """
        self.drop_features = {
            'col_upper': [],  # upper_threshold 이상인 column
            'col_lower': [],  # lower_threshold 미만인 column
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

            if missing_value_ratio == 0.0:
                # 이 컬럼엔 Missing Value가 없다.
                pass
            elif missing_value_ratio >= upper_threshold:
                # upper_threshold보다 결측치가 많으면,
                # 해당 컬럼 자체를 삭제한다.

                df.drop(labels=col, axis=1, inplace=True)  # columns
                self.drop_features['col_upper'].append(col)
            elif missing_value_ratio <= lower_threshold:
                # lower_threshold 미만이면, 해당 컬럼에 대해서
                # NaN인 레코드를 Drop한다.

                # 근데 우려되는 점이 컬럼의 순서에 따라 삭제되는
                # 레코드가 달라진다는 것이다.
                df.drop(labels=self._drop_rows(df[col].isna()),
                        axis=0, inplace=True)  # index
                self.drop_features['col_lower'].append(col)
            else:
                # lower_threshold 이상 upper_threshold 미만인 경우,
                # Data Imputation을 해야한다.
                pass

    def _drop_rows(self, bool_li: pd.DataFrame):
        ret_li = []
        for index, value in enumerate(bool_li):
            if value == True:
                ret_li.append(index)
            else:
                pass
        return ret_li


if __name__ == '__main__':
    ap = AutomaticProcess()
    print(os.getcwd())
    df = pd.read_csv(r'../data/AirQualityUCI.csv')

    print(df.info())
    ap.missing_value_process(df)
    print(df.info())
    print(ap.drop_features['col_upper'])
    print(ap.drop_features['col_lower'])
