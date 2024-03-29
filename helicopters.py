import numpy as np
import cv2

def Generate(width, height, count):
    # method to generate random targets
    targets = []
    for i in range(count):
        position_x = np.random.randint(width)
        position_y = np.random.randint(height - 165) + 160
        targets.append((position_x, position_y))
    return targets

def Initialize(count):
    # shuffle initial solution
    solution = np.arange(count)
    np.random.shuffle(solution)
    return solution

def Evaluate(targets, solution):
    # fitness function - sum of all distances
    distance = 0
    for i in range(len(targets)):
        index_a = solution[i]
        index_b = solution[i - 1]
        dst= get_distance(targets[index_a], targets[index_b])
        distance += dst
    return distance

def get_distance(target1, target2):
    # distance of two points
    delta_x = target1[0] - target2[0]
    delta_y = target1[1] - target2[1]
    return (delta_x ** 2 + delta_y ** 2) ** 0.5

def Modify(current):
    # randomly swap two positions in current solution 
    new = current.copy()
    if len(new) == 1: 
        return new 
    index_a = np.random.randint(len(current))
    index_b = np.random.randint(len(current))
    while index_b == index_a:
        index_b = np.random.randint(len(current))
    new[index_a], new[index_b] = new[index_b], new[index_a]
    return new

def ModifyTargets(targets_a, targets_b, helicopters): 
    # randomly assign one target to different helicopter 
    new_a = targets_a.copy()
    new_b = targets_b.copy()
    random_number = np.random.uniform()
    if (random_number >= 0.5 and len(new_a) > 0) or (random_number < 0.5 and len(new_b) == 0):
        distances = [get_distance(target, helicopters[1]) for target in new_a]
        distances = np.array(distances)
        probabilities = 1 / distances**2
        probabilities /= np.sum(probabilities)
        index_a = np.random.choice(len(new_a), p=probabilities)
        item = new_a.pop(index_a)
        new_b.append(item)
    else: 
        distances = [get_distance(target, helicopters[0]) for target in new_b]
        distances = np.array(distances)
        probabilities = 1 / distances
        probabilities /= np.sum(probabilities)
        index_b = np.random.choice(len(new_b), p=probabilities)
        item = new_b.pop(index_b)
        new_a.append(item)          

    return new_a, new_b

def DrawPoints(width, height, targets_a, targets_b, helicopters, button_x, button_y, button_height, button_width):
    # draw innitial targets and helicopters
    frame = np.zeros((height, width, 3))
    cv2.rectangle(frame, (button_x, button_y), (button_x + button_width, button_y + button_height), WHITE, -1)
    cv2.putText(frame, "RUN", (button_x + 10, button_y + 30), FONT, SIZE, GREEN)
    for target in targets_a:
        cv2.circle(frame, (target[0], target[1]), 5, YELLOW, -1)
        
    for target in targets_b:
        cv2.circle(frame, (target[0], target[1]), 5, PINK, -1)

    cv2.circle(frame, (helicopters[0][0], helicopters[0][1]), 5, BLUE, -1)
    if len(helicopters) ==2:
        cv2.circle(frame, (helicopters[1][0], helicopters[1][1]), 5, RED, -1)
    cv2.imshow("Simulated Annealing", frame)    

def Draw(width, height, targets_a, targets_b, helicopters, solution_a, solution_b, infos):
    # draw simulation
    frame = np.zeros((height, width, 3))
    for i in range(len(targets_a)):
        index_a = solution_a[i]
        index_b = solution_a[i - 1]
        point_a = (targets_a[index_a][0], targets_a[index_a][1])
        point_b = (targets_a[index_b][0], targets_a[index_b][1])
        cv2.line(frame, point_a, point_b, GREEN, 2)

    for i in range(len(targets_b)):
        index_a = solution_b[i]
        index_b = solution_b[i - 1]
        point_a = (targets_b[index_a][0], targets_b[index_a][1])
        point_b = (targets_b[index_b][0], targets_b[index_b][1])
        cv2.line(frame, point_a, point_b, WHITE, 2)

    for target in targets_a[:-1]:
        cv2.circle(frame, (target[0], target[1]), 5, YELLOW, -1)
        
    for target in targets_b[:-1]:
        cv2.circle(frame, (target[0], target[1]), 5, PINK, -1)

    cv2.circle(frame, (helicopters[0][0], helicopters[0][1]), 5, BLUE, -1)
    cv2.circle(frame, (helicopters[1][0], helicopters[1][1]), 5, RED, -1)

    cv2.putText(frame, f"Temperature ", (25, 50), FONT, SIZE, RED)
    cv2.putText(frame, f"Score ", (25, 75), FONT, SIZE, RED)
    cv2.putText(frame, f"Best Score ", (25, 100), FONT, SIZE, RED)
    cv2.putText(frame, f"Worst Score ", (25, 125), FONT, SIZE, RED)
    cv2.putText(frame, f"# Targets ", (25, 150), FONT, SIZE, RED)

    cv2.putText(frame, f" {infos[0]:.2f}", (175, 50), FONT, SIZE, GREEN)
    cv2.putText(frame, f" {infos[1]:.2f}", (175, 75), FONT, SIZE, GREEN)
    cv2.putText(frame, f" {infos[2]:.2f}", (175, 100), FONT, SIZE, GREEN)
    cv2.putText(frame, f" {infos[3]:.2f}", (175, 125), FONT, SIZE, GREEN)
    cv2.putText(frame, f" {len(targets_a)-1}", (175, 150), FONT, SIZE, GREEN)

    cv2.putText(frame, f" {infos[0]:.2f}", (300, 50), FONT, SIZE, WHITE)
    cv2.putText(frame, f" {infos[4]:.2f}", (300, 75), FONT, SIZE, WHITE)
    cv2.putText(frame, f" {infos[5]:.2f}", (300, 100), FONT, SIZE, WHITE)
    cv2.putText(frame, f" {infos[6]:.2f}", (300, 125), FONT, SIZE, WHITE)
    cv2.putText(frame, f" {len(targets_b)-1}", (300, 150), FONT, SIZE, WHITE)

    cv2.putText(frame, f" {infos[7]:.2f}", (500, 50), FONT, SIZE, BLUE)
    cv2.putText(frame, f" {infos[8]:.2f}", (500, 75), FONT, SIZE, BLUE)
    cv2.putText(frame, f" {infos[9]:.2f}", (500, 100), FONT, SIZE, BLUE)
    cv2.putText(frame, f" {infos[10]:.2f}", (500, 125), FONT, SIZE, BLUE)

    cv2.imshow("Simulated Annealing", frame)
    cv2.waitKey(5)

def FindBestRoutes(targets_a, targets_b, helicopters, current_score, best_score, worst_score, g_temperature):
    # find best routes for given targets
    targets_touple = ()
    sorted_touples = sorted(targets_a, key=lambda x: x[0])
    for touple in sorted_touples: 
        targets_touple += touple
    # check for routes that has already been optimized    
    if targets_touple in BEST_ROUTES:
        best_score_ab, trg_a, trg_b = BEST_ROUTES[targets_touple]
        current_solution_a = [targets_a.index(target) for target in trg_a]
        current_solution_b = [targets_b.index(target) for target in trg_b]
        infos = (INITIAL_TEMPERATURE, 0, 0, 0, 0, 0, 0, g_temperature, current_score, best_score, worst_score)
        Draw(WIDTH, HEIGHT, targets_a, targets_b, helicopters, current_solution_a, current_solution_b, infos)
        return (best_score_ab, current_solution_a, current_solution_b)
    
    current_solution_a = Initialize(len(targets_a))
    current_score_a = Evaluate(targets_a, current_solution_a)
    best_score_a = worst_score_a = current_score_a

    current_solution_b = Initialize(len(targets_b))
    current_score_b = Evaluate(targets_b, current_solution_b)
    best_score_b = worst_score_b = current_score_b

    temperature = INITIAL_TEMPERATURE
    while (temperature > STOPPING_TEMPERATURE):
        new_solution_a = Modify(current_solution_a)
        new_score_a = Evaluate(targets_a, new_solution_a)
        best_score_a = min(best_score_a, new_score_a)
        worst_score_a = max(worst_score_a, new_score_a)
        if new_score_a < current_score_a:
            current_solution_a = new_solution_a
            current_score_a = new_score_a
        else:
            delta = new_score_a - current_score_a
            probability = np.exp(-delta / temperature)
            if probability > np.random.uniform():
                current_solution_a = new_solution_a
                current_score_a = new_score_a

        new_solution_b = Modify(current_solution_b)
        new_score_b = Evaluate(targets_b, new_solution_b)
        best_score_b = min(best_score_b, new_score_b)
        worst_score_b = max(worst_score_b, new_score_b)
        if new_score_b < current_score_b:
            current_solution_b = new_solution_b
            current_score_b = new_score_b
        else:
            delta = new_score_b - current_score_b
            probability = np.exp(-delta / temperature)
            if probability > np.random.uniform():
                current_solution_b = new_solution_b
                current_score_b = new_score_b

        temperature *= TEMPERATURE_DECAY
        infos = (temperature, current_score_a, best_score_a, worst_score_a, current_score_b, best_score_b, worst_score_b, g_temperature, current_score, best_score, worst_score)
        Draw(WIDTH, HEIGHT, targets_a, targets_b, helicopters, current_solution_a, current_solution_b, infos)
    BEST_ROUTES[targets_touple] = (best_score_a + best_score_b, [targets_a[i] for i in current_solution_a], [targets_b[i] for i in current_solution_b])   
    return (best_score_a + best_score_b, current_solution_a, current_solution_b)    

BEST_ROUTES = {}
WIDTH = 840
HEIGHT = 680
TARGET_COUNT = 10
INITIAL_TEMPERATURE = 300
GENERAL_TEMPERATURE = 1000
STOPPING_TEMPERATURE = 1
TEMPERATURE_DECAY = 0.95
GENERAL_TEMPERATURE_DECAY = 0.95
FONT = cv2.FONT_HERSHEY_DUPLEX
SIZE = 0.7
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
YELLOW = (0, 100, 255)
BLUE = (255, 0, 0)
PINK = (100, 0, 255)
BUTTON_CLICKED = False

# BLUE helicopter - YELLOW targets - GREEN routes
# RED helicopter - PINK targets - WHITE routes

def on_mouse_click(event, x, y, flags, param, button_x, button_y, button_height, button_width, helicopters, targets_a_general, targets_b_general):
    global BUTTON_CLICKED
    if not BUTTON_CLICKED and event == cv2.EVENT_LBUTTONDOWN:
        if button_x < x < button_x + button_width and button_y < y < button_y + button_height and len(helicopters) == 2 and len(targets_a_general) + len(targets_b_general) > 0:
            BUTTON_CLICKED = not BUTTON_CLICKED
            print("Button clicked!")
        elif 160 < y < HEIGHT - 5:
            if len(helicopters) < 2:
                helicopters.append((x,y))
            elif (x,y) not in targets_a_general and (x,y) not in targets_b_general:
                if get_distance((x,y), helicopters[0]) < get_distance((x,y), helicopters[1]):
                    targets_a_general.append((x,y))
                else:
                    targets_b_general.append((x,y))  

def main():
    cv2.namedWindow("Simulated Annealing")
    button_x, button_y, button_width, button_height = WIDTH-110, 50, 100, 40
    cv2.setMouseCallback("Simulated Annealing", lambda event, x, y, flags, param: on_mouse_click(event, x, y, flags, param, button_x, button_y, button_height, button_width, helicopters, targets_a_general, targets_b_general))

    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    # custom targets and helicopters
    targets_a_general = []
    targets_b_general = []
    helicopters = []
    
    while True:
        cv2.rectangle(frame, (button_x, button_y), (button_x + button_width, button_y + button_height), WHITE, -1)
        cv2.putText(frame, "RUN", (button_x + 10, button_y + 30), FONT, SIZE, GREEN)

        cv2.imshow("Simulated Annealing", frame)
        if len(helicopters) > 0:
            DrawPoints(WIDTH, HEIGHT, targets_a_general, targets_b_general, helicopters, button_x, button_y, button_height, button_width)   
        if cv2.waitKey(5) and BUTTON_CLICKED:
            break


    # fixed targets
    # all_targets = [
    #     (160, 390), (170, 410), (200, 500), (250, 382), (388, 400), (410, 440), (255, 387), (246, 399), 
    #     (188, 312), (417, 255), (562, 365), (650, 480), (413, 340), (700, 340)
    # ]

    # random targets
    # targets_a_general = Generate(WIDTH, HEIGHT, TARGET_COUNT)
    # targets_b_general = Generate(WIDTH, HEIGHT, TARGET_COUNT)

    # random targets
    # all_targets = Generate(WIDTH, HEIGHT, 2*TARGET_COUNT)

    # randomly placed helicopters
    # helicopters = Generate(WIDTH, HEIGHT, 2)

    # fixed placement of helicopters
    # helicopters = [(110, 440), (730, 440)]

    # closest targets to each helicopter
    # all_targets = Generate(WIDTH, HEIGHT, 2*TARGET_COUNT)
    # targets_a_general = []
    # targets_b_general = []
    # for target in all_targets:
    #     if get_distance(target, helicopters[0]) < get_distance(target, helicopters[1]):
    #         targets_a_general.append(target)
    #         continue
    #     targets_b_general.append(target)
    
    current_score = np.inf
    best_score = worst_score = current_score
    
    g_temperature = GENERAL_TEMPERATURE

    best_targets_a = []
    best_targets_b = []
    best_solution_a = []
    best_solution_b = []
    first_iteration = True
    while(g_temperature > STOPPING_TEMPERATURE):
        if first_iteration:
            targets_a, targets_b = targets_a_general, targets_b_general
            first_iteration = False
        else:    
            targets_a, targets_b = ModifyTargets(targets_a_general, targets_b_general, helicopters)
        targets_a.append(helicopters[0])
        targets_b.append(helicopters[1])

        new_score, new_solution_a, new_solution_b = FindBestRoutes(targets_a, targets_b, helicopters, current_score, best_score, worst_score, g_temperature)
        if new_score < best_score:
            best_score = new_score
            best_targets_a = targets_a
            best_targets_b = targets_b
            best_solution_a = new_solution_a
            best_solution_b = new_solution_b
        if worst_score == np.inf:
            worst_score = new_score
        worst_score = max(worst_score, new_score)
        if new_score < current_score:
            targets_a_general = targets_a[:-1]
            targets_b_general = targets_b[:-1]
            current_score = new_score
        else:
            delta = new_score - current_score
            probability = np.exp(-delta / g_temperature)
            if probability > np.random.uniform():
                targets_a_general = targets_a[:-1]
                targets_b_general = targets_b[:-1]
                current_score = new_score
        g_temperature *= GENERAL_TEMPERATURE_DECAY

    global TEMPERATURE_DECAY, BEST_ROUTES
    TEMPERATURE_DECAY = 0.992
    BEST_ROUTES = {}
    best_score, best_solution_a, best_solution_b = FindBestRoutes(best_targets_a, best_targets_b, helicopters, best_score, best_score, worst_score, g_temperature)    
    infos = (0, 0, 0, 0, 0, 0, 0, g_temperature, 0, best_score, worst_score)    
    Draw(WIDTH, HEIGHT, best_targets_a, best_targets_b, helicopters, best_solution_a, best_solution_b, infos)    
    cv2.waitKey(0) 

if __name__ == "__main__":
    main()