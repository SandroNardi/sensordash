from flask import Flask, render_template
import os
import meraki
import datetime as dt
import zoneinfo as zi
import dateutil.parser as datep

API_KEY = os.getenv('MERAKI_HOME_NET_RO')

orgid = '000000'
org_name = 'Sandro at Meraki'

app = Flask(__name__)


@app.route("/")
def home():
    # create dashboard obj
    dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
    # fetch all info from meraki dashboard via API except on error
    try:
        # get org
        orgs = dashboard.organizations.getOrganizations()
        # search for org by name break on find
        for org in orgs:
            if org['name'] == org_name:
                orgid = org['id']
                break
        # fetch sensor readings
        sensors_status = dashboard.sensor.getOrganizationSensorReadingsLatest(
            orgid, total_pages='all'
        )
        # fetch sensor list for names
        sensors_list = dashboard.organizations.getOrganizationDevicesAvailabilities(
            orgid, total_pages='all', productTypes='sensor'
        )
        # fetch network for timezone
        networks = dashboard.organizations.getOrganizationNetworks(
            orgid, total_pages='all'
        )
    except Exception as error:
        # render error page template on API exception
        return render_template("error.html", error=error)
    # create a dictionary {'network id':'network time zone'}
    net_tzones = {}
    for network in networks:
        net_tzones[network['id']] = network['timeZone']

    # for each sensor reading
    sensor_to_output = []
    for sensor in sensors_status:
        # check all the readings available
        for reading in sensor['readings']:
            # skip to next elemnt if humitity is not available
            if 'humidity' not in reading:
                continue

            # if sensor has humidity serach for sensor name in sensor list
            to_find = sensor['serial']
            for sensor_device in sensors_list:
                # skip if serial not match
                if sensor_device["serial"] != to_find:
                    continue
                # time zone conversion

                # set time zone
                tz = zi.ZoneInfo(net_tzones[sensor['network']['id']])
                # convert current time to time zone
                now_tz = dt.datetime.now().astimezone(tz)
                # convert last reading time stamp to time zone
                last_reading_tz = datep.isoparse(reading['ts'])

                #last_reading_tz = dt.datetime.fromisoformat(reading['ts']).astimezone(tz)
                # calculate the difference
                delta = now_tz-last_reading_tz


                # convert delta in minutes and seconds
                total_seconds = int(delta.total_seconds())
                hours, remainder = divmod(total_seconds, 60*60)
                minutes, seconds = divmod(remainder, 60)

                # format in printable output xx h xx m
                last_update = f'{hours} h {minutes} m'

                # add to printalbe list {sensor name, current humidity %, last update xx h xx m}
                sensor_to_output.append(
                    {'name': sensor_device['name'], 'humidity': reading['humidity'], 'last_update': last_update})

    # render in template sensors
    return render_template("sensors.html", sensor_to_output=sensor_to_output)


if __name__ == '__main__':
    app.run(debug=True)
