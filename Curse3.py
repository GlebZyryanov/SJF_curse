from abc import ABC, abstractmethod
import sys
class SJF(ABC):
    @abstractmethod
    def taskData(self,none_tasks):
        pass

    @abstractmethod
    def scheduleTasks(self, tasks_data):
        pass

    @abstractmethod
    def getTimeTaskComplete(self, tasks_data):
        pass

    @abstractmethod
    def getWaitingTime(self, tasks_data):
        pass

    @abstractmethod
    def printData(self, tasks_data, average_taskcomplete_time, average_waiting_time, sequence_tasks):
        pass


class SJF_NonPreemptive(SJF):

    def taskData(self, none_tasks):
        tasks_data = []
        for i in range(none_tasks):
            temporary = []
            tasks_number = int(input("Введите номер задачи: "))
            if(tasks_data.count(tasks_number)>1):
                print("2-х одинаковых задач быть не может!")
                sys.exit("Ошибка!")
            arrival_task_time = int(input(f"Введите время прибытия задачи {tasks_number}: "))
            lenght_task = int(input(f"Введите длину задачи {tasks_number}: "))
            temporary.extend([tasks_number, arrival_task_time, lenght_task, 0])
          #  0 - назначаем состояние задачи. 0 - не выполнено, 1 - задача выполнена
            tasks_data.append(temporary)
        SJF_NonPreemptive.scheduleTasks(self, tasks_data)
    def scheduleTasks(self, tasks_data):
        start_time = [] #время старта выполнения
        exit_time = []  #время окончания
        s_time = 0
        sequence_tasks = []
        tasks_data.sort(key=lambda x: x[1])
        #Сортировка в соответствии с временем прибытия
        for i in range(len(tasks_data)):
            ready_queue = [] #в этой очереди задачи пришедшие процессору
            temp = []
            normal_queue = [] #в этой очереди - задачи пока не пришедшие процессору
            for j in range(len(tasks_data)):
                if (tasks_data[j][1] <= s_time) and (tasks_data[j][3] == 0):
                    temp.extend([tasks_data[j][0], tasks_data[j][1], tasks_data[j][2]])
                    ready_queue.append(temp)
                    temp = []
                elif tasks_data[j][3] == 0:
                    temp.extend([tasks_data[j][0], tasks_data[j][1], tasks_data[j][2]])
                    normal_queue.append(temp)
                    temp = []
            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x[2])
                #сортировка в соответствии с временем выполнения
                start_time.append(s_time)
                s_time = s_time + ready_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                sequence_tasks.append(ready_queue[0][0])
                for k in range(len(tasks_data)):
                    if tasks_data[k][0] == ready_queue[0][0]:
                        break
                tasks_data[k][3] = 1
                tasks_data[k].append(e_time)
            elif len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                start_time.append(s_time)
                s_time = s_time + normal_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                sequence_tasks.append(normal_queue[0][0])
                for k in range(len(tasks_data)):
                    if tasks_data[k][0] == normal_queue[0][0]:
                        break
                tasks_data[k][3] = 1
                tasks_data[k].append(e_time)
        t_time = SJF_NonPreemptive.getTimeTaskComplete(self, tasks_data)
        w_time = SJF_NonPreemptive.getWaitingTime(self, tasks_data)
        SJF_NonPreemptive.printData(self, tasks_data, t_time, w_time,sequence_tasks)
    def getTimeTaskComplete(self, tasks_data):
        total_taskcomplete_time = 0
        for i in range(len(tasks_data)):
            taskcomplete_time = tasks_data[i][4] - tasks_data[i][1]

           # taskcomplete_time = completion_time - arrival_task_time
           #Время выполнения задачи - это время пока задача обрабатывается процессором

            total_taskcomplete_time = total_taskcomplete_time + taskcomplete_time
            tasks_data[i].append(taskcomplete_time)
        average_taskcomplete_time = total_taskcomplete_time / len(tasks_data)

       # average_taskcomplete_time = total_taskcomplete_time / none_tasks

        return average_taskcomplete_time
    def getWaitingTime(self, tasks_data):
        total_waiting_time = 0
        for i in range(len(tasks_data)):
            waiting_time = tasks_data[i][5] - tasks_data[i][2]
           # waiting_time = taskcomplete_time - lenght_task.
           #Время ожидания задачи - это время пока пакет "ждет" своей очереди
            total_waiting_time = total_waiting_time + waiting_time
            tasks_data[i].append(waiting_time)
        average_waiting_time = total_waiting_time / len(tasks_data)

      #  average_waiting_time = total_waiting_time / none_tasks

        return average_waiting_time
    def printData(self, tasks_data, average_taskcomplete_time, average_waiting_time, sequence_tasks):
        tasks_data.sort(key=lambda x: x[0])
       # Сортировка по номеру задачи
        for i in range(len(tasks_data)):
            for j in range(len(tasks_data[i])):
                if(j==0):print("Номер задачи: ",tasks_data[i][j], end="|")
                if(j==1): print(" Время поступления: ",tasks_data[i][j],end="|")
                if(j==2):print(" Длина задачи: ",tasks_data[i][j],end="|")
                if(j==3):print(" Факт завершения: ",tasks_data[i][j],end="|")
                if(j==4):print(" Время завершения: ",tasks_data[i][j],end="|")
                if(j==5):print(" Время выполнения задачи: ",tasks_data[i][j],end="|")
                if(j==6):print(" Время ожидания задачи: ",tasks_data[i][j])
        print("Среднее время выполнения:", average_taskcomplete_time,'\n')
        print("Среднее время простоя задач:", average_waiting_time,'\n')
        print("Последовательность выполнения задач:", sequence_tasks,'\n')
class SJF_Preemptive(SJF):
    def taskData(self, none_tasks):
        tasks_data = []
        for i in range(none_tasks):
            temporary = []
            tasks_number = int(input("Введите номер задачи: "))
            if (tasks_data.count(tasks_number) > 1):
                print("2-х одинаковых задач быть не может!")
                sys.exit("Ошибка!")
            arrival_task_time = int(input(f"Введите время прибытия задачи {tasks_number}: "))
            lenght_task = int(input(f"Введите время выполнения задачи {tasks_number}: "))
            temporary.extend([tasks_number, arrival_task_time, lenght_task, 0, lenght_task])
            #  0 - назначаем состояние задачи. 0 - не выполнено, 1 - задача выполнена
            tasks_data.append(temporary)
        SJF_Preemptive.scheduleTasks(self, tasks_data)
    def scheduleTasks(self, tasks_data):
        start_time = []
        exit_time = []
        s_time = 0
        sequence_tasks = []
        tasks_data.sort(key=lambda x: x[1])
        #Сортировка задач по времени прибытия на процессор
        while 1:
            ready_queue = []
            normal_queue = []
            temp = []
            for i in range(len(tasks_data)):
                if tasks_data[i][1] <= s_time and tasks_data[i][3] == 0:
                    temp.extend([tasks_data[i][0], tasks_data[i][1], tasks_data[i][2], tasks_data[i][4]])
                    ready_queue.append(temp)
                    temp = []
                elif tasks_data[i][3] == 0:
                    temp.extend([tasks_data[i][0], tasks_data[i][1], tasks_data[i][2], tasks_data[i][4]])
                    normal_queue.append(temp)
                    temp = []
            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break
            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x[2])
                #Сортировка задач по длине
                start_time.append(s_time)
                s_time = s_time + 1
                e_time = s_time
                exit_time.append(e_time)
                sequence_tasks.append(ready_queue[0][0])
                for k in range(len(tasks_data)):
                    if tasks_data[k][0] == ready_queue[0][0]:
                        break
                tasks_data[k][2] = tasks_data[k][2] - 1
                # Если длина пакета = 0, то задача выполнена
                if tasks_data[k][2] == 0:  
                    tasks_data[k][3] = 1
                    tasks_data[k].append(e_time)
            if len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                start_time.append(s_time)
                s_time = s_time + 1
                e_time = s_time
                exit_time.append(e_time)
                sequence_tasks.append(normal_queue[0][0])
                for k in range(len(tasks_data)):
                    if tasks_data[k][0] == normal_queue[0][0]:
                        break
                tasks_data[k][2] = tasks_data[k][2] - 1
                #если длина пакета = 0, то задача выполнена
                if tasks_data[k][2] == 0:  
                    tasks_data[k][3] = 1
                    tasks_data[k].append(e_time)
        t_time = SJF_Preemptive.getTimeTaskComplete(self, tasks_data)
        w_time = SJF_Preemptive.getWaitingTime(self, tasks_data)
        SJF_Preemptive.printData(self, tasks_data, t_time, w_time, sequence_tasks)
    def getTimeTaskComplete(self, tasks_data):
        total_taskcomplete_time = 0
        for i in range(len(tasks_data)):
            taskcomplete_time = tasks_data[i][5] - tasks_data[i][1]
            #taskcomplete_time = completion_time - arrival_task_time
            total_taskcomplete_time = total_taskcomplete_time + taskcomplete_time
            tasks_data[i].append(taskcomplete_time)
        average_taskcomplete_time = total_taskcomplete_time / len(tasks_data)
        #average_taskcomplete_time = total_taskcomplete_time / none_tasks
        return average_taskcomplete_time
    def getWaitingTime(self, tasks_data):
        total_waiting_time = 0
        for i in range(len(tasks_data)):
            waiting_time = tasks_data[i][6] - tasks_data[i][4]
            #waiting_time = taskcomplete_time - lenght_task
            total_waiting_time = total_waiting_time + waiting_time
            tasks_data[i].append(waiting_time)
        average_waiting_time = total_waiting_time / len(tasks_data)
       # average_waiting_time = total_waiting_time / none_tasks
        return average_waiting_time
    def printData(self, tasks_data, average_taskcomplete_time, average_waiting_time, sequence_tasks):
        tasks_data.sort(key=lambda x: x[0])
        for i in range(len(tasks_data)):
            for j in range(len(tasks_data[i])):
                if (j == 0): print("Задача:", tasks_data[i][j], end="|")
                if (j == 1): print(" Время поступления:", tasks_data[i][j], end="|")
                if (j == 2): print(" Длина задачи(конец):", tasks_data[i][j], end="|")
                if (j == 3): print(" Факт завершения:", tasks_data[i][j], end="|")
                if (j == 4): print(" Длина задачи(начальная):", tasks_data[i][j], end="|")
                if (j == 5): print(" Время завершения:", tasks_data[i][j], end="|")
                if (j == 6): print(" Время выполнения:", tasks_data[i][j], end="|")
                if (j == 7): print(" Время ожидания:", tasks_data[i][j])
        print("Среднее время выполнения:", average_taskcomplete_time, '\n')
        print("Среднее время простоя задач:", average_waiting_time, '\n')
        print("Последовательность выполнения задач:", sequence_tasks, '\n')


if __name__ == "__main__":
    print("Моделирование поведения мультизадачной системы (классического мультипрограммирования)\n"
          "пакетного режима с фиксированным числом задач и дисциплиной обслуживания JSF")
    print("Существует 2 версии алгоритма JSF - Упреждающее(Preemptive) и Неупреждающее(Non-Preemptive) или планирование без вытеснений\n"
          "1 - JSF(Preemptive)\t2 - JSF(Non-Preemptive)\n")
    flag = int(input())
    if(flag==1):
        none_tasks = int(input("Ввод количества задач: "))
        sjf = SJF_Preemptive()
        sjf.taskData(none_tasks)

    if(flag ==2):
        none_tasks = int(input("Ввод количества задач: "))
        sjf = SJF_NonPreemptive()
        sjf.taskData(none_tasks)
    if(flag!=1 and flag!=2):
        print("\nОшибка ввода.")
