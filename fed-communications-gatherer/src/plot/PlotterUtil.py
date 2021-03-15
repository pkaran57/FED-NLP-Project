import os

import matplotlib.pyplot as plt
import pandas as pd
from typing import List

from src.definitions import OUTPUT_DIR


class PlotterUtil:
    @staticmethod
    def plot_entity_sentiments_over_time(entity_sentiments_df: List[pd.DataFrame]):
        for df in entity_sentiments_df:
            df.iloc[:, 0].plot(grid=True, label=df.columns[0], legend=True)

        plt.xlabel("Time")
        plt.ylabel("Sentiment")
        plt.suptitle("Entity Sentiment over Time", fontsize=14)

        plt.xticks(rotation=60)
        plt.legend(
            title="Entity Names",
            loc="upper left",
            bbox_to_anchor=(1.05, 1),
            shadow=True,
        )
        plt.tight_layout()
        plt.savefig(
            os.path.join(OUTPUT_DIR, "Entity-Sentiment-Analysis.svg"),
            bbox_inches="tight",
        )
        plt.show()
