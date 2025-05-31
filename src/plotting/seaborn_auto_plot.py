import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def auto_plot_from_parquet(parquet_path: str, plot_title: str = "Auto Plot from Parquet"):
    if not os.path.exists(parquet_path):
        print(f"Файл не найден: {parquet_path}")
        return

    df = pd.read_parquet(parquet_path)
    if df.empty:
        print("Пустой DataFrame.")
        return

    # Определяем основные поля
    ohlc_cols = [col for col in df.columns if col.lower() in ["open", "high", "low", "close"]]
    volume_col = next((col for col in df.columns if col.lower() == "volume"), None)
    time_col = next((col for col in df.columns if col.lower() in ["timestamp", "datetime", "date", "time"]), None)

    # Остальные индикаторы
    exclude = set(ohlc_cols + ([volume_col] if volume_col else []) + ([time_col] if time_col else []))
    indicator_cols = [col for col in df.columns if col not in exclude]

    n_panels = 2 + len(indicator_cols)  # OHLC, Volume, индикаторы
    fig, axes = plt.subplots(n_panels, 1, sharex=True, figsize=(14, 3 * n_panels), gridspec_kw={'height_ratios': [2, 1] + [1]*len(indicator_cols)})
    if n_panels == 3:
        axes = [axes]  # если всего 3 панели, axes может быть не списком
    if not isinstance(axes, (list, np.ndarray)):
        axes = [axes]

    # OHLC график
    ax_ohlc = axes[0]
    if time_col:
        x = df[time_col]
    else:
        x = df.index
    for col in ohlc_cols:
        ax_ohlc.plot(x, df[col], label=col)
    ax_ohlc.set_ylabel("OHLC")
    ax_ohlc.legend()
    ax_ohlc.set_title(plot_title)

    # Volume
    ax_vol = axes[1]
    if volume_col:
        ax_vol.bar(x, df[volume_col], color='gray', alpha=0.5)
        ax_vol.set_ylabel("Volume")
    else:
        ax_vol.set_visible(False)

    # Индикаторы
    for i, col in enumerate(indicator_cols):
        ax = axes[2 + i]
        sns.lineplot(x=x, y=df[col], ax=ax)
        ax.set_ylabel(col)
        ax.set_title(col)

    plt.tight_layout()
    plt.show()

