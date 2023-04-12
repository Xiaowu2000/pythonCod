import random
import math
import re
import time
import copy

class Robot:
    def __init__(self, index,  name, x, y, abilities):
        self.name = name
        self.index = index
        self.x = x
        self.y = y
        self.abilities = abilities
        self.task_times = []

    def can_do(self, task):
        if 'husky' in self.name:
            if 'a' in task.point:
                return False
        else: 
            if 'g' in task.point:
                return False
        return task is not None and task.ability in self.abilities

    def do_task(self, task):
        if task != 'wait':
            distance = math.sqrt((float(self.x) - float(task.x)) ** 2 + (float(self.y) - float(task.y)) ** 2)
            self.x = task.x
            self.y = task.y
            self.task_times.append(distance)
        else:
            pass

    def get_time(self):
        return sum(self.task_times)

class Task:
    def __init__(self,index, point,  x, y, ability):
        self.index = index
        self.point = point
        self.x = x
        self.y = y
        self.ability = ability


class State:
    def __init__(self, robots, tasks):
        self.robots = robots
        self.tasks = tasks
        self.actions_list = []

    def get_actions(self,robots,tasks,actions_list,actions = []):
        i=0
        for j in range(len(tasks)):
            if tasks[j] is not None:
                if robots[i].can_do(tasks[j]):
                    actions.append((robots[i].index, tasks[j].index))
                    new_robots = robots.copy()
                    new_robots.remove(robots[i])
                    new_tasks = tasks.copy()
                    new_tasks.remove(tasks[j])
                    if len(new_robots) != 0 and len(new_tasks) != 0:
                        self.get_actions(new_robots,new_tasks,actions_list,actions)
                        actions.pop()
                    else:
                        actions_list.append(actions.copy())
                        actions.pop()
                        pass
                else:
                    new_robots = robots.copy()
                    new_robots.remove(robots[i])
                    new_tasks = tasks.copy()
                    if len(new_robots) != 0 and len(new_tasks) != 0:
                        self.get_actions(new_robots,new_tasks,actions_list,actions)
                        pass
                    else:
                        print('MISSION IMPOSIBLE')
                    

    def get_actions_list(self):
        actions_list = []
        self.get_actions(self.robots, self.tasks, actions_list)
        return actions_list

    def apply_action(self, action):
        robot_index, task_index = action
        robot = self.robots[robot_index]
        if task_index != 'wait':
            task = self.tasks[task_index]
            self.tasks[task_index] = None
        else:
            task = 'wait'
        robot.do_task(task)

    def is_terminal(self):
        return all(task is None for task in self.tasks)

    def get_reward(self):
        return max(robot.get_time() for robot in self.robots)

    def __str__(self):
        return f"State(robots={self.robots}, tasks={self.tasks})"

class Node:
    def __init__(self, state, parent, action, untried_actions = None):
        self.state = state
        self.parent = parent
        self.action = action
        self.reward = 0
        self.visits = 0
        self.children = []
        if untried_actions == None:
            self.untried_actions = state.get_actions_list()
        else:
            self.untried_actions = untried_actions


    def expand(self): 
        new_state = State(
            copy.deepcopy(self.state.robots),
            copy.deepcopy(self.state.tasks)
        )     
        # applied_actions = []
        # for i in range(len(self.untried_actions)):
        #     action = random.choice(self.untried_actions[i])
        #     if action[1] != 'wait':
        #         self.untried_actions[i].remove(action)
        #         for i in range(len(self.untried_actions)):
        #             for task in self.untried_actions[i]:
        #                 if task[1] == action[1]:
        #                     self.untried_actions[i].remove(task)
        #     new_state.apply_action(action)
        #     applied_actions.append(action)
        actions = random.choice(self.untried_actions)
        for action in actions:   
            new_state.apply_action(action)
        new_node = Node(new_state, self, actions)
        self.children.append(new_node)
        return new_node

    def is_fully_expanded(self):
        for i in range(len(self.untried_actions)):
            if len(self.untried_actions[i]) != 1:
                return False
        return True
    
    def reward(self):
        return self.state.get_reward()

    def is_terminal(self):
        return self.state.is_terminal()

    def select_child(self, exploration_constant=1.4):
        max_score = -1
        selected_child = None
        for child in self.children:
            score = (
                0 - child.visits / child.reward
                + 1.41 * math.sqrt(2 * math.log(self.visits) / child.visits)
            )
            # print ('===')
            # print(0 - child.reward / child.visits)
            # print(1.41 * math.sqrt(2 * math.log(self.visits) / child.visits))
            if score > max_score:
                max_score = score
                selected_child = child
        return selected_child

    def backpropagate(self, reward):
        self.visits += 1
        self.reward += reward
        if self.parent is not None:
            self.parent.backpropagate(reward)

class MCTS:
    def __init__(self, state):
        self.root = Node(state, None, None)

    def run(self, max_iterations):
        for _ in range(max_iterations):
            node = self.root
            while not node.is_terminal():
                if not node.is_fully_expanded():
                    child = node.expand()
                    node = child
                else:
                    node = node.select_child()
            reward = node.state.get_reward() 
            node.backpropagate(reward)

        best_child = self.root.children[0]
        for child in self.root.children:
            if child.visits > best_child.visits:
                best_child = child
        return best_child.action

# #生成随机任务和机器人
# tasks = []
# for i in range(10):
#     task = Task(round(random.uniform(0, 10), 2), round(random.uniform(0, 10), 2), random.randint(1, 3))
#     tasks.append(task)
 
# # # 保存为txt文件
# filenameA = './config/tasks.data'
# # with open(filename, 'wb') as file:
# #     pickle.dump(tasks, file)

# # 从txt文件读取
# with open(filenameA, 'rb') as file:
#     tasks = pickle.load(file)

# # 输出数组
# for task in tasks:
#     print(task.x, task.y, task.ability)

RobotSpawnMap = {}
Map = {}
mapData = 'Ros\scripts\mrga_tp\mrga_waypoints.txt'
with open(mapData, 'r') as file:
    for line in file:
        name = line[:line.index('[')]

        Robotname = ''
        RobotSpawnRegex = r"\{(.*?)\}"
        RobotSpawnmatches = re.search(RobotSpawnRegex, line)
        if RobotSpawnmatches:
            Robotname = RobotSpawnmatches.group(1)

        regex = r"\[(.*?)\]"
        matches = re.search(regex, line)
        if matches:
            XYindex = matches.group(1).split(', ')

        if Robotname:
            RobotSpawnMap[Robotname] = XYindex
        else:
            Map[name]= XYindex
    # robots = pickle.load(file)


# filenameB = './config/robots.data' #二进制数据
# # 从txt文件读取
# with open(filenameB, 'rb') as file:
#     robots = pickle.load(file)

robots = []
robotData = 'Ros\scripts\mrga_tp\mrga_robots.txt'
with open(robotData, 'r') as file:
    index = 0
    for line in file:
        name = line[:line.index('[')]
        regex = r"\[(.*?)\]"
        matches = re.search(regex, line)
        if matches:
            # 将匹配的子串拆分为数组
            ablities = matches.group(1).split(', ')
        robots.append(Robot(index, name, RobotSpawnMap[name][0],RobotSpawnMap[name][1], ablities))
        index+=1

tasks = []
taskssData = 'Ros\scripts\mrga_tp\mrga_goals.txt'
with open(taskssData, 'r') as file:
    index = 0
    for s in file:
        name = s[s.index(' ') + 1:s.index(')')]
        ability = s[s.index(')') + 1:].rstrip('\n')
        tasks.append(Task(index, name,Map[name][0],Map[name][1],ability))
        index+=1





# # 输出数组
# for robot in robots:
#     if robot.x == 1:
#         robot.abilities.append(2)
#     print(robot.x, robot.y, robot.abilities)

# with open(filenameB, 'wb') as file:
#     pickle.dump(robots, file)

start_time = time.time()
#初始化状态
state = State(robots, tasks)

#运行 MCTS 算法
mcts = MCTS(state)
best_action = mcts.run(12200)
end_time = time.time()

print('time: ', end_time-start_time)
print("Best action:", best_action)

