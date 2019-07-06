from .protocol import get_json_obj, ProtoConstants, CommandBase, CNames, InfoCommandBase, Endpoints


class SettingsItem(object):
    def __init__(self, json_obj):
        self.id = int(get_json_obj(json_obj, ProtoConstants.Item.HASHVAL))
        self.c_name = get_json_obj(json_obj, ProtoConstants.Item.CNAME)
        self.type = get_json_obj(json_obj, ProtoConstants.Item.TYPE)
        self.name = get_json_obj(json_obj, ProtoConstants.Item.NAME)
        self.value = get_json_obj(json_obj, ProtoConstants.Item.VALUE)
        self.options = []
        options = get_json_obj(json_obj, ProtoConstants.Item.ELEMENTS)
        if options is not None:
            for opt in options:
                self.options.append(opt)

class GetCurrentAudioCommand(InfoCommandBase):

    def __init__(self, device_type):
        super(GetCurrentAudioCommand, self).__init__()
        InfoCommandBase.url.fset(self, Endpoints.ENDPOINTS[device_type]["VOLUME"])

    @staticmethod
    def _get_items(json_obj):
        items = get_json_obj(json_obj, ProtoConstants.RESPONSE_ITEMS)
        if items is None:
            return []

        results = []
        for itm in items:
            item = SettingsItem(itm)
            results.append(item)

        return results

    def process_response(self, json_obj):
        items = self._get_items(json_obj)
        for itm in items:
            if itm.c_name.lower() == CNames.Audio.VOLUME:
                if itm.value is not None:
                    return int(itm.value)
                return None

        return 0

class GetPictureSettingCommand(InfoCommandBase):

    def __init__(self, picture_cname, device_type):
        super(GetPictureSettingCommand, self).__init__()

        if device_type == "soundbar":
            raise Exception("Picture settings not supported for device_type " + device_type)

        self._picture_cname = picture_cname
        url = Endpoints.ENDPOINTS[device_type]["PICTURE"] + '/' + picture_cname
        InfoCommandBase.url.fset(self, url)

    @staticmethod
    def _get_items(json_obj):
        items = get_json_obj(json_obj, ProtoConstants.RESPONSE_ITEMS)
        if items is None:
            return []

        results = []
        for itm in items:
            item = SettingsItem(itm)
            results.append(item)

        return results

    def process_response(self, json_obj):
        items = self._get_items(json_obj)
        for itm in items:
            if itm.c_name.lower() == self._picture_cname:
                return itm

        return None

class ChangePictureSettingCommand(CommandBase):
    def __init__(self, id_, cname, value, device_type):
        super(ChangePictureSettingCommand, self).__init__()

        if device_type == "soundbar":
            raise Exception("Picture settings not supported for device_type " + device_type)

        url = Endpoints.ENDPOINTS[device_type]["PICTURE"] + '/' + cname
        CommandBase.url.fset(self, url)
        self.VALUE = value
        # noinspection SpellCheckingInspection
        self.HASHVAL = int(id_)
        self.REQUEST = ProtoConstants.ACTION_MODIFY

    def process_response(self, json_obj):
        return True

