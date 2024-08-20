from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from task_manager import TaskManager
from analytics import Analytics
from voice_input import VoiceInput

class TaskManagerApp(App):
    def build(self):
        self.task_manager = TaskManager()
        self.analytics = Analytics()
        self.voice_input = VoiceInput()

        self.layout = BoxLayout(orientation='vertical', padding=10)

        # Add Task Section
        self.task_input = TextInput(hint_text='Enter task title', multiline=False)
        self.priority_input = TextInput(hint_text='Enter task priority', multiline=False)
        add_button = Button(text="Add Task", on_press=self.add_task)
        self.layout.add_widget(self.task_input)
        self.layout.add_widget(self.priority_input)
        self.layout.add_widget(add_button)

        # Tasks List Section
        self.task_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 300))
        self.scroll_view.add_widget(self.task_list)
        self.layout.add_widget(self.scroll_view)

        # Message Label
        self.message_label = Label()
        self.layout.add_widget(self.message_label)

        # Analytics and Voice Input Buttons
        analytics_button = Button(text="Show Analytics", on_press=self.show_analytics)
        voice_input_button = Button(text="Add Task via Voice", on_press=self.add_task_by_voice)
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
            task_label = Label(text=task_text, size_hint_y=None, height=40)
            delete_button = Button(text="Delete", size_hint_y=None, height=40)
            delete_button.bind(on_press=lambda x, task_id=task_id: self.delete_task(task_id))
            complete_button = Button(text="Complete", size_hint_y=None, height=40)
            complete_button.bind(on_press=lambda x, task_id=task_id: self.complete_task(task_id))
            task_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            task_box.add_widget(task_label)
            task_box.add_widget(complete_button)
            task_box.add_widget(delete_button)
            self.task_list.add_widget(task_box)

    def add_task(self, instance):
        title = self.task_input.text
        priority = self.priority_input.text
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
        analytics_data = self.analytics.get_task_distribution()  # Assuming this returns some analytics data
        popup_content = BoxLayout(orientation='vertical')
        for key, value in analytics_data.items():
            popup_content.add_widget(Label(text=f"{key}: {value}"))
        close_button = Button(text="Close", on_press=lambda x: self.dismiss_popup())
        popup_content.add_widget(close_button)
        self.popup = Popup(title="Task Analytics", content=popup_content, size_hint=(0.9, 0.9))
        self.popup.open()

    def dismiss_popup(self):
        if hasattr(self, 'popup'):
            self.popup.dismiss()

    def add_task_by_voice(self, instance):
        task = self.voice_input.listen()
        if task:
            priority = self.priority_input.text
            self.task_manager.add_task(task, priority=priority)
            self.message_label.text = 'Task added via voice input successfully!'
            self.refresh_task_list()
        else:
            self.message_label.text = 'No task recognized. Please try again.'

if __name__ == "__main__":
    TaskManagerApp().run()
