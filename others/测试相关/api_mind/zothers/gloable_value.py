
class g_var(object):
    _gloable_dic = {} #最大程度保证全局变量的互斥性

    def set_dict(self, key, value):
        self._gloable_dic[key] = value

    def show_dict(self):
        return self._gloable_dic

    def get_dict(self, key):
        return self._gloable_dic[key]

    def del_dict(self, key):
        del self._gloable_dic[key]