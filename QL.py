#!/usr/bin/env python
#__*__ coding: utf-8 __*__

import random
import time

class Q_brain:

    def __init__(self, tabu_table = [[]], epsilon = 0.9, cold_factor = 0.9):
        self.Q_table = dict()
        self.state_stream = []
        self.epsilon = epsilon
        self.choice_stream = []
        self.cold_factor = cold_factor
        self.cold_stream = []
        self.punish_once = 1
        self.bonus_once = 1000
        self.punish_wandering = 50
        self.tabu_table = tabu_table
        self.wandering_thd = 200
        return

    def training(self, strt_point, terminal_point, train_times):
        for train_idx in range(train_times):
            # print(train_idx)
            cur_point = tuple(strt_point)
            self.state_stream.clear()
            self.choice_stream.clear()
            self.cold_stream.clear()
            t = 0
            while True:
                self.observe_state(cur_point)
                self.state_stream.append(self.cstate)
                if not self.Q_table.__contains__(self.cstate):
                    self.Q_table[self.cstate] = [0 for idx in range(len(self.cstate))]

                cumul_punish = self.Q_table[self.cstate]
                choice_idx = epsilon_greedy(self.epsilon, cumul_punish)
                self.choice_stream.append(choice_idx)
                # print(self.cstate)
                cur_point = self.cstate[choice_idx]

                for idx in range(len(self.cold_stream)) :
                    self.cold_stream[idx] = self.cold_stream[idx] * self.cold_factor
                self.cold_stream.append(1)
                # print(list(cur_point), end=' ')
                if list(cur_point) == terminal_point:
                    self.punishment(-self.bonus_once)
                    break
                else:
                    self.punishment(self.punish_once)

                t = t + 1
                if t >= self.wandering_thd:
                    self.punishment(self.punish_wandering)
                    break

            # print('')
        # for keys, values in self.Q_table.items():
        #     print(keys, values)
        # print(self.Q_table)
        # while True:
        #     1
        return

    def observe_state(self, cur_point):
        x, y = cur_point[0], cur_point[1]
        neighbour = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        self.cstate = ()
        for unit in neighbour:
            if list(unit) in self.tabu_table:
                continue
            elif unit[0] >= 10 or unit[0] < 0 or unit[1] >= 10 or unit[1] < 0:
                continue
            else:
                self.cstate = self.cstate + (unit,)

    def punishment(self, value):
        for t in range(len(self.choice_stream)):
            choice_idx = self.choice_stream[t]
            state_tmp = self.state_stream[t]
            # print(state_tmp)
            punish_tmp = self.Q_table[state_tmp]
            punish_tmp[choice_idx] = punish_tmp[choice_idx] + self.cold_stream[t] * value

    def make_choice(self, cur_point):
        self.observe_state(tuple(cur_point))
        # print(self.cstate)
        if not self.Q_table.__contains__(self.cstate):
            self.Q_table[self.cstate] = [0 for idx in len(self.cstate)]
        cumul_punish = self.Q_table[self.cstate]
        choice_idx = epsilon_greedy(1, cumul_punish)
        return list(self.cstate[choice_idx])

    def exist_route(self, strt_point, terminal_point):
        cur_point = strt_point
        self.route = [strt_point]
        t = 0
        while True:
            cur_point = self.make_choice(cur_point)
            # print(cur_point)
            # time.sleep(1)
            self.route.append(cur_point)
            if cur_point == terminal_point:
                return True
            elif t >= self.wandering_thd:
                return False


    def __route__(self):
        return self.route

    def clear_history(self):
        self.state_stream.clear()
        self.choice_stream.clear()
        self.cold_stream.clear()
        self.Q_table.clear()

def choice_classify(cumul_punish):
    min_punish = min(cumul_punish)
    best_choice_idx = []
    other_choice_idx = []
    # print(cumul_punish)
    for punish_idx in range(len(cumul_punish)):
        punish_tmp = cumul_punish[punish_idx]
        if punish_tmp == min_punish:
            best_choice_idx.append(punish_idx)
        else:
            other_choice_idx.append(punish_idx)
    return best_choice_idx, other_choice_idx

def epsilon_greedy(epsilon, cumul_punish):
    best_choice_idx, other_choice_idx = choice_classify(cumul_punish)
    randvalue = random.uniform(0,1)
    if randvalue < epsilon or len(other_choice_idx) == 0:
        return random.choice(best_choice_idx)
    else:
        return random.choice(other_choice_idx)
