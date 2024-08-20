import matplotlib.pyplot as plt
from task_manager import TaskManager

class Analytics:
    def __init__(self):
        self.manager = TaskManager()

    def plot_task_distribution_bar(self):
        # Retrieve tasks from TaskManager
        tasks = self.manager.get_tasks()

        # Initialize priority counts
        priority_counts = {"High": 0, "Medium": 0, "Low": 0}

        # Count tasks by priority
        for task_id, task in tasks.items():
            priority = task.get('priority')
            if priority in priority_counts:
                priority_counts[priority] += 1

        # Debugging: Print the priority counts to ensure data is correct
        print("Priority Counts:", priority_counts)

        # Prepare data for plotting
        labels = list(priority_counts.keys())
        counts = list(priority_counts.values())

        # Plotting the bar chart with updated colors
        plt.figure(figsize=(8, 6))
        plt.bar(labels, counts, color=['#FF6F61', '#6B5B95', '#88B04B'], edgecolor='black')
        plt.xlabel('Priority', fontsize=14, fontweight='bold', color='#333333')
        plt.ylabel('Number of Tasks', fontsize=14, fontweight='bold', color='#333333')
        plt.title('Task Priority Distribution', fontsize=16, fontweight='bold', color='#333333')
        plt.xticks(fontsize=12, fontweight='medium', color='#333333')
        plt.yticks(fontsize=12, fontweight='medium', color='#333333')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Show the plot
        plt.show()
