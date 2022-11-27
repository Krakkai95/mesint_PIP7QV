import random
import matplotlib.pyplot as plt
import numpy as np

def main():
    (
        max_machines,
        max_works,
        max_tabu,
        max_pauses,
        pauses_array,
        max_iterations,
    ) = readconfig()

    
    works_array = [[0 for _ in range(max_machines)] for _ in range(max_works)]
    for i in range(max_machines):
        for k in range(max_works):
            works_array[k][i] = random.randint(1, 50)
            print(str(works_array[k][i]) + "\t", end="")
        print("\n", end="")

        
    main_search(
        max_machines,
        max_works,
        max_tabu,
        max_pauses,
        pauses_array,
        works_array,
        max_iterations,
    )


def readconfig():
    pauses_array = []
    random.seed(int(input("Add meg a seedet a generáláshoz: ")))
    max_machines = int(input("Gépek száma: "))
    max_works = int(input("Munkák száma: "))
    max_tabu = int(input("A tabu tömb mérete: "))
    max_pauses = int(input("Szünetek száma: "))
    
    if max_pauses > 0:
        print("Add meg a szüneteket. Példa: 5-7")
        for i in range(max_pauses):
            pauses_array += [
                input("Add meg a következő szünetet: ").replace("\n", "").split("-")
            ]
    else:
        print("A szünetek száma 0")
    max_iterations = int(input("Maximális iterációszám: "))

    print("Ellenörzendő iterációk száma: ", max_iterations)

    return max_machines, max_works, max_tabu, max_pauses, pauses_array, max_iterations


def main_search(
    max_machines,
    max_works,
    max_tabu,
    max_pauses,
    pauses_array,
    works_array,
    max_iterations,
    ):

    
    default_array = []
    tabu = []
    for x in range(max_works):
        default_array += [x]

    best_time = float("inf")
    for i in range(max_iterations):
        machine_work = [0 for x in range(max_machines)]
        machine_solved = [0 for x in range(max_machines)]
        swappoint1 = random.randint(0, max_works - 1)
        swappoint2 = random.randint(0, max_works - 1)
        default_array_copy = default_array.copy()
        default_array_copy[swappoint1], default_array_copy[swappoint2] =(
        default_array_copy[swappoint2], default_array_copy[swappoint1])
        
        if default_array_copy in tabu:
            continue
        elif len(tabu) < max_tabu:
            tabu.append(default_array_copy)

        
        time = calculate_job_time(
            max_machines,
            max_works,
            max_pauses,
            pauses_array,
            works_array,
            default_array_copy,
            machine_work,
            machine_solved,
            False,
        )

        
        if time < best_time:
            best_time = time
            default_array = default_array_copy.copy()
            print("Új idő: ", best_time)
            print("Új sorrend: ", default_array)

    print("\n\nA program sikeresen lefutott.")
    machine_work = [0 for x in range(max_machines)]
    machine_solved = [0 for x in range(max_machines)]
    time = calculate_job_time(
        max_machines,
        max_works,
        max_pauses,
        pauses_array,
        works_array,
        default_array_copy,
        machine_work,
        machine_solved,
        True,
    )



def calculate_job_time(
    max_machines,
    max_works,
    max_pauses,
    pauses_array,
    works_array,
    default_array_copy,
    machine_work,
    machine_solved,
    display_graphic,
):
    if display_graphic:
        plt.style.use("_mpl-gallery")
        fig, ax = plt.subplots()

    time = 0
    while machine_solved[max_machines - 1] != max_works:
        for i in range(max_machines):
            if machine_solved[i]==max_works:
                continue
            if machine_work[i] == works_array[default_array_copy[machine_solved[i]]][i]:
                if machine_solved[i]<max_works:
                    machine_solved[i] += 1
                machine_work[i] = 0
                if machine_solved[i] != max_works:
                    if pausecheck(time, works_array[default_array_copy[machine_solved[i]]][i]-machine_work[i], pauses_array, max_pauses) and (
                        i == 0 or machine_solved[i - 1] > machine_solved[i]
                    ):
                        machine_work[i] +=1
                if display_graphic:
                    ax.bar(
                        time
                        - works_array[default_array_copy[machine_solved[i] - 1]][i],
                        0.5,
                        width=works_array[default_array_copy[machine_solved[i] - 1]][i],
                        bottom=max_machines - i - 1,
                        edgecolor="white",
                        linewidth=0.5,
                        align="edge",
                        color="green"
                    )
            elif pausecheck(time, works_array[default_array_copy[machine_solved[i]]][i]-machine_work[i], pauses_array, max_pauses) and (
                    i == 0 or machine_solved[i - 1] > machine_solved[i]
                ):
                    machine_work[i] += 1
        time += 1
    time-=1
    if display_graphic:
        ax.set(
            xlim=(0, time),
            xticks=np.arange(0, 0),
            ylim=(0, max_machines),
            yticks=np.arange(0, max_machines + 1),
        )
        plt.show()
    return time



def pausecheck(time, machine_work, pauses_array, max_pauses):
    for i in range(max_pauses):
        if (
            (time >= int(pauses_array[i][0]) and time <= int(pauses_array[i][1]))
            or (
                time + machine_work >= int(pauses_array[i][0])
                and time + machine_work <= int(pauses_array[i][1])
            )
            or (
                time <= int(pauses_array[i][0])
                and time + machine_work >= int(pauses_array[i][1])
            )
        ):
            return False
    return True

if __name__ == "__main__":
    main()
