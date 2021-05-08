from typing import Optional

from datetime import datetime
from threading import Timer

import math
import ui
import sound


class TimerController(object):
    # Views
    view: ui.View
    timer_display: ui.Label
    button_green: ui.Button
    button_red: ui.Button    
    
    # View Model
    _timer_value: float = 0
    """Timer Value in seconds"""
    
    _timer_start_value: float = 0
    """The initial value of timer """
    
    _timer_running: bool = 0
    _timer_run_time: Optional[datetime] = None
    
    # Control
    _timer: Optional[Timer] = None
    
    # Event Handlers
    def on_button_green(self, sender: ui.Button):
        if self._timer_running:
            self._timer_pause()
        else:
            self._timer_start()

    def on_button_red(self, sender: ui.Button):
        if self._timer_running:
            self._timer_stop();
        else:
            self._timer_reset()
            
    def on_button_add_01(self, sender: ui.Button):
        self._timer_add(60)

    def on_button_add_03(self, sender: ui.Button):
        self._timer_add(3 * 60)

    def on_button_add_05(self, sender: ui.Button):
        self._timer_add(5 * 60)

    def on_button_add_07(self, sender: ui.Button):
        self._timer_add(7 * 60)

    def on_button_add_11(self, sender: ui.Button):
        self._timer_add(11 * 60)

    def on_button_add_13(self, sender: ui.Button):
        self._timer_add(13 * 60)            
                        
    # Others
    def __init__(self):
        self.view = ui.load_view()
        self.button_green = self.view['button_green']
        self.button_red = self.view['button_red']
        self.timer_display = self.view['timer_display']
                
    def show(self):    
        self.view.present('sheet')
        self._update_display()
        
    def _update_display(self):
        time_remaining = self._calc_time_remaining()
        minute_portion = math.floor(time_remaining / 60)
        seconds_portion = math.floor(time_remaining - minute_portion*60)
        display_text = f'{minute_portion:02}:{seconds_portion:02}'
        self.timer_display.text = display_text
        
        if self._timer_running:
            self.button_green.title = "Pause"
            self.button_red.title = "Stop"
        else:
            self.button_green.title = "Start"
            self.button_red.title = "Reset"
        
        self.button_green.enabled = time_remaining > 0
            
    def _calc_time_remaining(self) -> float:
        if self._timer_run_time is not None:
            delta_time = datetime.utcnow() - self._timer_run_time
            return self._timer_value - delta_time.total_seconds()
        else:
            return self._timer_value
                        
    def _timer_add(self, time_value: float):
        self._timer_value += time_value
        self._timer_start_value = self._timer_value
        self._update_display()
        sound.play_effect('8ve:8ve-beep-hightone')
            
    def _timer_start(self):
        self._timer_run_time = datetime.utcnow()
        self._timer_running = True
        self._update_display()
        self._timer_schedule()
        sound.play_effect('digital:ThreeTone2')

    def _timer_stop(self):
        self._timer_unschedule()
        self._timer_running = False
        self._timer_value = self._timer_start_value
        self._timer_run_time = None        
        self._update_display()
        sound.play_effect('digital:Zap2')

    def _timer_pause(self):
        self._timer_unschedule()
        self._timer_running = False
        self._timer_value = self._calc_time_remaining()
        self._timer_run_time = None
        self._update_display()
        sound.play_effect('digital:TwoTone2')        

    def _timer_end(self):
        self._timer_unschedule()
        self._timer_running = False
        self._timer_value = 0
        self._timer_run_time = None
        self._update_display()
        sound.play_effect('arcade:Powerup_3')

    def _timer_reset(self):
        self._timer_value = 0
        self._timer_run_time = None
        self._update_display()
        sound.play_effect('digital:PhaserDown1')
            
    def _on_timer_update(self):
        self._update_display()
        time_remaining = self._calc_time_remaining()
        if time_remaining  <= 0:
            self._timer_end()
        if self._timer_running:
            self._timer_schedule()
        
    def _timer_schedule(self):
        self._timer_unschedule()
        t = Timer(0.5, self._on_timer_update)
        self._timer = t
        t.start()
        
    def _timer_unschedule(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        
if __name__=='__main__':
    tc = TimerController()
    tc.show()
