from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.metrics import dp
import matplotlib.pyplot as plt
from task_manager import TaskManager
from analytics import Analytics
from voice_input import VoiceInput

# Set the background color of the app window
Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light grey background

class PastelButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.8, 0.87, 0.91, 1)  # Light pastel blue
        self.color = (0.2, 0.2, 0.2, 1)  # Dark grey text
        self.font_size = '16sp'
        self.size_hint_y = None
        self.height = dp(50)
        self.bold = True

class PastelTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.94, 0.94, 0.98, 1)  # Very light pastel purple
        self.foreground_color = (0.3, 0.3, 0.3, 1)  # Dark grey text
        self.font_size = '16sp'
        self.padding_y = (10, 10)
        self.size_hint_y = None
        self.height = dp(40)

class PastelLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (0.3, 0.3, 0.3, 1)  # Dark grey text
        self.font_size = '16sp'

class TaskManagerApp(App):
    def build(self):
        self.task_manager = TaskManager()
        self.analytics = Analytics()
        self.voice_input = VoiceInput()

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Add Task Section
        input_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=dp(50))
        self.task_input = PastelTextInput(hint_text='Enter task title')
        self.priority_input = PastelTextInput(hint_text='Enter task priority')
        input_layout.add_widget(self.task_input)
        input_layout.add_widget(self.priority_input)
        self.layout.add_widget(input_layout)

        add_button = PastelButton(text="Add Task", on_press=self.add_task)
        self.layout.add_widget(add_button)

        # Tasks List Section
        self.task_list = GridLayout(cols=1, spacing=15, size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 200))
        self.scroll_view.add_widget(self.task_list)
        self.layout.add_widget(self.scroll_view)

        # Message Label
        self.message_label = PastelLabel()
        self.layout.add_widget(self.message_label)

        # Analytics and Voice Input Buttons
        analytics_button = PastelButton(text="Show Analytics", on_press=self.show_analytics, background_color=(0.65, 0.89, 0.89, 1))
        voice_input_button = PastelButton(text="Add Task via Voice", on_press=self.add_task_by_voice)
        self.layout.add_widget(analytics_button)
        self.layout.add_widget(voice_input_button)

        return self.layout

    def refresh_task_list(self):
        self.task_list.clear_widgets()
        tasks = self.task_manager.get_tasks()
        for task_id, task in tasks.items():
            task_text = f"{task_id}: {task['title']} (Priority: {task['priority']})"
            if task['completed']:
                task_text += " - Completed"
            task_label = PastelLabel(text=task_text, size_hint_x=0.6, height=dp(40))
            
            task_buttons = BoxLayout(orientation='horizontal', size_hint_x=0.4, spacing=5)
            delete_button = PastelButton(text="Delete", size_hint_y=None, height=dp(40))
            delete_button.bind(on_press=lambda x, task_id=task_id: self.delete_task(task_id))
            complete_button = PastelButton(text="Complete", size_hint_y=None, height=dp(40))
            complete_button.bind(on_press=lambda x, task_id=task_id: self.complete_task(task_id))
            
            task_buttons.add_widget(complete_button)
            task_buttons.add_widget(delete_button)
            
            task_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=10)
            task_box.add_widget(task_label)
            task_box.add_widget(task_buttons)
            self.task_list.add_widget(task_box)

    def add_task(self, instance):
        title = self.task_input.text
        priority = self.priority_input.text.capitalize()  # Ensure priority is capitalized
        if title:
            self.task_manager.add_task(title, priority=priority)
            self.message_label.text = 'Task added successfully!'
            self.task_input.text = ""
            self.priority_input.text = ""
            self.refresh_task_list()
        else:
            self.message_label.text = 'Task title cannot be empty.'

    def delete_task(self, task_id):
        self.task_manager.delete_task(task_id)
        self.message_label.text = f'Task {task_id} deleted successfully!'
        self.refresh_task_list()

    def complete_task(self, task_id):
        self.task_manager.complete_task(task_id)
        self.message_label.text = f'Task {task_id} marked as completed!'
        self.refresh_task_list()

    def show_analytics(self, instance):
        self.analytics.plot_task_distribution_bar()

    def add_task_by_voice(self, instance):
        task = self.voice_input.listen()
        if task:
            priority = self.priority_input.text.capitalize()  # Ensure priority is capitalized
            self.task_manager.add_task(task, priority=priority)
            self.message_label.text = 'Task added via voice input successfully!'
            self.refresh_task_list()
        else:
            self.message_label.text = 'No task recognized. Please try again.'

if __name__ == "__main__":
    TaskManagerApp().run()
