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

        mpl.style.use("default")
        fig, ax = plt.subplots(figsize=(3, 3))

        ax.set_title("Россия - статистика зараженных короновирусов")
        ax.plot(data.days, data.active, 'C1', label='C1')
        ax.plot(data.days, data.cured, 'C2', label='C2')
        ax.plot(data.days, data.died)
        ax.legend()

        fig.savefig("covid/covid.png")
        return response, "covid/covid.png"

