from flask import Flask, render_template
import os
import meraki

API_KEY = os.getenv('API_KEY_RO')

orgid = '991866'

app = Flask(__name__)


@app.route("/sensors")
def home():

    dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
    sensors_status = dashboard.sensor.getOrganizationSensorReadingsLatest(
        orgid, total_pages='all'
    )
    sensors_list = dashboard.organizations.getOrganizationDevicesAvailabilities(
        orgid, total_pages='all', productTypes='sensor'
    )
    xes = []
    for sensor in sensors_status:
        for reading in sensor['readings']:
            if 'humidity' in reading:
                to_find = sensor['serial']
                for el in sensors_list:
                    if el["serial"] == to_find:
                        xes.append(
                            {'name': el['name'], 'humidity': reading['humidity'], 'ts': reading['ts']})

    return render_template("sensors.html", xes=xes)


@ app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)
