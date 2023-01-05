from flask import Flask, render_template
import os
import meraki
import datetime
import pytz

API_KEY = os.getenv('API_KEY_RO')

orgid = '000000'

app = Flask(__name__)


@app.route("/")
def home():

    dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
    try:
        orgs = dashboard.organizations.getOrganizations()
        for org in orgs:
            if org['name'] == 'Sandro at Meraki':
                orgid = org['id']
                break

        sensors_status = dashboard.sensor.getOrganizationSensorReadingsLatest(
            orgid, total_pages='all'
        )
        sensors_list = dashboard.organizations.getOrganizationDevicesAvailabilities(
            orgid, total_pages='all', productTypes='sensor'
        )
    except Exception as e:
        return render_template("error.html", x=e)
    xes = []
    for sensor in sensors_status:
        for reading in sensor['readings']:

            if 'humidity' not in reading:
                continue

            # sensor has humidity
            to_find = sensor['serial']

            for el in sensors_list:
                if el["serial"] != to_find:
                    continue
                diff = datetime.datetime.now(
                )-datetime.datetime.strptime(reading['ts'], '%Y-%m-%dT%H:%M:%SZ')

                total_seconds = int(diff.total_seconds())
                hours, remainder = divmod(total_seconds, 60*60)
                minutes, seconds = divmod(remainder, 60)

                last_update = f'{hours} h {minutes} m'

                xes.append(
                    {'name': el['name'], 'humidity': reading['humidity'], 'last_update': last_update})

    return render_template("sensors.html", xes=xes)


if __name__ == '__main__':
    app.run(debug=True)
