def generate_monthly_report(expenses):
    summary = {}
    for exp in expenses:
        if exp.category not in summary:
            summary[exp.category] = 0
        summary[exp.category] += exp.amount
    return summary

def plot_ascii_bar_chart(data):
    for category, amount in data.items():
        bar_length = int(amount // 5)  # Adjust the divisor to change the scaling of the bar
        print(f"{category}: {'#' * bar_length}  ({amount})")
