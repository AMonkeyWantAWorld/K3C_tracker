import base64
import logging
import requests
import json
import voluptuous as vol
from collections import namedtuple

from homeassistant.components.device_tracker import (
    DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import (
    CONF_HOST, CONF_PASSWORD, CONF_USERNAME)
import homeassistant.helpers.config_validation as cv
_LOGGER = logging.getLogger(__name__)

Device = namedtuple('Device', ['mac'])

HTTP_HEADER_NO_CACHE = 'no-cache'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_USERNAME): cv.string
})

stoken = ""

def get_scanner(hass, config):
    """Validate the configuration and return a TP-Link scanner."""
    try:
        return K3CDeviceScanner(config[DOMAIN])
    except ConnectionError:
        return None

class K3CDeviceScanner(DeviceScanner):

    def __init__(self,config):
        host = config[CONF_HOST]
        username, password = config[CONF_USERNAME], config[CONF_PASSWORD]

        self.host = host
        self.username = username
        self.password = password

        self.last_results = []
        self.success_init = self._update_info()

    def scan_devices(self):
        """Scan for new devices and return a list with found device IDs."""
        self._update_info()
        return self.last_results

        # pylint: disable=no-self-use
    def get_device_name(self, device):
        """Firmware doesn't save the name of the wireless device.
        Home Assistant will default to MAC address."""
        return None

    def _update_info(self):
        _LOGGER.info("Loading wireless clients...")

        global stoken
        headers = {
            "Content-Type": "application/json"
        }

        loginUrl = "http://{}/cgi-bin/".format(self.host)

        passwordString = self.password.encode();
        result = base64.b64encode(passwordString)

        security = {'security': {'login': {'username': 'tab', 'password': result.decode()}}}
        r = requests.post(loginUrl, data=self.buildPostData("set", security), headers=headers)
        responseJson = json.loads(r.text)
        stoken = responseJson['module']['security']['login']['stok']

        getDeviceListUrl = "http://{}/cgi-bin/stok={}/data".format(self.host, stoken)
        deviceArgs = {'device_manage': {'client_list': None}}
        r = requests.post(getDeviceListUrl, data= self.buildPostData("get", deviceArgs), headers=headers)

        result = json.loads(r.text)
        results = []
        if(result['error_code'] == 0):
            clientList = result['module']['device_manage']['client_list']

            if clientList is None:
                return False

            for device in clientList:
                if device['online_status'] == "1":
                    results.append(device['mac'].replace('_','.'))
        self.last_results = results
        return True

    def buildPostData(self,method, args):
        postInfo = {}
        data = json.loads(json.dumps(postInfo))
        data['method'] = method
        data['_deviceType'] = 'PC'
        data['module'] = args
        postInfo = json.dumps(data)
        print(postInfo)
        return postInfo










