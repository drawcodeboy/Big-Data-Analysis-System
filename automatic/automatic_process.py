import pandas as pd
import os
import sys


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
                              lower_threshold: float = 0.1,
                              imputation_method: str = 'mean'):

        # custom의 경우는 Column마다 imputation을 다르게 주려는 용도 (아직 구현 X)
        # custom은 쓰려면, 컬럼에 대응하는 메서드를 string으로 받는 딕셔너리도 input으로 받게 하자.
        _imputation_li = ['mean', 'median', 'mode', 'custom']  # 다른 것도 더 추가해야 함
        assert imputation_method in _imputation_li, 'This is NOT method for imputation!'

        for col in df.columns:
            missing_value_ratio = df[col].isnull().sum()/len(df[col])

            if missing_value_ratio == 0.0:
                # 이 컬럼엔 Missing Value가 없다.
                pass
            elif missing_value_ratio >= upper_threshold:
                # upper_threshold보다 결측치가 많으면,
                # 해당 컬럼 자체를 삭제한다.

                df = df.drop(labels=col, axis=1)  # columns
                self.drop_features['col_upper'].append(col)
            elif missing_value_ratio <= lower_threshold:
                # lower_threshold 미만이면, 해당 컬럼에 대해서
                # NaN인 레코드를 Drop한다.

                # 근데 우려되는 점이 컬럼의 순서에 따라 삭제되는
                # 레코드가 달라진다는 것이다.
                df = df.drop(labels=self._drop_rows(df[col].isna()),
                             axis=0)  # index
                self.drop_features['col_lower'].append(col)
            else:
                # lower_threshold 이상 upper_threshold 미만인 경우,
                # Data Imputation을 해야한다.
                if imputation_method == 'mean':
                    mean = df[col].mean(axis=1, skipna=True)
                    df = df[col].fillna(mean)
                elif imputation_method == 'median':
                    median = df[col].median(axis=1, skipna=True)
                    df = df[col].fillna(median)
                elif imputation_method == 'mode':
                    mode = df[col].mode(axis=1, dropna=True)
                    df = df[col].fillna(mode)
                elif imputation_method == 'custom':
                    print('Not Yet')
                else:
                    pass
        return df

    def _drop_rows(self, bool_li: pd.DataFrame):
        ret_li = []
        for index, value in enumerate(bool_li):
            if value == True:
                ret_li.append(index)
            else:
                pass
        return ret_li

    def outlier_process(self,
                        df: pd.DataFrame,
                        criterion: str = 'quantile'):
        r'''
        표준화 혹은 정규화가 되어있는 것을 추천,
        또한 str이 있는 경우에 오류 raise
        '''
        _criterion_li = ['quantile']
        assert criterion in _criterion_li, 'This is NOT criterion for detect OUTLIER!'

        for col in df.columns:
            if df[col].dtype == 'object':
                raise TypeError(
                    f'{col}컬럼에 대해 사분위수를 구할 때, object 타입을 지원하지 않습니다.')

        for col in df.columns:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1

            boundary = 1.5 * iqr

            index1 = df[df[col] > (q3 + boundary)].index
            index2 = df[df[col] < (q1 - boundary)].index

            df = df.drop(index1)
            df = df.drop(index2)

        return df


if __name__ == '__main__':
    ap = AutomaticProcess()
    print(os.getcwd())
    df = pd.read_csv(r'../../data/AirQualityUCI.csv')

    print('\n[NONE]\n')
    print(df.info())
    df = ap.missing_value_process(df)
    print('\n[MISSING VALUE]\n')
    print(df.info())
    df = df.drop(labels=['Date', 'Time'], axis=1)
    df = ap.outlier_process(df)
    print('\n[OUTLIER]\n')
    print(df.info())
