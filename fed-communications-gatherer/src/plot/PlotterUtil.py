import matplotlib.pyplot as plt
import pandas as pd
from typing import List


class PlotterUtil:
    @staticmethod
    def plot_entity_sentiments_over_time(entity_sentiments_df: List[pd.DataFrame]):
        for df in entity_sentiments_df:
            df.iloc[:, 0].plot(grid=True, label=df.columns[0], legend=True)

        plt.xlabel("Time")
        plt.ylabel("Sentiment")
        plt.suptitle("Entity Sentiment over Time", fontsize=14)

        plt.xticks(rotation=60)
        plt.tight_layout()
        plt.show()
