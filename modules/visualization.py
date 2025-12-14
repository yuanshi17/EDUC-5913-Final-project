import matplotlib.pyplot as plt

def plot_line_chart(df, x, y, title="Line Chart"):
    fig, ax = plt.subplots(figsize=(10,4))
    for col in y:
        ax.plot(df[x], df[col], marker="o", label=col)
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.set_ylabel("Amount")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    return fig

def plot_bar_chart(df, x, y, title="Bar Chart"):
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(df[x], df[y])
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    plt.xticks(rotation=45)
    return fig