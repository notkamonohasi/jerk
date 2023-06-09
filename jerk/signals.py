from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .simulator import Simulator

from typing import Union
from enum import Enum
import math

class Aspect(Enum) : 
    BLUE = 0 
    YELLOW_TO_RED = 1
    RED = 2
    YELLOW_TO_BLUE = 3

def convert_index_into_aspect(index : int) -> Aspect : 
    assert index <= 3
    if index == 0 : 
        return Aspect.BLUE
    elif index == 1 : 
        return Aspect.YELLOW_TO_RED
    elif index == 2 : 
        return Aspect.RED
    elif index == 3 : 
        return Aspect.YELLOW_TO_BLUE


class Signal : 
    def __init__(self, init_data : dict[str, any], simulator : Simulator) -> None:
        self.number = init_data["number"]
        self.first_time = init_data["first_time"]   # 時刻0での位相[s]
        self.interval_list : list[int] = init_data["interval_list"]   # 青 -> 黄 -> 赤 -> 黄

        self.simulator = simulator

        self.cycle = int(sum(self.interval_list))

        assert len(self.interval_list) == 4

        self.update()   # 初期化しておく必要がある
    

    def update(self) : 
        # 剰余の計算が入るため、秒からミリ秒に変えて計算する
        pos_time = self.simulator.get_second()   # s
        amari = int((self.first_time + pos_time) * 1000) % int(self.cycle * 1000) 

        self.signal_cos = math.cos(amari / self.cycle)
        self.signal_sin = math.sin(amari / self.cycle)

        pos_sum = 0
        for index in range(len(self.interval_list)) : 
            pos_sum += self.interval_list[index] * 1000
            if pos_sum > amari : 
                self.signal_aspect : Aspect = convert_index_into_aspect(index)
                self.remain_time = (pos_sum - amari) / 1000   # msに戻す
                self.remain_time = round(self.remain_time, 3)   # 表示を綺麗にするため
                return 
            

    def get_signal_state(self) -> dict[str, Union(Aspect, float)] : 
        return {
            "aspect" : self.signal_aspect, 
            "remain_time" : self.remain_time, 
            "signal_cos" : self.signal_cos, 
            "signal_sin" : self.signal_sin
        }

        




