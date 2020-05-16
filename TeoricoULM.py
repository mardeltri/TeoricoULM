import pickle
import os
import random
from data.menus import MENU, SETTINGS_MENU


class Utils:
    def __init__(self):
        if os.name == 'posix':
            self.clear_command = 'reset'
        else:
            self.clear_command = 'cls'

    def wait_user(self):
        input("\nPresiona Intro para continuar...")

    def clear_screen(self):
        os.system(self.clear_command)


class App(Utils):
    def __init__(self):
        Utils.__init__(self)
        self._questions = None
        self._param = None
        self.load_data()
        self.main_menu()
        self.save_data()
        self.bye_bye()

    def load_data(self):
        with open('data/questions.pickle', 'rb') as f:
            questions = pickle.load(f)
            self._questions = Questions(questions)
        with open('data/param.pickle', 'rb') as f:
            self._param = pickle.load(f)

    def main_menu(self):
        usrquest = None
        # Define menu
        while True:
            self.clear_screen()
            print("Bienvenido!\n")
            print("Menu principal")
            print("Por favor, selecciona una de las siguientes opciones:")
            options = MENU.keys()
            for entry in options:
                print(entry, MENU[entry])
            selection = input("\nSelección:")
            if selection == '1':
                usrquest = self.select_topics()
            elif selection in set(('2', '')):
                usrquest = self.continue_last()
            elif selection == '3':
                self.show_results()
            elif selection == '4':
                param = self.settings()
            elif selection in set(('5', 'e')):
                break
            else:
                print("Opción no disponible! Por favor, selecciona una opción válida.")
        self._questions.update(usrquest)

    def select_topics(self):
        self.clear_screen()
        print('Menú de selección de temas.\n')
        usrtopics = self.ask_topics()
        self._param['usrtopics'] = usrtopics
        usrquest = self._questions.get_by_topics(usrtopics)
        test = Test(usrquest, self._param)
        return test.get_questions()

    def continue_last(self):
        self.clear_screen()
        print('Menú para continuar con los últimos temas.')
        self.show_prev_usrtopics()
        usrtopics = self._param['usrtopics']
        usrquest = self._questions.get_by_topics(usrtopics)
        test = Test(usrquest, self._param)
        return test.get_questions()

    def show_prev_usrtopics(self):
        print('La última selección fue:')
        usrtopics = self._param['usrtopics']
        capitalizer = lambda x: x.capitalize()
        usrtopics = list(map(capitalizer, usrtopics))
        print(','.join(usrtopics))
        self.wait_user()

    def ask_topics(self):
        # Get topics
        topics = self._param['topics']
        for idx, topic in enumerate(topics):
            print('{0} - {1}'.format(idx + 1, topic.capitalize()))
        while True:
            idx_str = input("\nSelecciona uno o varios temas. Los valores deben separarse con espacios:")
            idxl = idx_str.split(' ')
            try:
                ind_pos = [int(idxk) - 1 for idxk in idxl]
            except ValueError:
                continue
            try:
                selection = [topics[i] for i in ind_pos]
            except IndexError:
                continue
            break
        return selection

    def settings(self):
        while True:
            self.clear_screen()
            print('Menú de configuración')
            print('Seleciona el parámetro a modificar:')
            options = []
            for entry in SETTINGS_MENU:
                print('{0}. {1}'.format(entry['n'], entry['des']))
                options.append(entry['n'])
            lastop = int(options[-1])
            print('{:d} o Intro. Menu principal'.format(lastop + 1))
            usersel = input("Selección:")
            if usersel in set(options):
                sel = next((item for item in SETTINGS_MENU if item['n'] == usersel), None)
                if sel['type']:
                    self.ask_parameter(sel)
                else:
                    # If type is empty, an action should be carried out
                    if sel['n'] == '4':  # Reset questions
                        self.__reset_questions(sel)
            else:
                break

    def __reset_questions(self, sel):
        self.clear_screen()
        print('Menú de reseteo de datos')
        print(sel['londes'])
        usersel_str = input("Selección: ")
        if usersel_str == '1':  # Reset all
            self._questions.set_value('score', 0)
            self._questions.set_value('ruled_out', False)
            print('Reseteo completo terminado.')
        elif usersel_str == '2':  # Reset score
            self._questions.set_value('score', 0)
            print('Contadores reestablecidos.')
        elif usersel_str == '3':  # Reset ruled out
            self._questions.set_value('ruled_out', False)
            print('Preguntas descartadas reestablecidas.')
        self.wait_user()

    def ask_parameter(self, sel):

        print(sel['londes'])
        print('Valor actual: {0}'.format(self._param[sel['var']]))
        flag = True
        while flag:
            usersel_str = input("Introducir nuevo valor: ")
            try:
                usersel_num = float(usersel_str)
            except ValueError:
                print('Valor no válido, introduzca un número.')
                continue
            if sel['type'] == 'int':
                self._param[sel['var']] = int(usersel_num)
            else:
                self._param[sel['var']] = usersel_num
            flag = False

    def show_results(self):
        self.clear_screen()
        print('Menu de resultados\n')
        columns = ['Tema', 'Totales', 'Incorrectas', 'Correctas', 'Contestadas']
        print('{:30s}{:8s}{:12s}{:12s}{:12s}'.format(*columns))
        str_creator = lambda x, y: '{:d}/{:.1f}%'.format(x, y)
        for idx, topic in enumerate(self._param['topics']):
            usrquest = self._questions.get_by_topics([topic])
            topicData = []
            topicData.append(topic.capitalize())
            total = len(usrquest)
            topicData.append(total)
            nincorrect, ncorrect, nrest = usrquest.get_nquest_by_score()
            topicData.append(str_creator(nincorrect, nincorrect / total * 100))
            topicData.append(str_creator(ncorrect, ncorrect / total * 100))
            topicData.append(str_creator((total-nrest), (total-nrest) / total * 100))
            print('{:30s}{:<8d}{:<12s}{:<12s}{:<12s}'.format(*topicData))
        self.wait_user()

    def save_data(self):
        with open("data/questions.pickle", 'wb') as f:
            pickle.dump(self._questions.questions, f)
        with open("data/param.pickle", 'wb') as f:
            pickle.dump(self._param, f)
        print('Datos guardados.')

    def bye_bye(self):
        print('Hasta luego! Qué tengas un buen día! :)')


class Questions:
    def __init__(self, questions):
        self.questions = questions

    def get_by_topics(self, topics):
        # Get questions
        selection = []
        for topic in topics:
            for question in self.questions:
                idx = question['group'].find(topic)
                if idx != -1:
                    selection.append(question)
        # print(len(questions))
        return Questions(selection)

    def get_random_sample(self, sample_size):
        selection = []
        nquestions = len(self.questions)
        if nquestions > sample_size:
            nquestions = sample_size
        [selection.append(question) for question in random.sample(self.questions, nquestions)]
        return Questions(selection), nquestions

    def update(self, questions_mod):
        if questions_mod is None:
            return
        # Sort questions
        self.questions = sorted(self.questions, key=lambda question: question['score'])
        for question_modk in questions_mod.questions:
            # idx = question_modk['id']-1
            question = next(question for question in self.questions if question['id'] == question_modk['id'])
            question['score'] = question_modk['score']
            # self.questions[idx] = question

    def filter(self, function):
        selection = list(filter(function, self.questions))
        return Questions(selection)

    def filter_pos_score(self):
        return self.filter(lambda question: question['score'] >= 0)

    def filter_neg_score(self):
        return self.filter(lambda question: question['score'] < 0)

    def filter_score(self, score):
        return self.filter(lambda question: question['score'] == score)

    def filter_by_value(self, param, value):
        return self.filter(lambda question: question[param] == value)

    def split_by_score(self):
        # This method splits questions by its question's score.
        # There are three outputs: questions with negative score, with the lowest positive score and the rest
        # Split apart negative values
        negatives = self.filter_neg_score()
        # Split apart positive values
        positives = self.filter_pos_score()
        # Compute min value from positives ones
        self.min_pos_value = positives.min('score')
        # Get questions with previous minimum positive value
        min_score_quest = self.filter_score(self.min_pos_value)
        # Split apart the rest of questions (those above minimum positive value)
        rest = self.filter(lambda question: question['score'] > self.min_pos_value)
        return negatives, min_score_quest, rest

    def get_nquest_by_score(self):
        negatives, min_score_quest, rest = self.split_by_score()
        nincorrect = len(negatives)
        ncorrect = len(rest)
        nrest = len(min_score_quest)
        if self.min_pos_value > 0:
            ncorrect += nrest
            nrest = 0
        return nincorrect, ncorrect, nrest

    def get_min_pos_value(self):
        # Returns minimum positive score value
        if self._min_pos_value is None:
            self.split_by_score()
        return self._min_pos_value

    def set_value(self, param, value):
        [question.update({param: value}) for question in self.questions]

    def min(self, param):
        min_value = min(question[param] for question in self.questions)
        return min_value

    def __len__(self):
        return len(self.questions)

    def __iter__(self):
        return iter(self.questions)


class Test(Utils):
    def __init__(self, questions, param):
        Utils.__init__(self)
        self._questions = questions.filter_by_value('ruled_out', False)
        self._param = param
        self._test_questions = None

        test_questions = self.create()
        self.launch(test_questions)

    def create(self):
        test = []
        # Split apart negatives, minimum positive values and the rest
        negatives, min_score_quest, rest = self._questions.split_by_score()

        # Get number of questions
        nquest_rem = self._param['nquest']
        nrepmax = int(self._param['prep'] * self._param['nquest'])
        sample = negatives.get_random_sample(nrepmax)
        test += sample[0].questions
        nquest_rem -= sample[1]

        # Get random questions with negative score
        sample = min_score_quest.get_random_sample(nquest_rem)
        test += sample[0].questions
        nquest_rem -= sample[1]

        # If more questions need to be included
        if nquest_rem > 0:
            sample = rest.get_random_sample(nquest_rem)
            test += sample[0].questions
            nquest_rem -= sample[1]

        # Shake questions
        test = random.sample(test, len(test))
        
        return test

    def launch(self, test_questions):
        ncorrect = 0
        for idx, question in enumerate(test_questions):
            quest = Question(question, self._param)
            flag_exit = quest.ask(idx)
            if flag_exit:
                return
            bans = quest.check_answer()
            flag_exit = quest.menu()
            if flag_exit:
                return
            question = quest.get_question()
            if bans:
                ncorrect += 1
            # test[idx] = question
            # Update questions (so that everything is saved when user stops the program)
            self._questions.update(Questions([question]))

        # End of test
        self.show_results(ncorrect)

    def show_results(self, ncorrect):
        self.clear_screen()
        print('Fin del test!')
        mark = ncorrect / self._param['nquest'] * 10
        print('Puntuación:{:5.2f}'.format(mark))
        if mark >= 5:
            print('Enhorabuena! You are awesome!! : )')
        self.wait_user()

    def get_questions(self):
        return self._questions


class Question(Utils):
    def __init__(self, question, param):
        Utils.__init__(self)
        self._question = question
        self._param = param
        self._answer = None
        self._finish_test = False
        self._flag_digit = True
        self._list_type = param['list_type']  # 1: (a,b,c,d) 2: (1,2,3,4)

        self._opdict = param['opdict']
        self._options = set(list(self._opdict.values()) + list(self._opdict.keys()))

    def ask(self, idx):
        self.print(idx)
        flag = True
        flag_exit = False
        while True:
            answer = input("Respuesta:")
            if answer in set(('exit','e')) :
                answer = -1
                flag = False
                flag_exit = True
                break
            elif answer in self._options:
                if self._list_type == 2:
                    answer = self._param['opdict'][answer]
                flag = False
                break
            else:
                if self._list_type == 1:
                    print('La respuesta debe corresponder con la letra (a, b, c, d) de la pregunta.')
                else:
                    print('La respuesta debe corresponder con la posición (1, 2, 3, 4) de la pregunta.')
                continue
        # print('Respuesta usuario: ', answer)
        self._answer = answer
        return flag_exit

    def check_answer(self):
        if self._answer is None:
            print('Call ask before using this method')
            return None
        print('\n')
        if self._question['answer'] == self._answer:
            bans = True
            self._question['score'] += 1
            print('La respuesta es correcta! :)')
        else:
            bans = False
            self._question['score'] -= 1
            print('La respuesta es incorrecta. La solución es:')
            correct_ans = self._question['answer']
            correct_ans_str = correct_ans
            if self._list_type == 2:
                for num, letter in self._opdict.items():
                    if letter == correct_ans:
                        correct_ans_str = num
                        break
            print('{0}. {1}'.format(correct_ans_str, self._question['options'][correct_ans]))
        #self.wait_user()
        return bans

    def print(self, idx):
        self.clear_screen()
        print('Test en curso')
        idx += 1
        print('Tema: {0}\n'.format(self._question['group'].split('-')[0]))
        print('Pregunta {:d}/{:d}'.format(idx, self._param['nquest']))
        print('\n{0}. {1}'.format(idx, self._question['heading']))
        for idxans, op in enumerate(self._question['options'].keys()):
            if self._list_type == 1:
                print('{0}. {1}'.format(op, self._question['options'][op]))
            else:
                print('{0}. {1}'.format(idxans + 1, self._question['options'][op]))
        print('\nEscriba exit/e para salir')

    def get_question(self):
        return self._question

    def menu(self):
        flag_exit = False
        # Define menu
        menu = {}
        menu['1'] = "Continuar (Intro)"
        menu['2'] = "Descartar pregunta"
        menu['3'] = "Salir"
        while True:
            print("\nSelecciona una de las siguientes opciones:")
            options = menu.keys()
            for entry in options:
                print(entry, menu[entry])
            selection = input("Selección:")
            if selection in set(('1', '')):
                break
            elif selection == '2':
                self.rule_out()
                break
            elif selection == '3':
                flag_exit = True
                break
            else:
                print("Opción no disponible! Por favor, selecciona una opción válida.")
        return flag_exit

    def rule_out(self):
        self._question['ruled_out'] = True
        print('Pregunta descartada.')
        self.wait_user()


if __name__ == "__main__":
    app = App()
