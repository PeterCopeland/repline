from recorder import recorder
from queue import Queue
from encoding import encode
import configparser
import os

class repline():
    def __init__(self):
        self.recorder = recorder.recorder()
        self.config = settings()

    def open_ui(self):
        #from ui.tk import Application
        #Application.open_ui(self)
        from ui.displayotronhat import ui
        ui.open_ui(self)
        # from ui.displayotronhat import record
        # record.open_ui(self)

    def record(self):
        """Start recording"""
        self.recorder.record()

    def stop(self):
        """Stop recording"""
        self.recorder.stop()

    def register_callback_queue(self, moduleName, queue: Queue):
        print ("module in self: {}".format(hasattr(self, moduleName)))
        if (hasattr(self, moduleName)):
            module = getattr(self, moduleName)
            print ("register_callback: {}".format(hasattr(module, "register_callback")))
            if (hasattr(module, "register_callback_queue")):
                module.register_callback_queue(queue)

class settings():
    config = configparser.ConfigParser()
    options = {
        "recording": {
            "normalisation": {
                "default": 0,
                "min": 0,
                "max": 2,
            },
        },
        "trackDetection": {
            "silenceThreshold": {
                "min": -100,
                "max": 0,
                "default": -16
            },
            "minSilenceLength": {
                "min": 100,
                "max": 10000,
                "step": 100,
                "default": 1000
            }
        },
        "encoding": {
            "outputFormat": {
                "default": encode.format_WAV
            }
        },
        "encoding_mp3": {
            "bitrate": {
                "default": "qscale:a 4"
            }
        },
        "encoding_oggvorbis": {
            "bitrate": {
                "default": "qscale:a 4"
            }
        },
        "encoding_aac": {
            "quality": "3"
        },
        "hardware": {
            "inputDevice": {
                "default": None
            },
            "outputDevice": {
                "default": None
            }
        }
    }

    def __init__(self):
        self.read()

    def get(self, group, setting):
        print ("Getting current value of %s.%s" % (group, setting))
        # Set a default if it's not already in the file
        if (not self.config.has_section(group)):
            print ("Populating section: %s" % group)
            self.config.add_section(group)
            for option in self.options[group].keys():
                print ("Getting default value of %s.%s" % (group, option))
                self.set_default(group, option)
        elif (self.config.has_option(group, setting)):
            self.set_default(group, setting)

        if self.config.has_option(group, setting):
            return self.config.get(group,setting)

    def set_default(self, group, setting):
        default = self.options[group][setting]["default"]
        print ('Default value for %s.%s is %s' % (group, setting, default))
        if default != None:
            if not self.config.has_section(group):
                self.config.add_section(group)
            self.config[group][setting] = str(default)

    def set(self, group, setting, value):
        if not self.config.has_section(group):
            self.config.add_section(group)
        self.config.set(group, setting, str(value))

    def save(self):
        with open('repline.ini', 'w') as configfile:
            self.config.write(configfile)

    def read(self):
        if (os.path.isfile('repline.ini')):
            with open('repline.ini', 'r') as configfile:
                self.config.read(configfile)

repline = repline()
repline.open_ui()