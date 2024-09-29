def generate_monthly_report(expenses):
    # Summarize expenses by category
    summary = {}
    for exp in expenses:
        if exp.category not in summary:
            summary[exp.category] = 0
        summary[exp.category] += exp.amount
    return summary

def plot_ascii_bar_chart(data):
    # Plot the summary using ASCII bar charts
    for category, amount in data.items():
        print(f"{category}: {'#' * int(amount // 10)}")
