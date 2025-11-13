from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from datetime import datetime
import json
import os

class ColoredLabel(Label):
    def __init__(self, bg_color=None, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color or (1, 1, 1, 1)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
    def update_rect(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            Rectangle(pos=self.pos, size=self.size)

class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.298, 0.686, 0.314, 1)  # #4caf50
        self.color = (1, 1, 1, 1)
        self.font_size = dp(16)
        self.size_hint_y = None
        self.height = dp(50)
        self.bold = True

class PrimaryButton(StyledButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.298, 0.686, 0.314, 1)  # #4caf50

class WarningButton(StyledButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (1, 0.596, 0, 1)  # #ff9800

class DangerButton(StyledButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.957, 0.263, 0.212, 1)  # #f44336

class RangeButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.298, 0.686, 0.314, 1)
        self.color = (1, 1, 1, 1)
        self.font_size = dp(14)
        self.size_hint_y = None
        self.height = dp(40)

class MainMenu(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = dp(40)
        self.spacing = dp(15)
        
        # Title
        title = ColoredLabel(
            text="Church Security System",
            font_size=dp(28),
            bold=True,
            color=(0.18, 0.49, 0.196, 1),  # #2e7d32
            size_hint_y=None,
            height=dp(60)
        )
        self.add_widget(title)
        
        # Description
        description = ColoredLabel(
            text="This system is designed to enhance the attendance tracking of cars coming into the church and leaving. It includes features such as car detection, license plate recognition, and logging of entry and exit times.",
            font_size=dp(14),
            color=(0.22, 0.557, 0.235, 1),  # #388e3c
            text_size=(Window.width - dp(80), None),
            size_hint_y=None,
            height=dp(80)
        )
        self.add_widget(description)
        
        # Buttons
        buttons_data = [
            ("Start Security System", PrimaryButton, self.app.start_security_system),
            ("Settings", PrimaryButton, self.app.open_settings),
            ("View Car Data", PrimaryButton, self.app.view_car_data),
            ("Exit Car", WarningButton, self.app.exit_car),
            ("Save Data to File", PrimaryButton, self.app.save_to_file),
            ("Exit", DangerButton, self.app.exit_app)
        ]
        
        for text, btn_class, callback in buttons_data:
            btn = btn_class(text=text)
            btn.bind(on_press=callback)
            self.add_widget(btn)

class RangeSelectionModal(ModalView):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = False
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Title
        title = ColoredLabel(
            text="Select Expected Number of Cars",
            font_size=dp(20),
            bold=True,
            color=(0.18, 0.49, 0.196, 1),
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(title)
        
        # Scrollable grid for ranges
        scroll = ScrollView()
        grid = GridLayout(cols=3, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        ranges = ["1-40", "1-50", "1-60", "1-70", "1-80", "1-90", 
                "1-100", "1-110", "1-120", "1-130", "1-140", 
                "1-150", "1-160", "1-170", "1-180", "1-190", "1-200"]
        
        for range_str in ranges:
            btn = RangeButton(text=range_str)
            btn.bind(on_press=lambda instance, r=range_str: self.select_range(r))
            grid.add_widget(btn)
        
        scroll.add_widget(grid)
        layout.add_widget(scroll)
        
        # Close button
        close_btn = DangerButton(text="Close")
        close_btn.bind(on_press=self.dismiss)
        layout.add_widget(close_btn)
        
        self.add_widget(layout)
    
    def select_range(self, range_str):
        self.dismiss()
        self.app.input_license_plates(range_str)

class LicensePlateInputModal(ModalView):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.size_hint = (0.95, 0.95)
        self.auto_dismiss = False
        self.entries = []
        
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Title
        self.title_label = ColoredLabel(
            text="",
            font_size=dp(20),
            bold=True,
            color=(0.18, 0.49, 0.196, 1),
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(self.title_label)
        
        # Scroll to Top button
        scroll_top_btn = WarningButton(text="Scroll to Top (Car 1)")
        scroll_top_btn.bind(on_press=lambda x: setattr(self.scroll_view, 'scroll_y', 1.0))
        main_layout.add_widget(scroll_top_btn)
        
        # Create scroll view
        self.scroll_view = ScrollView(do_scroll_x=False)
        self.input_layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
        self.scroll_view.add_widget(self.input_layout)
        main_layout.add_widget(self.scroll_view)
        
        # Buttons layout
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
        
        save_btn = PrimaryButton(text="Save All")
        save_btn.bind(on_press=self.save_data)
        
        cancel_btn = DangerButton(text="Cancel")
        cancel_btn.bind(on_press=self.dismiss)
        
        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(cancel_btn)
        main_layout.add_widget(btn_layout)
        
        self.add_widget(main_layout)
    
    def setup_inputs(self, car_range):
        self.car_range = car_range
        self.entries.clear()
        self.input_layout.clear_widgets()
        
        # Update title
        self.title_label.text = f"Input License Plates - {car_range} cars"
        
        min_cars, max_cars = map(int, car_range.split('-'))
        
        # Calculate total height needed for all input rows
        row_height = dp(50)
        total_height = (max_cars - min_cars + 1) * row_height
        
        # Set the height of the input layout to enable scrolling
        self.input_layout.height = total_height
        
        # Add cars in the correct order (1, 2, 3, ...)
        for i in range(min_cars, max_cars + 1):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            
            label = ColoredLabel(
                text=f"Car {i}:",
                size_hint_x=0.3,
                color=(0.106, 0.369, 0.125, 1),
                halign='left',
                text_size=(dp(100), None)
            )
            
            entry = TextInput(
                hint_text=f"Enter plate for car {i}",
                multiline=False,
                size_hint_x=0.7,
                background_color=(0.784, 0.902, 0.788, 1),
                foreground_color=(0.106, 0.369, 0.125, 1),
                padding=[dp(10), dp(10)],
                font_size=dp(14)
            )
            
            row.add_widget(label)
            row.add_widget(entry)
            self.input_layout.add_widget(row)
            self.entries.append((i, entry))
        
        # Try to scroll to top automatically
        self._auto_scroll_attempt()
    
    def _auto_scroll_attempt(self):
        """Try to scroll automatically, but user can use button if it fails"""
        self.scroll_view.scroll_y = 1.0
        Clock.schedule_once(lambda dt: setattr(self.scroll_view, 'scroll_y', 1.0), 0.5)
        Clock.schedule_once(lambda dt: setattr(self.scroll_view, 'scroll_y', 1.0), 1.0)
    
    def save_data(self, instance):
        for car_num, entry in self.entries:
            plate = entry.text.strip()
            if plate:
                self.app.car_data[self.car_range][f"car_{car_num}"] = {
                    "plate": plate,
                    "entry_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "exit_time": None
                }
        
        self.dismiss()
        self.app.show_summary()
                                        
class SummaryModal(ModalView):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = True
        
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        self.add_widget(self.layout)
    
    def show_summary(self, car_range):
        self.layout.clear_widgets()
        
        # Title
        title = ColoredLabel(
            text=f"Data for {car_range} cars",
            font_size=dp(20),
            bold=True,
            color=(0.18, 0.49, 0.196, 1),
            size_hint_y=None,
            height=dp(40)
        )
        self.layout.add_widget(title)
        
        # Data display
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        data = self.app.car_data.get(car_range, {})
        for car_id, info in data.items():
            entry_text = f"{car_id}: {info['plate']}\nEntry: {info['entry_time']}"
            entry_label = ColoredLabel(
                text=entry_text,
                text_size=(Window.width * 0.7, None),
                size_hint_y=None,
                height=dp(60),
                color=(0.106, 0.369, 0.125, 1),
                bg_color=(0.784, 0.902, 0.788, 1)  # Light green background
            )
            content.add_widget(entry_label)
        
        scroll.add_widget(content)
        self.layout.add_widget(scroll)
        
        # Close button
        close_btn = PrimaryButton(text="Close")
        close_btn.bind(on_press=self.dismiss)
        self.layout.add_widget(close_btn)
        
        self.open()
        

class CarDataModal(ModalView):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.size_hint = (0.9, 0.9)
        self.auto_dismiss = True
        
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        self.add_widget(self.layout)
    
    def show_data(self):
        self.layout.clear_widgets()
        
        # Title
        title = ColoredLabel(
            text="All Car Data",
            font_size=dp(20),
            bold=True,
            color=(0.18, 0.49, 0.196, 1),
            size_hint_y=None,
            height=dp(40)
        )
        self.layout.add_widget(title)
        
        if not self.app.car_data:
            no_data = ColoredLabel(
                text="No car data available yet.",
                font_size=dp(16),
                color=(0.18, 0.49, 0.196, 1)
            )
            self.layout.add_widget(no_data)
            return
        
        # Tabbed panel for different ranges
        tabs = TabbedPanel(do_default_tab=False)
        
        for range_str, cars in self.app.car_data.items():
            tab = TabbedPanelItem(text=range_str)
            tab.background_color = (0.298, 0.686, 0.314, 1)  # Green tabs
            
            # Scrollable content for this range
            scroll = ScrollView()
            content = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
            content.bind(minimum_height=content.setter('height'))
            
            for car_id, info in cars.items():
                entry_text = (f"{car_id}: {info['plate']}\n"
                            f"Entry: {info['entry_time']}\n"
                            f"Exit: {info.get('exit_time', 'Not recorded')}")
                
                entry_label = ColoredLabel(
                    text=entry_text,
                    text_size=(Window.width * 0.8, None),
                    size_hint_y=None,
                    height=dp(80),
                    color=(0.106, 0.369, 0.125, 1),
                    bg_color=(0.784, 0.902, 0.788, 1)  # Light green background
                )
                content.add_widget(entry_label)
            
            scroll.add_widget(content)
            tab.add_widget(scroll)
            tabs.add_widget(tab)
        
        self.layout.add_widget(tabs)
        
        # Close button
        close_btn = PrimaryButton(text="Close")
        close_btn.bind(on_press=self.dismiss)
        self.layout.add_widget(close_btn)
        
        self.open()

class ExitCarModal(ModalView):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = False
        self.selected_car = None
        
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        self.add_widget(self.layout)
    
    def show_available_cars(self):
        self.layout.clear_widgets()
        self.selected_car = None
        
        # Title
        title = ColoredLabel(
            text="Select a Car to Exit",
            font_size=dp(20),
            bold=True,
            color=(0.18, 0.49, 0.196, 1),
            size_hint_y=None,
            height=dp(40)
        )
        self.layout.add_widget(title)
        
        # Get available cars
        available_cars = []
        for range_str, cars in self.app.car_data.items():
            for car_id, car_info in cars.items():
                if car_info.get('exit_time') is None:
                    available_cars.append((range_str, car_id, car_info))
        
        if not available_cars:
            no_cars = ColoredLabel(
                text="No cars currently in the system.",
                font_size=dp(16),
                color=(0.18, 0.49, 0.196, 1)
            )
            self.layout.add_widget(no_cars)
        else:
            # Scrollable list of cars
            scroll = ScrollView()
            car_list = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
            car_list.bind(minimum_height=car_list.setter('height'))
            
            for range_str, car_id, car_info in available_cars:
                btn = PrimaryButton(
                    text=f"{range_str} - {car_id}: {car_info['plate']}",
                    size_hint_y=None,
                    height=dp(60)
                )
                btn.car_data = (range_str, car_id, car_info)
                btn.bind(on_press=self.select_car)
                car_list.add_widget(btn)
            
            scroll.add_widget(car_list)
            self.layout.add_widget(scroll)
            
            # Exit button
            self.exit_btn = WarningButton(text="Mark as Exited")
            self.exit_btn.bind(on_press=self.process_exit)
            self.exit_btn.disabled = True
            self.layout.add_widget(self.exit_btn)
        
        # Close button
        close_btn = DangerButton(text="Close")
        close_btn.bind(on_press=self.dismiss)
        self.layout.add_widget(close_btn)
        
        self.open()
    
    def select_car(self, instance):
        # Reset all buttons
        for child in self.layout.children:
            if hasattr(child, 'children'):
                for grandchild in child.children:
                    if hasattr(grandchild, 'car_data'):
                        for btn in grandchild.children:
                            if hasattr(btn, 'car_data'):
                                btn.background_color = (0.298, 0.686, 0.314, 1)  # Default green
        
        # Highlight selected button
        instance.background_color = (0.18, 0.49, 0.196, 1)  # Darker green
        self.selected_car = instance.car_data
        self.exit_btn.disabled = False
    
    def process_exit(self, instance):
        if not self.selected_car:
            return
        
        range_str, car_id, car_info = self.selected_car
        
        # Record exit time
        self.app.car_data[range_str][car_id]['exit_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Show success message
        success_label = ColoredLabel(
            text=f"Car {car_id} has been marked as exited!",
            color=(0.18, 0.49, 0.196, 1),
            font_size=dp(16),
            size_hint_y=None,
            height=dp(40)
        )
        self.layout.add_widget(success_label)
        
        # Refresh after a delay
        Clock.schedule_once(lambda dt: self.show_available_cars(), 2)

class ChurchSecurityApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.car_data = {}
        self.current_range = ""
        
        # Initialize modals
        self.range_modal = RangeSelectionModal(self)
        self.input_modal = LicensePlateInputModal(self)
        self.summary_modal = SummaryModal(self)
        self.data_modal = CarDataModal(self)
        self.exit_modal = ExitCarModal(self)
    
    def build(self):
        # Set window background color
        Window.clearcolor = (0.91, 0.96, 0.91, 1)  # #e8f5e9
        
        return MainMenu(self)
    
    def start_security_system(self, instance=None):
        self.range_modal.open()
    
    def input_license_plates(self, car_range):
        self.current_range = car_range
        self.car_data[car_range] = {}
        self.input_modal.setup_inputs(car_range)
        self.input_modal.open()
    
    def show_summary(self):
        self.summary_modal.show_summary(self.current_range)
    
    def view_car_data(self, instance=None):
        self.data_modal.show_data()
    
    def exit_car(self, instance=None):
        self.exit_modal.show_available_cars()
    
    def open_settings(self, instance=None):
        # Simple settings implementation
        from kivy.uix.popup import Popup
        
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        content.add_widget(ColoredLabel(text="Settings", font_size=dp(20)))
        content.add_widget(ColoredLabel(text="Settings feature would go here"))
        
        close_btn = PrimaryButton(text="Close")
        popup = Popup(title='Settings', content=content, size_hint=(0.6, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()
    
    def save_to_file(self, instance=None):
        if not self.car_data:
            self.show_message("No data to save.")
            return
        
        try:
            filename = "car_data.json"
            with open(filename, 'w') as f:
                json.dump(self.car_data, f, indent=2)
            self.show_message(f"Data saved to {filename}")
        except Exception as e:
            self.show_message(f"Error saving file: {str(e)}")
    
    def exit_app(self, instance=None):
        self.stop()
    
    def show_message(self, message):
        from kivy.uix.popup import Popup
        
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        content.add_widget(ColoredLabel(text=message))
        
        close_btn = PrimaryButton(text="OK")
        popup = Popup(title='Information', content=content, size_hint=(0.6, 0.3))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()

if __name__ == '__main__':
    ChurchSecurityApp().run()