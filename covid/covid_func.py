from covid.receive_data import ReceiveCovid
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib as mpl


class Covid:

    @staticmethod
    def get_data():
        response = ""
        i = 9
        data = ReceiveCovid()
        data.start()
        response += "По состоянию на {}\n".format(data.upd_date)
        response += "Случаев: {0} ({1} за сегодня)\n".format(data.total[i], data.total_plus[i])
        response += "Активных: {0} ({1} за сегодня)\n".format(data.active[i], data.active_plus[i])
        response += "Вылечено: {0} ({1} за сегодня)\n".format(data.cured[i], data.cured_plus[i])
        response += "Умерло: {0} ({1} за сегодня)\n".format(data.died[i], data.died_plus[i])

        #  Стиль графика
        mpl.style.use("default")
        fig, ax = plt.subplots()

        #  Установка заголовка графика
        ax.set_title("Россия - статистика зараженных короновирусом", fontsize=12)

        #  Задание данных для построения графика
        ax.plot(data.days, data.died, "o-k", label="Умерло")
        ax.plot(data.days, data.cured, "o-g", label="Вылечено")
        ax.plot(data.days, data.active, "o-r", label="Активных")

        #  Настройка позиции (вида) индексов осей
        ax.set_xticklabels(data.days, fontsize=9, rotation=45, horizontalalignment="center")

        #  Частота индексов на оси OY
        ax.yaxis.set_major_locator(ticker.MultipleLocator(4))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))

        #  Названия осей
        ax.set_xlabel("Дата", fontsize=12)
        ax.set_ylabel("Кол-во чел.")

        #  Инициализация легенды графика
        ax.legend()

        plt.show()
        fig.savefig("covid/covid.png")
        return response, "covid/covid.png"
