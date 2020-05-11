from covid.receive_data import ReceiveCovid
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

        labels = ["Активных", "Вылечено", "Умерло"]
        colors = ["#CF3419", "#1CC423", "k"]

        #  Стиль графика
        mpl.style.use("default")
        fig, ax = plt.subplots()

        ax.set_title("Россия - статистика зараженных короновирусом", fontsize=12)

        y1 = [int(data.active[i]) for i in range(len(data.active))]
        y2 = [int(data.cured[i]) for i in range(len(data.cured))]
        y3 = [int(data.died[i]) for i in range(len(data.died))]

        ax.stackplot(data.days, y1, y2, y3, labels=labels, colors=colors, baseline="zero")
        fig.autofmt_xdate()

        #  Инициализация легенды графика
        ax.legend(loc="upper left")
        plt.show()

        fig.savefig("covid/covid.png")
        return response, "covid/covid.png"
